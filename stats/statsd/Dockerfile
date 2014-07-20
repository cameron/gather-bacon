from debian:wheezy

RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y make gcc python g++ checkinstall wget

RUN wget http://nodejs.org/dist/node-latest.tar.gz -O /tmp/nodebuild
RUN tar xzf /tmp/nodebuild -C /tmp
RUN cd /tmp/node-* && chmod +x configure && ./configure
RUN cd /tmp/node-* && checkinstall -y --install=no --pkgversion 0.11.11 make -j$(($(nproc)+1)) install
RUN dpkg -i /tmp/node-*/node_*

RUN npm install statsd

ADD start /start
ADD config.js /node_modules/statsd/config.js

EXPOSE 8125/udp

CMD ["/bin/bash", "/start"]
