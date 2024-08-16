# Dags y workflow
- Workflow: Flujo de trabajo y se construyen con DAG
- DAG: En Airflow, un DAG (Directed Acyclic Graph) es una estructura que define la relación y la secuencia de ejecución de un conjunto de tareas (tasks). Un DAG representa el flujo de trabajo como un gráfico dirigido, donde los nodos son las tareas y las aristas son las dependencias entre estas tareas.
Características Clave de un DAG:

    Dirigido: El flujo de ejecución tiene una dirección específica, es decir, las tareas deben seguir una secuencia definida.
    Acríclico: No puede haber ciclos en el flujo, lo que significa que ninguna tarea puede depender de sí misma directa o indirectamente.

Función en Airflow:
El DAG en Airflow se utiliza para orquestar tareas complejas, asegurando que se ejecuten en el orden correcto y gestionando las dependencias entre ellas. Cada DAG se define en un archivo Python y se puede programar para que se ejecute a intervalos regulares o en respuesta a ciertos eventos.
# Tasks
- Tipos de tasks: 
1) Operators: Son los que definen las task.
2) Sensors: Un sensor en Airflow es un tipo especial de task que "espera" un evento específico o una condición antes de permitir que otras tareas en el DAG continúen. Un sensor verifica repetidamente si la condición se cumple (como la existencia de un archivo, la finalización de una tarea en otro DAG, o una respuesta HTTP específica) y sólo después de que se cumple, la task se considera completa.
- Algunos ejemplos de task operators y task sensor:
1) BashOperator
    Descripción: Ejecuta comandos de Bash en una shell.
    Uso: Ideal para ejecutar scripts y comandos de shell directamente desde Airflow.
    Ejemplo: BashOperator(task_id='run_script', bash_command='python3 my_script.py')
2) PythonOperator
    Descripción: Ejecuta funciones Python.
    Uso: Útil cuando se necesita ejecutar lógica escrita en Python, como transformaciones de datos.
    Ejemplo: PythonOperator(task_id='run_function', python_callable=my_function)
3) HttpSensor
    Descripción: Espera una respuesta HTTP específica antes de continuar.
    Uso: Se utiliza para monitorear servicios web y actuar según el estado de respuesta.
    Ejemplo: HttpSensor(task_id='check_api', http_conn_id='my_api', endpoint='status', response_check=lambda response: "success" in response.text)
4) DockerOperator:
    Descripción: Ejecuta un contenedor Docker.
    Uso: Para ejecutar tareas dentro de contenedores Docker, permitiendo entornos de ejecución aislados.
    Ejemplo: `DockerOperator(task_id='run_docker', image='my_image', command='python script.py')`
5) KubernetesPodOperator:
    Descripción: Ejecuta un pod en un clúster de Kubernetes.
    Uso: Ideal para ejecutar tareas en un entorno Kubernetes.
    Ejemplo: `KubernetesPodOperator(task_id='run_pod', name='my_pod', image='my_image')`


