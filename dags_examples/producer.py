from airflow import DAG, Dataset
from airflow.decorators import task
from datetime import datetime

# Puede ser un archivo, una base de datos etc, solo necesitas poner su uri (direccion)
my_file = Dataset('/tmp/my_file.txt')
my_file2 = Dataset('/tmp/my_file2.txt')
# Caso de archivo o rds de aws
# my_file_s3 = Dataset('s3://my-bucket-name/my_folder/my_file.csv')
# my_rds_table = Dataset('rds://my-db-instance/my_database/my_table')

# Un Dag que interactuara con un datasets
dag = DAG(dag_id = 'producer',
          # Cambio schedule_interval a solo schedule desde la version 2.4 de airflow 
          schedule = '@daily',
          start_date = datetime(2024,11,6),
          catchup = False )

# Declara update_dataset como una tarea y especifica que esta tarea genera my_file como output,
# permitiendo que otros DAGs o tareas puedan depender de este archivo como dataset.
@task(outlets=[my_file])
# Dentro de update_dataset, el archivo representado por my_file se abre en modo "append" ("a+")
# y se agrega el texto "producer update" al archivo.
def update_dataset():
    with open(my_file.uri, "a+") as f:
        f.write("producer update")

@task(outlets=[my_file2])
def update_dataset2():
    with open(my_file2.uri, "a+") as f:
        f.write("producer update")

# Ejecuta la función update_dataset dentro del DAG
update_dataset() >> update_dataset2()

## Notas
# 1) Al definir la task con el decorador @task se asocia directamente con el dag sin necesidad
#    de hacerlo explicitamente.
# 2) En este ejemplo se usó el decorador @task en lugar de un operador tradicional como 
# PythonOperator. Desde Airflow 2.0, se introdujo el concepto de TaskFlow API, que permite 
# definir tareas de una forma más "Pythonica" usando decoradores como @task. 
# 3) El decorador @task puede sustituir algunos operadores más allá del PythonOperator, ya que 
# en Airflow 2.0+ también se introdujeron otros decoradores, como @task.bash, @task.virtualenv, 
# y @task.kubernetes
# 4) Si necesitas leer o escribir en S3 o RDS, además de definir los datasets, tendrías que 
# usar operadores de interacción específicos (como S3Hook para S3 o PostgresHook para RDS) 
# dentro de tus tareas.