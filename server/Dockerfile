from debian:wheezy

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get install -y gcc python-dev python-pip git procps curl libpq-dev libffi-dev unzip

RUN curl -O https://bitbucket.org/eradman/entr/get/1dc74ab543e2.zip
RUN unzip 1dc74ab543e2.zip && cd eradman-entr-1dc74ab543e2 && ./configure && make && make install

ADD requirements.txt /requirements.txt
RUN pip install -r requirements.txt

RUN mkdir vendor
WORKDIR vendor

RUN git clone https://github.com/teepark/greenhouse
RUN cd greenhouse; python setup.py install

RUN git clone https://github.com/cameron/datahog
RUN cd datahog; python setup.py install

RUN git clone https://github.com/cameron/databacon
RUN cd databacon/databacon; python setup.py install

ADD ./app /app
RUN touch /.reload

WORKDIR /
EXPOSE 80

CMD ls /.reload | entr -r python /app/routes.py
