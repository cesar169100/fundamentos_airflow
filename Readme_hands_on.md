Este readme es para el curso de Udemy.
## Limitaciones de airflow/casos donde no es la mejor opcion
- Flujos de alta frecuencia(intervalos de segundos)
- Transferencia de datos en tiempo real
- Si el flujo es mu sencillo usa un cronjob y ya
## Notas
- Definiciones basicas checar el primer readme.md al igual que la instalacion con docker.
- Empezaremos este curso de manera practica con airflow en eks. En el curso de hands on solo se anotaran ejemplos y cosas importantes de la teoria.
# Curso airflow Hands on Guide
## Seccion 4: Primer data pipeline con airflow
- En esta seccion se ha desarrolado un ejemplo de como seria un pipeline con airflow, se define el dag que contiene las task y posteriormente se definen todas esas task que componen al dag. Al final se especifica el orden/dependencias de las tasks, el codigo esta en dags/user_processing.py
- En Airflow, los detalles de conexión (host, puerto, nombre de la base de datos, usuario, y contraseña) se configuran en la interfaz de Airflow como una Connection.
- Cuando usas PostgresHook(postgres_conn_id='postgres'), Airflow busca una conexión llamada postgres en la pestaña de Connections en la interfaz de Airflow (o definida en el archivo de configuración de Airflow si se ha configurado de esa forma).
- El backfilling es el proceso de ejecutar tareas en un intervalo de tiempo pasado para completar datos o tareas que no se ejecutaron debido a algún motivo, como una caída del sistema. En otras palabras, se utiliza para llenar "huecos" en la ejecución de los DAGs cuando hay periodos anteriores pendientes de ejecutar. Supón que tienes un DAG programado para ejecutarse diariamente (schedule_interval='@daily') con una start_date=datetime(2024, 10, 1). Si defines este DAG hoy (octubre 5 de 2024), Airflow intentará ejecutar el DAG el 1, 2, 3 y 4 de octubre (ejecuciones pasadas), poniéndose al día con el calendario hasta hoy.
## Seccion 5: The new way of scheduling dags
- Trigger (detonar) ejecuciones de un dag a partir de eventos como la existencia de datos en una db o la actualizacion de un archivo o db.
- Imagina un escenario de un dag muy largo (muchas task) y cada task es desarrollada por un miembro del equipo. Obviamente puede haber complicaciones de desarrollo pues cada quien desarrolla y usa herramientas segun su estilo y conocimiento; en este caso se pueden crear mini-dags los cuales componen cada uno solo un cierto numero de task, ie, un dag de 6 task se puede dividir en minidags cada uno de 2 task.
- En Airflow, los datasets permiten crear dependencias basadas en archivos o tablas de datos, para coordinar DAGs según la disponibilidad de los datos.
- Los codigos de esta seccion son producer.py y consumer.py
- Limitaciones de los Datasets:
1) Los dags de consumo de datasets se detonan cuando la tarea que hace un update termina exitosamente. Airflow no checa si ese cambio fue efectivamente realizado.
2) No se pueden combinar schedules de cron y de datasets
3) Si dos tareas actualizan un mismo dataset, entonces el dag de consumo se activa en cuanto una de las dos tareas termine, no espera a las dos
4) A dag can only use datasets in the same airflow instance. A dag cannot wait for a dataset defined in another airflow instance
## Section 6: Databases and executors
- Los ejecutores no ejecutan tareas, definen como ejecutar las task y en que sistema. Tienes executors locales y remotos; los locales como tu compu y remotos como el kubernetes executor para ejecutar en un cluster, CeleryExecutor tambien es para ejecutar en cluster. 
- En un entorno de airflow con docker-compose, puedes revisar el tipo de executor en la variable de entorno AIRFLOW__CORE__EXECUTOR que viene al inicio del archivo docker-compose.
- El docker compose trae de executor a CeleryExecutor, este docker compose, basicamente convierte tu compu en un cluster con 1 worker (obvio ademas de instalar la ui, scheduler, etc).
- Al levantar airflow con Celeryexecutor, tenemos acceso a flower, que es una herramienta web para gestionar y moniorear clusters de celery. Para que flower se levante debes levantar airflow normal con tu docker-compose pero agregando: docker-compose --profile flower up -d
- Se accede a flower en localhost:5555
- Con las colas (queues) puedes tener varias donde cada cola apunta a un tipo de worker. Por ejemplo, una cola llamada high_cpu apunta a un worker de 5cpus, otra cola llamada ml_model apunta a un worker GPU, etc
- Si quieres agregar otro nodo worker al cluster de airflow que se levanta con el docker compose, solo tienes que copiar toda la parte de airflow-worker (linea 150), pegarla abajo y cambiar el nombre a algo como airflow-worker-2, todo lo demas igual. Si levantas airflow con esta modificacion al docker compose tendras 2 nodos worker.
- Nuevamente, en el docker compose en la seccion de los airflow-worker hay un parametro que se llama command: celery worker (linea 152), aqui puedes modificarlo asi: 
command: celery worker -q queue_1, de esta manera este worker se encargara de ejecutar las task que sean enviadas a la cola queue_1. El worker que dejes sin asignar un nombre de queue sera la cola default, ahi se ejecutaran las tareas por default a menos que no especifiques una cola en particular.
- Un codigo que ejemplifica como asignar una task a una cola particular y por tanto a un worker es parallel_dag.py
## Seccion 7: Implementing advanced concepts in airflow
- Introducimos el concepto de subdags para agrupar tareas que puedan ser similares y luego que ese subdag sea parte de otro dag.
- Usaremos el codigo de parallel_subdags.py como ejemplo y los subdags se definen en la carpeta subdags
- Al parecer los subdags ya estan deprecados y como solo sirven para agrupar tareas, pues se hace ahora de forma mas sencilla con los taskGroups. En los mismos codigos anteriores se dice como.
- Xcom contiene informacion que quisieras compartir entre tareas. Una manera de hacerlo es que una tarea guarde la info en algun lugar (csv, bd, etc) y la segunda tarea tome esa info para hacer su trabajo. La manera nativa de airflow es hacerlo mediante xcom (cross comunication) que se guarda en la metabase de datos de airflow. Xcom sirve para datos chicos como un diccionario que pudiera ser util para otra task. El codigo de ejemplo es xcom_dag.py
- Elegir una task u otra en funcion de una condicion. En el mismo codigo xcom_dag.py viene como. Hay otros branch operators aparte del de python.
- Los triggers son los criterios para ejecutar tareas, el criterio por defecto es all_succeed, es decir si todas las tareas de las que t3 depende corren con exito entonces t3 se ejecuta 
([t1,t2] >> t3), pero hay otros criterios, por ejemplo que t3 se ejecute solo si una de las dos son exitosas o ambas fallan. Ejemplo en el mismo codigo anterior
## Seccion 8: Creating airflow plugins with elasticsearch and postgreSQL
- En esta seccion se vera como crear nuestros propios hooks, operadores, etc 
- El archivo docker-compose-es.yaml es airflow pero tambien agrega elasticsearch.
- Un Airflow plugin es una forma de extender la funcionalidad nativa de Airflow. Permite agregar nuevas capacidades, como operadores, hooks etc. Los plugins se implementan mediante Python y se registran en la carpeta plugins de tu instalación de Airflow
- Para crear algo nuevo (operator, hook, etc) se necesita crear una clase (MyHookClass, MyOperatorClass, etc) que hereda de la clase AirflowPlugin. Al parecer, si agregas un nuevo plugin debes reiniciar la aplicacion de airflow para que puedas usar este nuevo plugin
- El codigo de ejemplo para crear un hook que se comunique con elasticsearch esta en plugins como elastic_hook.py y en dags esta elastic_dag.py que usa el hook creado.
## Apendice
- En este apendice hay blogs para aprender a usar los operadores docker, kubernetes, setear variables, etc