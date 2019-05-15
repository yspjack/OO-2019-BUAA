FROM ubuntu:18.04
RUN sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list \
    && sed -i 's/security.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list \
    && apt-get update \
    && apt-get -y --no-install-recommends install python3-pip openjdk-8-jdk-headless \
    && rm -rf /var/lib/apt/lists/*
RUN pip3 install -i https://mirrors.aliyun.com/pypi/simple --no-cache-dir numpy
