from debian:wheezy

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get install -y python-pip python-dev
RUN apt-get install -y libffi-dev libcairo2-dev

RUN pip install graphite-api feather-http

RUN /usr/sbin/useradd graphiteapi

ADD acaowrap.py /acaowrap.py
ENV PYTHONPATH /

EXPOSE 8000

CMD ["/usr/local/bin/featherctl", "start", "-u", "graphiteapi", "-g", "graphiteapi", "-f", "acaowrap:app"]
