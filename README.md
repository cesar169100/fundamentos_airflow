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
# Airflow Scheduler
El scheduler de Airflow es el componente que se encarga de programar y ejecutar las tareas definidas en los DAGs (Directed Acyclic Graphs). El scheduler monitorea continuamente los DAGs para determinar cuándo deben ejecutarse las tareas según los intervalos de tiempo definidos o en respuesta a eventos específicos. Cuando una tarea está lista para ejecutarse, el scheduler la coloca en una cola para que los workers la procesen.
# Instalación de Apache Airflow usando Docker
- Para ambientes productivos se recomienda mediante helm: "If you want to get an easy to configure Docker-based deployment that Airflow Community develops, supports and can provide support with deployment, you should consider using Kubernetes and deploying Airflow using Official Airflow Community Helm Chart"
- Descargar el docker-compose de airflow mediante: 
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.3.3/docker-compose.yaml'
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.10.0/docker-compose.yaml'
puedes cambiar la version, por ejemplo, en vez de 2.3.3 pueder ser 2.10.0 que es la mas reciente.
- Hacer los siguientes cambios en el docker-compose.yaml: 
AIRFLOW__CORE__LOAD_EXAMPLES: 'false' (linea 62)
AIRFLOW__SCHEDULER__DAG_DIR_LIST_INTERVAL: 5 (Este ya no viene en versiones recientes)
- Ejecutar:
docker compose down --volumes --remove-orphans
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env
docker compose up airflow-init
docker compose up

- Luego podrás acceder a la interfaz gráfica de Airflow mediante http://localhost:8080/ con user y pass igual a airflow
- docker rm -f $(docker ps -aq) : Eliminar todos los conatiners
- NOTA: Se levanto airflow en la version antigua 2.3.3, esta manera no es recomendable en prod, la usare para el curso hasta que vea como levantar airflow en un cluster de eks mediante helm, que es lo recomendado para ambientes productivos.
# Posibles configuraciones
- Hacerlas en el docker compose, en la seccion enviroment linea 54 vienen algunas pero obvio hay mas y estan en los docs de airflow.
# Variables y conexiones
- Definir variables en Airflow sirve para almacenar valores que pueden ser reutilizados en múltiples DAGs o tasks. Estas variables permiten que los flujos de trabajo sean más flexibles y dinámicos, facilitando la configuración de parámetros como rutas de archivos, credenciales, etc.
- Para una variable, en la interfaz grafica, ir a Admin -> Variables -> Crearla dando nombre, valor y descripcion. O importarla de un doc.
Tambien en Admin vamos a conexiones -> add new record -> Especificar sus atributos tipo nombre, url, host, user, password etc
- Hay distintos tipos de proovedores a los que podemos crear una conexion (aws s3, aws rds, postgre, etc), en caso de que el que se desea no este dentro de los tipos se debe instalar.
- NOTA: Para ejecutar comandos de airflow en python es necesario entrar al container del webserver de airflow: 'docker exec -it container_id python' 
# Implementando un DAG
- En dags/primer_dag.py se definen dags de 3 maneras.
- Cuando creas un archivo py en la carpeta dags en automatico reconoce los dags en ese script y los veras en la interfaz grafica
# Bash Operator
- El codigo esta en dags/bash_operator.py