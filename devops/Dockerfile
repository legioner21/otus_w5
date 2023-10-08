FROM python:3.10.0-alpine

WORKDIR /opt/project/app

ENV PYTHONBUFFERED=1
ENV TZ=Europe/Moscow

COPY scripts /opt/project/scripts
COPY requirements.txt /opt/project/requirements.txt

RUN chmod +x /opt/project/scripts/*.sh;
RUN /opt/project/scripts/install_packages.sh

COPY app /opt/project/app

EXPOSE 8000

CMD /opt/project/scripts/run.sh