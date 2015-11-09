FROM alpine:3.2
MAINTAINER Charlie Lewis <clewis@iqt.org>

RUN apk add --update \
    python \
    py-pip \
    && rm -rf /var/cache/apk/*

ADD . /vent-control
RUN pip install -r /vent-control/requirements.txt
WORKDIR /vent-control
ENV PATH "$PATH":/vent-control
ENV VENT_CONTROL_DAEMON http://localhost:8080

EXPOSE 8080

ENTRYPOINT ["python", "vent-control"]
CMD ["daemon"]
