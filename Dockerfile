FROM ubuntu:16.04
MAINTAINER Erik Leen "erik.leven@sesam.io"
COPY ./service /service

RUN apt-get update
RUN apt-get install -y build-essential
RUN apt-get install -y python3
RUN apt-get install -y python3-dev
RUN apt-get install -y curl
RUN apt-get install -y libssl-dev

RUN curl -sSL https://bootstrap.pypa.io/get-pip.py | python3

RUN pip3 install --upgrade pip

RUN pip3 install -r /service/requirements.txt

CMD ["python3", "-u", "./service/netcompany-ms.py"]
