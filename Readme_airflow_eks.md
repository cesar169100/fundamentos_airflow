# Curso airflow en EKS
## Notas previas
- Se puede definir un presupuesto(budget) en aws
- FluxCD es una herramienta de GitOps para gestionar configuraciones y despliegues en Kubernetes mediante el uso de repositorios Git como la única fuente de verdad. Al monitorear cambios en los archivos de configuración almacenados en Git, FluxCD asegura que el estado de tu clúster siempre esté sincronizado con el contenido del repositorio.
- FluxCD observa los cambios en un repositorio Git que contiene manifestos de Kubernetes. Cada vez que se actualizan, se activa un ciclo de sincronización.
- FluxCD permite volver fácilmente a versiones anteriores en caso de errores, ya que siempre se puede recuperar el estado anterior desde Git.
- repo del curso: https://github.com/marclamberti/airflow-materials-aws
- Cloud9 de aws proporciona un IDE de desarrollo
- helm repo add stable https://charts.helm.sh/stable
## Section 4: Creating cluster
- Se levanta el cluster con el archivo cluster.yml
- El archivo para levantar el cluster es cluster.yml
- La parte de Flux se dejara de lado por el momento, es mas para temas de devops y que interactue Git con el cluster
## Section 5: Deploying airflow with DAGS
- Doc oficial del chart de airflow escribir Helm Chart for Apache Airflow e ingresar a la pag oficial de airflow.apache.org
- El repo del chart de airflow: https://github.com/apache/airflow/tree/main/chart
- El KubernetesExecutor ejecuta las tareas en kuberntes, el scheduler de airflow manda una tarea u kubernetes levanta un pod para ejecutar esa tarea, un pod para cada tarea. Puedes definir que tantos recursos usar para cada task en especifico. Si las tareas son pequenas no conviene mucho, por eso una task en este caso es recomnedable que sea considerable.
- Se agrego en el manifest del cluster (cluster.yaml) el addon de ebs pues es necesario para el despliegue.
- Instala airflow como se indica en comands.txt de esta seccion 5, optamos por la version de bitnami. El archivo values.yaml tiene los parametros de configuracion para ser desplegado sin problemas
- fernetKey es una clave criptográfica utilizada para cifrar datos sensibles en Airflow, como conexiones o variables. Es fundamental para la seguridad de la instalación. El codigo para generar una es fernet_key.py
- Para cargar los dags, se uso un reposiorio publico por facilidad. En la practica sera uno privado y no es recomendable poner la ruta con el token pues esto es informacion sensible. LO recomendable es generar una ssh key y tratarla como secret montada en un volumen. Ver la seccion manifest_examples/volumenes del curso de kubernetes, ahi viene la explicacion de un secret. Los comandos para crear las llaves ssh estan en create_ssh.txt
- Una vez creadas las llaves, en el values.yaml poner en el parametro repository la url de ssh, no la de http. Crear un secret (kubectl apply -f secrets.yaml) en el namespace de airflow con la llave privada y especificarlo en values.yaml. En la practica, nunca guardar el manifest de secrets.yml en la nube.
## Section 6: Building CI/CD pipelines to deploy airflow
- Esta seccion se trata del uso de aws Codepipeline para implementar pipelines en airflow. Codepipeline construye imagenes con airflow y las dependencias de los dags y se guardan en ECR. Esta seccion va mas acorde a un curso de CI/CD, ademas de que se pueden construir imagenes, guardarlas en ECR y usarlas en dags a traves de un kubernetes executor; tal vez no sea la practica correcta pero de momento probare esa manera y nos movemos a la siguiente  seccion.
## Seccion 7: Exposing the airflow UI
