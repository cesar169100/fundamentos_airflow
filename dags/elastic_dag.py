from airflow import DAG
from airflow.operators.python import PythonOperator
from plugins.hooks.elastic.elastic_hook import ElasticHook
from datetime import datetime

def print_info():
    hook = ElasticHook()
    print(hook.info())

with DAG(dag_id='elastic_dag', start_date=datetime(2024,11,13),
         shedule = '@daily',
         catchup = False) as dag:
    
    info = PythonOperator(task_id='print info', python_callable=print_info)