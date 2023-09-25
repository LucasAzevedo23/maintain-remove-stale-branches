FROM python:3.12-rc

WORKDIR /usr/src

COPY main.py main.py
COPY requirements.txt requirements.txt

RUN apt-get update -y &&\
    apt-get upgrade -y &&\
    pip install -r requirements.txt

ENTRYPOINT [ "python3", "/usr/src/main.py" ]