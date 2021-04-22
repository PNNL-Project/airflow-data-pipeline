STEPS TO INSTALL AIRFLOW

Please follow the instructions below 

System Tested : Ubuntu 20.0.4
Requirements : Need to have docker installed on the system

Please run the scripts in the airflow folder in the following order

Please note that you need to have root access to run these scripts.

1. Run the airflow_install_step1.sh

Command : sudo ./airflow_install_step1.sh

This script will initialize the airflow containers

Please see to that the script does cause any errors

2. Run the airflow_install_step2.sh

Command : sudo ./airflow_install_step2.sh

The script will run the docker containers and install all the services and start airflow services

3. Run the airflow_install_libraries.sh

Command : sudo ./airflow_install_libraries.sh

This script will install the libraries.

4.Run the following code sudo docker ps -a. This will show the list of docker services running

Trouble Shooting:

If see the DAGS are not initialize . Please follow the following steps

1. Go to airflow_install directory. You need to have root access.

2. Run the airflow.sh script

Command : sudo ./airflow.sh bash

In this will open the command line of the container .

run the airflow db init

This willl initialize the dags