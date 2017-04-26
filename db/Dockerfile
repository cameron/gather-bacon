FROM debian:wheezy

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get -y install wget

ADD pgapt.list /etc/apt/sources.list.d/pgapt.list
RUN wget -O - http://apt.postgresql.org/pub/repos/apt/ACCC4CF8.asc | apt-key add -
RUN apt-get -y update && apt-get -y upgrade && apt-get install -y postgresql-9.3 postgresql-contrib-9.3

ADD start /start
ADD shard.up.sql /shard.up.sql

EXPOSE 5432

CMD ["/bin/sh", "/start"]
