from debian:wheezy

RUN echo deb http://nginx.org/packages/debian/ wheezy nginx >>/etc/apt/sources.list
ADD nginx_signing.key /nginx_signing.key
RUN apt-key add nginx_signing.key
RUN apt-get update && apt-get -y upgrade

RUN apt-get install -y nginx

ADD nginx.conf /etc/nginx/nginx.conf
ADD start /start
ADD webroot /webroot

EXPOSE 80

CMD ["/start"]
