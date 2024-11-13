# Creacion de un hook para interactuar con elasticsearch. Es necesario reiniciar el contenedor
# de airflow para poder ver el nuevo hook
from airflow.plugins_manager import AirflowPlugin
from airlow.hooks.base import BaseHook # Clase padre que heredara propiedades a nuestro hook
from elasticsearch import Elasticsearch

class ElasticHook(BaseHook):
    # conn_id es la conexion definida en la ui de airflow
    def __init__(self, conn_id='elastic_default', *args, **kwargs):
        super().__init__(*args, **kwargs)
        conn = self.get_connection(conn_id)

        conn_config = {}
        hosts = []
        # si host está presente, crea una lista de hosts separando los valores por comas
        if conn.host:
            hosts = conn.host.split(',')
        if conn.port:
            conn_config['port'] = int(conn.port)
        if conn.login:
            conn_config['http_auth'] = (conn.login, conn.password)

        # Inicializa el cliente de Elasticsearch (self.es) con los hosts y configuración 
        # (conn_config).
        self.es = Elasticsearch(hosts, **conn_config)
        self.index = conn.schema

    def info(self):
        return self.es.info()
    
    def set_index(self, index):
        self.index = index

    def add_doc(self, index, doc_type, doc):
        self.set_index(index)
        res = self.es.index(index=index, doc_type=doc_type, doc=doc)
        return res

# Define el plugin ElasticPlugin de Airflow, registrando ElasticHook como hook disponible en 
# el sistema.    
class ElasticPlugin(AirflowPlugin):
    name = 'elastic'
    hooks = [ElasticHook]