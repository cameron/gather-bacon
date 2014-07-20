from debian:wheezy

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get install -y python-pip python-dev

RUN pip install whisper carbon

RUN sed -ri '/daemonize/d' /opt/graphite/lib/carbon/util.py

RUN /usr/sbin/useradd carbon

ADD carbon.conf /opt/graphite/conf/carbon.conf
ADD storage-schemas.conf /opt/graphite/conf/storage-schemas.conf
ADD start /start

EXPOSE 2003 2004

CMD ["/bin/bash", "/start"]
