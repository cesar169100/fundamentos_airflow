from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.subdag import SubDagOperator
from subdags.subdag import extract_group, load_group
from datetime import datetime

with DAG(dag_id = 'parallel', start_date = datetime(2024,11,7), 
          schedule = '@daily',
          catchup = False) as dag:

# Los args de los subdags
# args = {'start_date': dag.start_date, 'schedule': dag.schedule, 'catchup': dag.catchup}
# extraction = SubDagOperator(task_id = 'extraction', 
#                             # el child_id debe ser el mismo que el task_id
#                             subdag = extract_subdag(dag.dag_id, 'extraction'),
#                             args = args)

# load = SubDagOperator(task_id = 'load', 
#                       subdag = load_subdag(dag.dag_id, 'load'),
#                       args = args)
    extraction = extract_group()
    load = load_group()

    transform = BashOperator(task_id = 'transform', bash_command = 'sleep 1', 
                         # Si esta task debe correr en algun worker en particular
                         queue = 'my_queue' )

# En este caso a lo mejor no tenia mucho sentido hacer subdag pero es solo para ejemplificar    
    extraction >> load >> transform