from debian:wheezy

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get install -y gcc python-dev python-pip git procps curl libpq-dev

RUN git clone https://github.com/teepark/shorty
RUN cd shorty; python setup.py install

RUN git clone https://github.com/teepark/feather
RUN cd feather; python setup.py install

RUN git clone https://github.com/teepark/datahog
RUN cd datahog; python setup.py install

RUN /usr/sbin/useradd legalease

ADD requirements.txt /requirements.txt
RUN pip install -r requirements.txt

ADD ./bin /srv/bin
ADD ./src /srv/app

EXPOSE 80

CMD ["/srv/bin/start", "-w", "-p", "80", "-u", "legalease", "-g", "legalease"]
