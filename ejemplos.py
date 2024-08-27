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