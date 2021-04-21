DIR1="/opt/airflow/dags/Tempdata"$1
DIR2="/opt/airflow/logs/A_pnnl"
if [ -d "$DIR1" ]; then
  rm -rf $DIR1
fi
if [ -d "$DIR2" ]; then
  rm -rf $DIR2
fi