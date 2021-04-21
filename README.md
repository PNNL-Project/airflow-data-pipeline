# airflow-data-pipeline

## Summary (Include Screenshots): 
    
    Airflow is an efficient open-source workflow management platform. A workflow consists of ‘Task’ and ‘Dependency’, which are defined in Python. Airflow uses directed acyclic graphs (DAGs) to manage workflow orchestration, and manages the scheduling and execution of all defined workflows. 
(1) This interface is the main page of Airflow, which shows all existing workflows.
![] (images/airflow-1.png)
(2) This interface is the ‘Tree View’ for a workflow. There are several columns in this interface. Each column is represented for a workflow executed in a scheduled time. The red circle means this task is failed due to various reasons. The green circle means this task is successful as expected.
![] (images/airflow-2.png)
(3) This interface is the ‘Graph View’ for a workflow. It shows ‘Dependencies’ within a workflow. Each rectangle is represented for a ‘Task’, which is the basic element of the workflow.
![] (images/airflow-3a.png)
![] (images/airflow-3b.png)
(4) This interface shows the running information for each execution.


## Relationship With Other Services: 

Airflow works automatically in the docker and provides the ’Hunting service’ with daily prediction data. All the data is preserved in the AWS MySQL database.

## Directions:

## Additional Notes:

