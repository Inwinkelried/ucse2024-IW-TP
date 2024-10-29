FROM python:3.11.9
ENV PYTHONUNBUFFERED 1
ENV DOCKER=True

RUN mkdir /app_grupo1
RUN mkdir /data

WORKDIR /app_grupo1

COPY requirements.txt /app_grupo1/
RUN pip install -r requirements.txt

COPY . /app_grupo1/

RUN python padel/manage.py migrate --database=default
RUN python padel/manage.py rebuild_index --noinput

CMD python padel/manage.py migrate;python padel/manage.py runserver 0.0.0.0:8000