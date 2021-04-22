**STEPS TO INSTALL AIRFLOW**

Please follow the instructions below 

**System Tested : Ubuntu 20.0.4
Requirements : Need to have docker installed on the system
**
**Please run the scripts in the airflow folder in the following order
**
Please note that you need to have root access to run these scripts.

**1. Run the airflow_install_step1.sh**

**Command :** sudo ./airflow_install_step1.sh

This script will initialize the airflow containers

Please see to that the script does cause any errors

The output should be

![image](https://user-images.githubusercontent.com/56701482/115645306-1ef1a080-a2ee-11eb-8e0a-d104983b5211.png)


**2. Run the airflow_install_step2.sh**

**Command :** sudo ./airflow_install_step2.sh

The script will run the docker containers and install all the services and start airflow services

The output should be

![image](https://user-images.githubusercontent.com/56701482/115645404-51030280-a2ee-11eb-9dc2-ea0c54604611.png)


**3. Run the airflow_install_libraries.sh**

**Command :** sudo ./airflow_install_libraries.sh

This script will install the libraries.

The output should be

![image](https://user-images.githubusercontent.com/56701482/115645460-6bd57700-a2ee-11eb-94e4-e71a2ffeb40e.png)


**4.Run the following code sudo docker ps -a. This will show the list of docker services running**

**Trouble Shooting:**

If see the DAGS are not initialize . Please follow the following steps

1. Go to airflow_install directory. You need to have root access.

2. Run the airflow.sh script

Command : sudo ./airflow.sh bash

In this will open the command line of the container .

run the airflow db init

This willl initialize the dags


Go to localhost:8080

The username and password will be airflow

The console should look like 

![image](https://user-images.githubusercontent.com/56701482/115646342-f9fe2d00-a2ef-11eb-938d-1f51b89c9b11.png)
