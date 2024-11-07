from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

dag = DAG(dag_id = 'parallel', start_date = datetime(2024,11,7), 
          schedule = '@daily',
          catchup = False)

extract_a = BashOperator(task_id = 'extract_a', bash_command = 'sleep 1', dag = dag)
extract_b = BashOperator(task_id = 'extract_b', bash_command = 'sleep 1', dag = dag)
load_a = BashOperator(task_id = 'load_a', bash_command = 'sleep 1', dag = dag)
load_b = BashOperator(task_id = 'load_b', bash_command = 'sleep 1', dag = dag)
transform = BashOperator(task_id = 'transform', bash_command = 'sleep 1', 
                         # Si esta task debe correr en algun worker en particular
                         queue = 'my_queue',
                         dag = dag)


extract_a >> load_a
extract_b >> load_b
# transform depende de 2 o mas task
[load_a, load_b] >> transform