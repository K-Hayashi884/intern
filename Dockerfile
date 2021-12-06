FROM python:3.9-slim
ENV PYTHONUNBUFFERE=1 \
	PYTHONDONTWRITEBYCODE=1

WORKDIR /app
RUN apt-get update -qq && apt-get install -y build-essential postgresql-client libpq-dev
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY docker-entrypoint.sh /usr/local/bin
RUN chmod 777 /usr/local/bin/docker-entrypoint.sh
ENTRYPOINT ["docker-entrypoint.sh"]