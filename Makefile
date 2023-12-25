run:
	uvicorn config_fastapi.app:app --reload --port 8000


socketio:
	uvicorn config_socketio.socketio_app:socket_app --reload --port 8001


worker:
	celery -A config_celery.celery.celery_app worker --loglevel=info


migration:
	alembic revision --autogenerate


migrate:
	alembic upgrade head


alembic:
	alembic init -t async migrations


celery_clear:
	celery purge


init_scripts:
	python init_scripts.py


asyncapi_docs:
	python src/chat/asyncapi/generator.py
	sudo ag asyncapi_docs.yaml @asyncapi/html-template -o static/async_api --force-write
	sudo mv static/async_api/index.html templates/asyncapi
	sudo chmod 746 templates/asyncapi/index.html

rabbit:
	sudo docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.12-management
