FROM ubuntu:16.04
MAINTAINER clewis@iqt.org

ENV DEBIAN_FRONTEND noninteractive

# hack for installing openjdk-7-jre refrenced from http://askubuntu.com/questions/759451/how-can-i-install-openjdk-on-ubuntu-16-04
RUN apt-get update && \
    apt-get install -y git npm nodejs software-properties-common && \
    add-apt-repository ppa:openjdk-r/ppa && \
    apt-get update && \
    apt-get install -y openjdk-7-jre
RUN ln -s /usr/bin/nodejs /usr/local/bin/node

RUN git clone https://github.com/swagger-api/swagger-ui.git
WORKDIR /swagger-ui
RUN git checkout tags/v2.1.4
RUN npm install
EXPOSE 8080
ADD index.html /swagger-ui/dist/index.html
ADD swagger-ui.js /swagger-ui/dist/swagger-ui.js
CMD ./node_modules/gulp/bin/gulp.js serve
