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
- Este archivo para levantar el cluster tiene una seccion de addons para instalar directo, sin embargo, no funciona no se instalan. Hay que hacerlo manual.
- La parte de Flux se dejara de lado por el momento, es mas para temas de devops y que interactue Git con el cluster
## Section 5: Deploying airflow with DAGS
- Doc oficial del chart de airflow escribir Helm Chart for Apache Airflow e ingresar a la pag oficial de airflow.apache.org
- El repo del chart de airflow: https://github.com/apache/airflow/tree/main/chart
- El KubernetesExecutor ejecuta las tareas en kuberntes, el scheduler de airflow manda una tarea u kubernetes levanta un pod para ejecutar esa tarea, un pod para cada tarea. Puedes definir que tantos recursos usar para cada task en especifico. Si las tareas son pequenas no conviene mucho, por eso una task en este caso es recomnedable que sea considerable.
- Instala el driver de EBS-CSI lo cual aparentemente no es necesario pues ya viene el addon en cluster.yml. En caso de que no jale, instalar driver como en el curso de kubernetes
- Instala airflow como se indica en comands.txt
- fernetKey es una clave criptográfica utilizada para cifrar datos sensibles en Airflow, como conexiones o variables. Es fundamental para la seguridad de la instalación.
- opciones: Probar opcion de bitnami, generar cluster con manifest cluster.yml que trae permisos de ebs y ademas instala en addon
