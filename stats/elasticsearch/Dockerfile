from debian:wheezy

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y wget openjdk-7-jre

RUN wget --no-check-certificate https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.1.0.tar.gz -O /tmp/es.tgz
RUN tar xzf /tmp/es.tgz -C / && mv /elasticsearch-1.1.0 /elasticsearch

EXPOSE 9200

CMD ["/bin/sh", "/elasticsearch/bin/elasticsearch"]
