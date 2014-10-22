from celery import Celery

celery = Celery(__name__)
celery.config_from_object('endpoint')

@celery.task
def update_external(external):
	external.getRegistry()
	
