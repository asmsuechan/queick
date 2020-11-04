FROM python:3

WORKDIR /tmp/queick
COPY . /tmp/queick

RUN python /tmp/queick/setup.py develop

CMD ["/bin/bash", "-c", "cd /tmp/queick/tests/integration && (queick &) && sleep 1 && python integration.py"]
