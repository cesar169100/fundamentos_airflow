# Este codigo trae las 3 maneras de definir un DAG
from airflow import DAG
from airflow.decorators import dag
from airflow.operators.empty import EmptyOperator
from datetime import datetime


# with DAG(
#     # nombre
#     dag_id="dag1",
#     description="dag1",
#     start_date=datetime(2022, 10, 31),
#     # Ejecucion una vez
#     schedule_interval="@once",
# ) as dag1:
#     op = EmptyOperator(task_id="dummy")


dag2 = DAG(
    dag_id="mi-primer-dag",
    description="2dag2",
    start_date=datetime(2022, 10, 31),
    schedule_interval="@once",
)
op2 = EmptyOperator(task_id="dummy2", dag=dag2)


# @dag(
#     dag_id="dag3",
#     description="dag3",
#     start_date=datetime(2022, 10, 31),
#     schedule_interval="@once",
# )
# def generate_dag():
#     op3 = EmptyOperator(task_id="dummy3")


# dag3 = generate_dag()