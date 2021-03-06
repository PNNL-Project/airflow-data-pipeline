# airflow-data-pipeline

## Summary (Include Screenshots): 
Airflow is an efficient open-source workflow management platform. A workflow consists of ‘Task’ and ‘Dependency’, which are defined in Python. Airflow uses directed acyclic graphs (DAGs) to manage workflow orchestration, and manages the scheduling and execution of all defined workflows. The following images show basic interfaces of Airflow:
#### (1) This interface is the main page of Airflow, which shows all existing workflows.
![](images/airflow-1.png)
##### (2) This interface is the ‘Tree View’ for a workflow. There are several columns in this interface. Each column is represented for a workflow executed in a scheduled time. The red circle means this task is failed due to various reasons. The green circle means this task is successful as expected.
![](images/airflow-2.png)
##### (3) This interface is the ‘Graph View’ for a workflow. It shows ‘Dependencies’ within a workflow. Each rectangle is represented for a ‘Task’, which is the basic element of the workflow.
![](images/airflow-4.png)
##### (4) This interface shows the running information for each execution.
![](images/airflow-3.png)
****
'DAG', directed acyclic graph, is the most important part in the Airflow. 'myDAGtest.py' is the DAG file of this project, and the workflow in this project is:

![](images/airflow-5.png)
****
Python files cannot be executed in 'DAG' directly. The way to run python files is to use 'BashOperator' in the Airflow. 'BashOperator' provides a way to execute commands in a Bash shell, which can also take input parameters. 'task_download.py', 'task_predict.py', 'task_upload.py' and 'task_upload_failure.py' are four python files which are expected to run within the 'BashOperator'. 'remove_cache.sh' is used to remove cache for each workflow, which can save memory for the server. There are five steps in the workflow, which is implemented by the previous 'BashOperator':

![](images/airflow-6.png)


## Relationship With Other Services: 
   Airflow works automatically in the docker and provides the ’Alert service’ with daily prediction data. Prediction results will be defined as '-1' if there is anything wrong with the original device data. All the data is stored back in the AWS MySQL database.

## Instructions:
   ### (1)'DatabaseSetting.yaml' needs to be changed whenever creating a new project. This yaml is used to change the MySQL database settings. Notice that the bottom line (circled in the picture below) represents the database tables queried. 
![](images/database-setting-tables.png)
     *What were the database tables used for?*
     * *seb_processed_data_time_shifted*: used to query and process data to be run through ml model
     * *zoneairflow_labeled_agg*: used to store the zone airflow prediction data
     * *zonetemp_labeled_agg*: used to store the zone temperature prediction data
   ### (2)Change the 'start_date'(in dag) in 'myDAGtest.py' before starting a new schedule.
   ### (3)Run command 'airflow db init' when DAG files be updated. This command is used to refresh the database in Airflow to update all changes.
   ### (4)Airflow runs jobs at the end of an interval, not the beginning. This means that the first run of the job is going to be after the first interval. For example, a daily job(which starts at 0:00 a.m.) will be executed in the next day 0:00 a.m. .
   ### (5)The ML models are placed under the 'Models' folder. 'zone_airflow_model.joblib' is for the prediction of 'zoneairflow' devices, and 'zone_temperature_model.joblib' is for the prediction of 'zonetemperature' devices. 
   ### (6)Label names are in the 'ML_labels.yml' file under 'Setting' folder. 

## What to do if the ML model needs to be changed:
1. Replace the models in the [Models](https://github.com/PNNL-Project/airflow-data-pipeline/tree/master/Models) folder
2. Make sure that the data pipeline model labels located in [ML_labels.yml](https://github.com/PNNL-Project/airflow-data-pipeline/blob/master/Setting/ML_labels.yml) match **exactly** to the order of labels created when building the model. The code to build the models are located in these two Jupyter Notebooks: [zone_airflow_model_training.ipynb](https://github.com/PNNL-Project/ml-models/blob/master/zoneairflow_model_training.ipynb) & [zonetemp_model_training.ipynb](https://github.com/PNNL-Project/ml-models/blob/master/zonetemp_model_training.ipynb) 

So for example, The following lists must match:
![](images/airflow-labels.png)
![](images/training_zonetemp.png)
![](images/training_zoneairflow.png)

## Steps to install Airflow

Please follow the instructions below 

System Tested : Ubuntu 20.0.4
Requirements : Need to have docker installed on the system

Please run the scripts in the airflow folder in the following order

Please note that you need to have root access to run these scripts.

### 1. Run the airflow_install_step1.sh

Command : sudo ./airflow_install_step1.sh

This script will initialize the airflow containers

Please see to that the script does cause any errors

### 2. Run the airflow_install_step2.sh

Command : sudo ./airflow_install_step2.sh

The script will run the docker containers and install all the services and start airflow services

### 3. Run the airflow_install_libraries.sh

Command : sudo ./airflow_install_libraries.sh

This script will install the libraries.

#### 4.Run the following code sudo docker ps -a. This will show the list of docker services running
****

Trouble Shooting:

If see the DAGS are not initialize . Please follow the following steps

#### 1. Go to airflow_install directory. You need to have root access.

#### 2. Run the airflow.sh script

Command : sudo ./airflow.sh bash

In this will open the command line of the container .

run the airflow db init

This will initialize the dags
