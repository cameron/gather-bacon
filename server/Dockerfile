from debian:wheezy

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get install -y gcc python-dev python-pip git procps curl libpq-dev libffi-dev

ADD requirements.txt /requirements.txt
RUN pip install -r requirements.txt

RUN mkdir vendor
WORKDIR vendor

RUN git clone https://github.com/teepark/greenhouse
RUN cd greenhouse; python setup.py install

RUN git clone https://github.com/teepark/datahog
RUN cd datahog; python setup.py install

RUN git clone https://github.com/cameron/databacon
RUN cd databacon/databacon; python setup.py install

ADD ./src /app

EXPOSE 8000

CMD ["/app/routes.py"]
