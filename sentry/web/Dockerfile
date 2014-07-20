FROM debian:wheezy

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get install -y python-pip
RUN apt-get install -y python-dev
RUN apt-get install -y libpq-dev

RUN pip install greenhouse datahog sentry==6.4.4

RUN mkdir /pythonpath
ENV PYTHONPATH /pythonpath

ADD sentry_config.py /sentry_config.py
ADD datahog_nodestore.py /pythonpath/datahog_nodestore.py

CMD ["/usr/local/bin/sentry", "--config=/sentry_config.py", "start"]
