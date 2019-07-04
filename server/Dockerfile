from debian:stretch

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get install -y gcc python3-pip git procps curl libpq-dev libffi-dev unzip build-essential

RUN curl -O https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py

RUN curl -O https://bitbucket.org/eradman/entr/get/1dc74ab543e2.zip
RUN unzip 1dc74ab543e2.zip && cd eradman-entr-1dc74ab543e2 && ./configure && make && make install

ADD requirements.txt /requirements.txt
RUN pip3 install -r requirements.txt

RUN mkdir vendor
WORKDIR vendor

RUN git clone git://github.com/teepark/greenhouse
RUN cd greenhouse; python3 setup.py install

RUN git clone git://github.com/cameron/datahog
RUN cd datahog; python3 setup.py install

RUN git clone git://github.com/cameron/databacon
RUN cd databacon/databacon; python3 setup.py install

ADD ./app /app
RUN touch /.reload

WORKDIR /
EXPOSE 80

CMD ls /.reload | entr -r python3 /app/routes.py
