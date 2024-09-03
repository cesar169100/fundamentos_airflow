from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

# Definimos funcion a ejecutar en nuestro DAG
def print_hello(country, **kwargs):
    print(f'Hola {country}')

python_dag = DAG(
    dag_id="python-operator",
    description="python",
    start_date=datetime(2024, 9, 2),
    schedule_interval="@once",
)
python_task_1 = PythonOperator(task_id="python-task-1", python_callable=print_hello, 
                             op_kwargs={'country':'Brasil'}, dag=python_dag)

python_task_2 = PythonOperator(task_id="python-task-1", python_callable=print_hello, 
                             op_kwargs={'country':'Mexico'}, dag=python_dag)
