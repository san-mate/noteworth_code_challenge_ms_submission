FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN mkdir /static
ADD requirements.txt /code/
RUN pip install uwsgi
RUN pip install -r requirements.txt
ADD ./noteworth_code_challenge /code/
RUN python manage.py collectstatic --noinput
