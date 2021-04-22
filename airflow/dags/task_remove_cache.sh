DIR1="/opt/airflow/dags/Tempdata"
DIR2="/opt/airflow/logs/A_pnnl"
if [ ! -d "$DIR1" ]
then
  mkdir $DIR1
else
  rm -rf $DIR1
  mkdir $DIR1
fi
if [ ! -d "$DIR2" ]
then
  mkdir $DIR2
else
  rm -rf $DIR2
  mkdir $DIR2
fi