mkdir airflow_install
cp -r dags airflow_install
cd airflow_install
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.0.2/docker-compose.yaml'
mkdir -m 777 logs  plugins
docker-compose up airflow-init

