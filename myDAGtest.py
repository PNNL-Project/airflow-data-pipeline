from datetime import timedelta,datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retry_delay': timedelta(seconds=30)
}
dag = DAG(
    dag_id='A_pnnl_test2',
    default_args=default_args,
    start_date=datetime(year=2020, month=1,day=1,hour=8,second=1),
    schedule_interval=timedelta(hours=4),
    catchup=True,
    tags=['A_pnnl_test2']
)


def init(**kwargs):
    if datetime.now().hour != 12:
        raise('Failed')

task_start = PythonOperator(
    task_id="task_start",
    python_callable=init,
    dag=dag)

task_create_folder = BashOperator(
    task_id="task_create_folder",
    bash_command='/opt/airflow/dags/create_folder.sh "{{ execution_date }}" ',
    dag=dag)


task_download = BashOperator(
    task_id='task_download',
    bash_command='python3 /opt/airflow/dags/task_download.py "{{ execution_date }}" ',
    do_xcom_push=True,
    dag=dag)

task_download_zoneTemperature = BashOperator(
    task_id="task_download_zoneTemperature",
    bash_command='echo task_download_zoneTemperature ',
    dag=dag
)
task_download_zoneAirflow = BashOperator(
    task_id="task_download_zoneAirflow",
    bash_command='echo task_download_zoneAirflow ',
    dag=dag
)
task_zoneAirflow_predict = BashOperator(
    task_id='task_zoneAirflow_predict',
    # Must have a space
    bash_command='python3 /opt/airflow/dags/task_predict.py "{{ ti.xcom_pull(task_ids="task_download", key="return_value") }}" "zoneAirflow" "{{ execution_date }}" ',
    dag=dag)

task_predict_zoneAirflow = BashOperator(
    task_id="task_predict_zoneAirflow",
    bash_command='echo task_predict_zoneAirflow ',
    dag=dag
)

task_zoneAirflow_upload = BashOperator(
    task_id='task_zoneAirflow_upload',
    # Must have a space
    bash_command='python3 /opt/airflow/dags/task_upload.py "{{ ti.xcom_pull(task_ids="task_download", key="return_value") }}" "zoneAirflow" "{{ execution_date }}" ',
    dag=dag)

task_zoneTemperature_predict = BashOperator(
    task_id='task_zoneTemperature_predict',
    # Must have a space
    bash_command='python3 /opt/airflow/dags/task_predict.py "{{ ti.xcom_pull(task_ids="task_download", key="return_value") }}" "zoneTemperature" "{{ execution_date }}" ',
    dag=dag)

task_predict_zoneTemperature = BashOperator(
    task_id="task_predict_zoneTemperature",
    bash_command='echo task_predict_zoneTemperature ',
    dag=dag
)

task_zoneTemperature_upload = BashOperator(
    task_id='task_zoneTemperature_upload',
    bash_command='python3 /opt/airflow/dags/task_upload.py "{{ ti.xcom_pull(task_ids="task_download", key="return_value") }}" "zoneTemperature" "{{ execution_date }}" ',
    dag=dag)

task_zoneAirflow_failure = BashOperator(
    task_id='task_zoneAirflow_failure',
    # Must have a space
    bash_command='python3 /opt/airflow/dags/task_upload_failure.py "{{ ti.xcom_pull(task_ids="task_download", key="return_value") }}" "zoneAirflow" ',
    trigger_rule='one_failed',
    dag=dag)


task_zoneTemperature_failure = BashOperator(
    task_id='task_zoneTemperature_failure',
    # Must have a space
    bash_command='python3 /opt/airflow/dags/task_upload_failure.py "{{ ti.xcom_pull(task_ids="task_download", key="return_value") }}" "zoneTemperature" ',
    trigger_rule='one_failed',
    dag=dag)

task_failure = BashOperator(
    task_id='task_failure',
    # Must have a space
    bash_command='/opt/airflow/dags/remove_cache.sh "{{ execution_date }}" ',
    trigger_rule='one_failed',
    dag=dag)

task_success = BashOperator(
    task_id='task_success',
    # Must have a space
    bash_command='/opt/airflow/dags/remove_cache.sh "{{ execution_date }}" ',
    trigger_rule='all_success',
    dag=dag)



task_start >> task_create_folder >> task_download >> [task_download_zoneTemperature,task_download_zoneAirflow,task_zoneAirflow_failure,task_zoneTemperature_failure]
task_start >> task_failure
task_download_zoneAirflow >> task_zoneAirflow_predict >> task_predict_zoneAirflow >> task_zoneAirflow_upload >> task_zoneAirflow_failure
task_download_zoneTemperature >> task_zoneTemperature_predict >> task_predict_zoneTemperature >> task_zoneTemperature_upload >> task_zoneTemperature_failure
task_zoneAirflow_predict >> task_zoneAirflow_failure
task_zoneTemperature_predict >> task_zoneTemperature_failure
[task_zoneAirflow_upload,task_zoneTemperature_upload] >> task_success
[task_zoneAirflow_failure,task_zoneTemperature_failure] >> task_failure