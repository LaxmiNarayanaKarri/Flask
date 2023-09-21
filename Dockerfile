FROM python:3.9.13


WORKDIR /app


COPY ./requirements.txt ./
RUN pip install -r requirements.txt


COPY . /app

EXPOSE 5000

ENV FLASK_APP=run.py

ENV FLASK_DEBUG=true
ENV FLASK_ENV=development


CMD python ./run.py