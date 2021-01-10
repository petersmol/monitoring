from python:3.9

MAINTAINER pub@petersmol.ru

COPY . /app
WORKDIR /app

RUN pip install pipenv
RUN pipenv install --system --deploy

CMD ["python", "-u", "run_consumer.py"]