from airflow import DAG
from datetime import datetime
from airflow.operators.bash import BashOperator

bash_dag = DAG(
    dag_id="bash-operator",
    description="bash",
    start_date=datetime(2024, 9, 2),
    schedule_interval="@once",
)
bash_task = BashOperator(task_id="bash-task", bash_command="echo 'Hola Mundo'",
                         dag=bash_dag)
bash_task