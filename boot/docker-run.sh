#!/bin/bash

source /opt/venv/bin/activate

cd /code
RUN_PORT=${PORT:-8000}
RUN_HOST=${HOST:-0.0.0.0}

uvicorn main:app --host $RUN_HOST --port $RUN_PORT
#uvicorn  -k uvicorn.workers.UvicornWorker -b $RUN_HOST:$RUN_PORT main:app
