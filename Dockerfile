ARG http_proxy=http://irproxy.ifpen.fr:8082
ARG https_proxy=http://irproxy.ifpen.fr:8082
ARG ftp_proxy=http://irproxy.ifpen.fr:8082
ARG ftps_proxy=http://irproxy.ifpen.fr:8082
ARG no_proxy=.ifp.fr,.ifpen.fr,localhost,127.0.0.1

FROM harbor.ifpen.fr/ifpen/arcaneframework/ifpen/docker-official-latest/python:3.11

##############################
### Configure Repositories ###
##############################

RUN sed -e 's,http://archive.ubuntu.com/,https://repos.ifpen.fr/repository/ubuntu_update/,g' \
        -e 's,http://security.ubuntu.com/,https://repos.ifpen.fr/repository/ubuntu_update/,g' 
        #-i /etc/apt/sources.list

RUN apt-get -o Acquire::https::repos.ifpen.fr::Verify-Peer=false -o Acquire::https::repos.ifpen.fr::Verify-Host=false update && \
    apt-get -o Acquire::https::repos.ifpen.fr::Verify-Peer=false -o Acquire::https::repos.ifpen.fr::Verify-Host=false install -y ca-certificates

########################
### Install packages ###
########################

RUN apt-get update && DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get install -y \
    python3 \
    python3-pip \
    python3-opencv \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

ARG PASSWORD
RUN pip install git+https://lecomtje:$PASSWORD@gitlab.ifpen.fr/tellus/andra/ai.calcimetry.git@wip_v_1_0

RUN mkdir /app
COPY flask/ /app/
WORKDIR /app

EXPOSE 5000

CMD [ "gunicorn", "-b 0.0.0.0:5000", "flaskapp:app"]







