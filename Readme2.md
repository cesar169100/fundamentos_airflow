Este readme es para el curso de Udemy.
## Limitaciones de airflow/casos donde no es la mejor opcion
- Flujos de alta frecuencia(intervalos de segundos)
- Transferencia de datos en tiempo real
- Si el flujo es mu sencillo usa un cronjob y ya
## Notas y GitOps
- Definiciones basicas checar el primer readme.md al igual que la instalacion con docker.
- Empezaremos este curso con airflow en eks
- Se puede definir un presupuesto(budget) en aws
- FluxCD es una herramienta de GitOps para gestionar configuraciones y despliegues en Kubernetes mediante el uso de repositorios Git como la única fuente de verdad. Al monitorear cambios en los archivos de configuración almacenados en Git, FluxCD asegura que el estado de tu clúster siempre esté sincronizado con el contenido del repositorio.
- FluxCD observa los cambios en un repositorio Git que contiene manifestos de Kubernetes. Cada vez que se actualizan, se activa un ciclo de sincronización.
- FluxCD permite volver fácilmente a versiones anteriores en caso de errores, ya que siempre se puede recuperar el estado anterior desde Git.
- repo del curso: https://github.com/marclamberti/airflow-materials-aws
- Cloud9 de aws proporciona un IDE de desarrollo
- helm repo add stable https://charts.helm.sh/stable