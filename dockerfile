FROM python:3.7.13-slim-buster

# install base environment
RUN apt-get update && \
	apt-get install -y build-essential wget ca-certificates procps && \
	apt-get clean
RUN update-ca-certificates

# install python environment
COPY requirements.txt requirements.txt
RUN pip config set global.trusted-host "pypi.org pypi.python.org files.pythonhosted.org"
RUN python3 -m pip install -U pip setuptools wheel
RUN python3 -m pip install -r requirements.txt

# move source code into container
COPY /src /src
COPY .env .env
WORKDIR /src

# start the app and init shell
RUN chmod +x ./start_app.sh
CMD . ./start_app.sh && /bin/bash
