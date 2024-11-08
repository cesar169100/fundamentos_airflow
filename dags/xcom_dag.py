from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.utils.trigger_rule import TriggerRule
from datetime import datetime

# ti es una abreviatura de Task Instance, un objeto que proporciona contexto sobre la tarea en
# ejecución dentro de Airflow.
def t1_f(ti):
    suma = 2+2
    # Método del objeto ti que permite enviar datos de una tarea para que estén disponibles en
    # otras tareas.
    ti.xcom_push(key = 'my_key', value = suma)
    # key='my_key': Define una clave única para identificar el valor almacenado. Esto es útil
    # si se quieren almacenar múltiples valores en XCom desde la misma tarea.

def t2_f(ti):
    # Jalamos el valor generado por la task t1
    valor = ti.xcom_pull(key = 'my_key', task_ids = 't1')
    print(valor)

def branch_f(ti):
    valor = ti.xcom_pull(key = 'my_key', task_ids = 't1')
    if valor >= 5:
        return 't2'
    else:
        return 't3'

with DAG(dag_id = 'xcom_dag', start_date = datetime(2024,11,8),
         schedule = '@monthly',
         catchup = False) as dag:
    
    t1 = PythonOperator(task_id = 't1', python_callable = t1_f)
    branch = BranchPythonOperator(task_id = 'elecccion', python_callable = branch_f)
    t2 = PythonOperator(task_id = 't2', python_callable = t2_f)
    t3 = BashOperator(task_id = 't3', bash_command = "echo ''")
    # Configura t4 para que se ejecute solo si todas las tareas previas en su flujo (t2) tienen
    # éxito. Hay otros tipos de triggers
    t4 = BashOperator(task_id = 't4', bash_command = "echo ''",
                      trigger_rule=TriggerRule.ALL_SUCCESS  )

    # t1 >> t2 >> t3
    t1 >> branch >> [t2, t3]
    t2 >> t4