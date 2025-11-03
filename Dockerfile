ARG UBUNTU_VERSION=22.04
FROM ubuntu:${UBUNTU_VERSION}

# update ca-certificates
RUN set -x \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
    && apt-get clean && rm -rf /var/cache/apt/archives/* /var/lib/apt/lists/*

# install PlantUML
RUN set -x \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        openjdk-17-jre \
        wget
RUN apt-get update && apt-get install -y wget graphviz fonts-noto-cjk && rm -rf /var/lib/apt/lists/* && \
    wget https://github.com/plantuml/plantuml/releases/latest/download/plantuml.jar \
        -O /usr/local/bin/plantuml.jar && \
    echo '#!/bin/sh' > /usr/local/bin/plantuml && \
    echo 'exec java -Dfile.encoding=UTF-8 -jar /usr/local/bin/plantuml.jar "$@"' >> /usr/local/bin/plantuml && \
    chmod 755 /usr/local/bin/plantuml && \
    ln -s /usr/local/bin/plantuml /usr/local/bin/puml

# install uv
ARG UV_VERSION=0.8.17
RUN set -x \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
    && curl -LsSf https://astral.sh/uv/${UV_VERSION}/install.sh | sh \
    && apt-get clean && rm -rf /var/cache/apt/archives/* /var/lib/apt/lists/*
ENV PATH=/root/.local/bin/:${PATH} \
    UV_NO_CACHE=1 \
    UV_LINK_MODE=copy

WORKDIR /workdir

COPY . .

RUN set -x \
    && uv sync

ENTRYPOINT ["uv", "run", "src/main.py"]
