run-uvicorn:
	cd src && uvicorn main:app --host=0.0.0.0 --port=8000

run:
	alembic upgrade head && \
	cd src && \
	uvicorn main:app --host=0.0.0.0 --port=8000

run-faststream:
	cd src && faststream run event_processor:app
