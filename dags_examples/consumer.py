# Este codigo consume el archivo modificado en producer.py y por lo tanto se detona una vez que 
# el dag de producer.py termine su ejecucion

from airflow import DAG, Dataset
from airflow.decorators import task
from datetime import datetime

# Necesitamos el dataset de producer.py
my_file = Dataset('/tmp/my_file.txt')
my_file2 = Dataset('/tmp/my_file2.txt')

# Tambien se puede defirnir como dag=DAG()
with DAG(dag_id = 'consumer',
        # No se define schedule en base a tiempo sino en base a un dataset. Es decir se
        # calendariza en funcion de las actualizaciones que reciba
        schedule = [my_file, my_file2], # Ahora se detona hasta que se modifiquen 2 datasets
        # Lo demas igual
        start_date = datetime(2024,11,6),
        catchup = False 
):
    
    @task
    def read_dataset():
        with open(my_file.uri, "r") as f:
            print(f.read())

    read_dataset()