# get newer version of docker with ubuntu rather than alpine
FROM ubuntu:14.04.2
MAINTAINER Charlie Lewis <clewis@iqt.org>

RUN apt-get update && apt-get install -qqy \
    apt-transport-https \
    ca-certificates \
    curl \
    iptables \
    lxc \
    python-pip \
    unzip

RUN curl -sSL https://get.docker.com/ | sh

# hacks for vmware driver
RUN curl -L https://github.com/vmware/govmomi/releases/download/v0.2.0/govc_linux_amd64.gz >govc.gz && gzip -d govc.gz && mv govc /usr/local/bin/govc
RUN chmod +x /usr/local/bin/govc
RUN curl -L https://github.com/boot2docker/boot2docker/releases/download/v1.9.0/boot2docker.iso >boot2docker.iso && mkdir -p /root/.docker/machine/ && mv boot2docker.iso /root/.docker/machine/boot2docker.iso

RUN curl -L https://github.com/docker/machine/releases/download/v0.5.0/docker-machine_linux-amd64.zip >machine.zip && \
    unzip machine.zip && \
    rm machine.zip && \
    mv docker-machine* /usr/local/bin

ADD ./wrapdocker /usr/local/bin/wrapdocker
RUN chmod +x /usr/local/bin/wrapdocker
ADD . /vent-control
RUN pip install -r /vent-control/requirements.txt
WORKDIR /vent-control
VOLUME /var/lib/docker
VOLUME /root/.docker
ENV PATH "$PATH":/vent-control
ENV VENT_CONTROL_DAEMON http://localhost:8080

EXPOSE 8080

ENTRYPOINT ["python", "vent-control"]
CMD ["daemon"]
