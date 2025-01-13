from airflow import DAG
from datetime import datetime
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
from pandas import json_normalize
import json

# Notacion cron posicion1: minuto, posicion2: hora, posicion3: dia del mes, posicion4: mes,
# posicion5: dia de la semana  * es cualquiera o todos
def process_user_f(ti):
    # Pull de lo generado por otra tarea
    user = ti.xcom_pull(task_ids = 'extract_user') 
    user = user['results'][0]
    processed_user = json_normalize({
        'firstname': user['name']['first'],
        'email': user['email']
    })
    process_user.to_csv('/tmp/processed.csv', index = None, header = False)

# funcion que utiliza un hook para cargar datos desde un archivo CSV a una tabla en una base 
# de datos PostgreSQL, notas de esto en el readme2
def store_user_f():
    hook = PostgresHook(postgres_conn_id='postgres')
    hook.copy_expert(
        sql = "COPY users FROM stdin WITH DELIMITER as ','",
        filename = '/tmp/processed_user.csv'
    )


user_processing_dag = DAG(
    dag_id = "user-procesing", # Id unico del dag
    description = "una descripcion",
    start_date = datetime(2024, 11, 6),
    # schedule_interval="@once", # @daily si es diario, lo hace a media noche etc
    schedule_interval = "0 11 * * *", # Diario a las 11am
    end_date = datetime(2024, 11, 7),
    catchup = False # Si lo dejas en true, en cuanto llegue la fecha de ejecucion, ejecutara todas
                    # las corridas no hechas entre la fecha de creacion y la start_date.
)
create_table = PostgresOperator(task_id="create-table", postgres_conn_id='postgres',
                                sql= ''' 
                                CREATE TABLE IF NOT EXISTS users (
                                firstname TEXT NOT NULL
                                email TEXT NOT NULL
                                );
                                ''',
                                # Podemos usar, tambien, un archivo.sql para ejecutar
                                dag = user_processing_dag
                                )

is_api_available = HttpSensor(task_id = 'availability',
                              #Pues interactua con un servicio externo, en este caso una url
                              http_conn_id = 'user_api',
                              enpoint = 'api/',
                              poke_interval=60,  # Intentará cada 60 segundos
                              timeout=600, # Tiempo total (10min)
                              dag = user_processing_dag
                              )

extract_user = SimpleHttpOperator(task_id = 'extract',
                                  http_conn_id = 'user_api',
                                  enpoint = 'api/',
                                  method = 'GET', #Pedir un dato, no enviarlo
                                  # Convertir la respuesta del GET a formato json
                                  response_filter = lambda response: json.loads(response.text),
                                  # Ver los logs en la UI
                                  log_response = True,
                                  dag = user_processing_dag
                                  )

process_user = PythonOperator(task_id = 'process', python_callable=process_user_f,
                              dag = user_processing_dag)

store_user = PythonOperator(task_id='store_user', python_callable=store_user_f,
                              dag = user_processing_dag)
# Especificamos orden/dependencias. Primero se ejecuta create_table
create_table >> is_api_available >> extract_user >> process_user >> store_user
