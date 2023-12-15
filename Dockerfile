FROM python:3.12.0
LABEL Name=jukwaa Version=1.0

RUN mkdir /jukwaa
WORKDIR /jukwaa
ADD requirements.txt /jukwaa/
RUN pip install -r requirements.txt
EXPOSE 8005

