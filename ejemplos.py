## Llamado de variables / importacion
from airflow.models import Variable

variable = Variable.get("mi-variable")
variable2 = Variable.get("mi-variable2", deserialize_json=True)

## Este código configura una tarea en un DAG de Airflow que ejecutará un script SQL 
# (pet_schema.sql) en una base de datos PostgreSQL utilizando una conexión especificada por 
# my_postgres_conn. Esta tarea podría ser utilizada, por ejemplo, para poblar una tabla en la 
# base de datos.
from airflow.providers.postgres.operators.postgres import PostgresOperator
populate_pet_table = PostgresOperator(
		task_id="populate_pet_table",
		postgres_conn_id="my_postgres_conn",
		sql="sql/pet_schema.sql",
)

from airflow import DAG
from datetime import datetime
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

bash_dag = DAG(
    dag_id="bash-operator",
    description="bash",
    start_date=datetime(2024, 9, 2),
    schedule_interval="@once",
)
bash_task = BashOperator(task_id="bash-task", bash_command="echo 'Hola Mundo'",
                         dag=bash_dag)
bash_task

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