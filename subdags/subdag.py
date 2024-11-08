# Aqui crearemos un subdag para tareas de extraccion y otro subdag para tareas de load.
from airflow import DAG
from airflow.operators import BashOperator
from airflow.utils.task_group import TaskGroup

# parent_dag_id es el dag mas grande del que este subdag formara parte
# Los args como schedule, catchup etc deben ser los mismos que el dag padre
# def extract_subdag(parent_dag_id, child_dag_id, args):
#     dag = DAG(f"{parent_dag_id}.{child_dag_id}",
#               start_date = args['start_date'],
#               schedule = args['schedule'],
#               catchup = args['catchup'] )
    
#     extract_a = BashOperator(task_id = 'extract_a', bash_command = 'sleep 1', dag = dag)
#     extract_b = BashOperator(task_id = 'extract_b', bash_command = 'sleep 1', dag = dag)

#     return dag

# def load_subdag(parent_dag_id, child_dag_id, args):
#     dag = DAG(f"{parent_dag_id}.{child_dag_id}",
#               start_date = args['start_date'],
#               schedule = args['schedule'],
#               catchup = args['catchup'] )
    
#     load_a = BashOperator(task_id = 'load_a', bash_command = 'sleep 1', dag = dag)
#     load_b = BashOperator(task_id = 'load_b', bash_command = 'sleep 1', dag = dag)

#     return dag

def extract_group():
    # Los grupos solo se pueden definir de esta forma
    with TaskGroup("Extraction", tooltip='extract') as group:
        extract_a = BashOperator(task_id = 'extract_a', bash_command = 'sleep 1')
        extract_b = BashOperator(task_id = 'extract_b', bash_command = 'sleep 1')
    return group

def load_group():
    # Los grupos solo se pueden definir de esta forma
    with TaskGroup("Load", tooltip='load') as group:
        load_a = BashOperator(task_id = 'load_a', bash_command = 'sleep 1')
        load_b = BashOperator(task_id = 'load_b', bash_command = 'sleep 1')
    return group
