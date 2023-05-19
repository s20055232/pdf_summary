FROM python:3.11
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

WORKDIR /code
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "back.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
#CMD ["gunicorn", "back.main:app", "--workers", "1", "--threads", "8", "--worker-class", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000"]
# `production` image used for runtime
#FROM python-base as production
#ENV FASTAPI_ENV=production
#COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
#COPY ./app /app/
#WORKDIR /app
#CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "main:app"]