DIR1="/opt/airflow/dags/Tempdata"$1
if [ ! -d "$DIR1" ]; then
  mkdir $DIR1
fi