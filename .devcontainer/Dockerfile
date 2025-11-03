# syntax=docker/dockerfile:1
ARG UBUNTU_VERSION=22.04
ARG _DEV_CONTAINERS_BASE_IMAGE=dev_container_auto_added_stage_label
FROM ubuntu:${UBUNTU_VERSION}

# set apt mirror server
ARG APT_MIRROR=""
RUN [ "${APT_MIRROR:-}" != "" ] && sed -i -r "s@http://(\\w+.)?archive\.ubuntu\.com/ubuntu/@${APT_MIRROR}@" || :

# enable cache that apt keeps
RUN rm -f /etc/apt/apt.conf.d/docker-clean \
    && echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' >/etc/apt/apt.conf.d/keep-cache

# update ca-certificates
RUN --mount=type=cache,target=/var/lib/apt/lists,sharing=locked \
    --mount=type=cache,target=/var/cache/apt,sharing=locked \
    apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates

# japanize
RUN --mount=type=cache,target=/var/lib/apt/lists,sharing=locked \
    --mount=type=cache,target=/var/cache/apt,sharing=locked \
    apt-get update \
    && apt-get install -y --no-install-recommends \
        tzdata \
    && ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime \
    && echo 'Asia/Tokyo' >/etc/timezone \
    && apt-get install -y --no-install-recommends \
        language-pack-ja-base \
        language-pack-ja
ENV LANG=ja_JP.UTF-8

# create user
ARG USERNAME=vscode
RUN --mount=type=cache,target=/var/lib/apt/lists,sharing=locked \
    --mount=type=cache,target=/var/cache/apt,sharing=locked \
    apt-get update \
    && apt-get install -y --no-install-recommends \
        sudo \
    && groupadd --gid 5000 ${USERNAME} \
    && useradd --uid 5000 --gid 5000 --home-dir /home/${USERNAME} --create-home --shell /bin/bash ${USERNAME} \
    && echo "${USERNAME} ALL=(ALL) NOPASSWD:ALL" >>/etc/sudoers.d/${USERNAME} \
    && chmod 0440 /etc/sudoers.d/${USERNAME}

# persist bash history
RUN mkdir -p /home/${USERNAME}/.cache/bash \
    && touch /home/${USERNAME}/.cache/bash/.bash_history \
    && chown -R ${USERNAME}:${USERNAME} /home/${USERNAME}/.cache/bash \
    && ln -s /home/${USERNAME}/.cache/bash/.bash_history /home/${USERNAME}/.bash_history \
    && echo "export PROMPT_COMMAND='history -a'" >>/home/${USERNAME}/.bashrc

# persist vscode extensions
RUN mkdir -p /home/${USERNAME}/.vscode-server/extensions /home/${USERNAME}/.vscode-server-insiders \
    && chown -R ${USERNAME}:${USERNAME} /home/${USERNAME}/.vscode-server /home/${USERNAME}/.vscode-server-insiders \
    && ln -s /home/${USERNAME}/.vscode-server/extensions /home/${USERNAME}/.vscode-server-insiders/extensions

# install common dev tools
RUN --mount=type=cache,target=/var/lib/apt/lists,sharing=locked \
    --mount=type=cache,target=/var/cache/apt,sharing=locked \
    apt-get update \
    && apt-get install -y --no-install-recommends \
        bash-completion \
        curl \
        git \
        gnupg2 \
        iputils-ping \
        less \
        net-tools \
        tar \
        time \
        unzip \
        xz-utils \
        zip \
        openjdk-17-jre \
        wget

# install lefthook, gitleaks
ARG LEFTHOOK_VERSION=1.11.3
ARG GITLEAKS_VERSION=8.24.0
RUN --mount=type=cache,target=/var/lib/apt/lists,sharing=locked \
    --mount=type=cache,target=/var/cache/apt,sharing=locked \
    apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        gzip \
        tar \
        xz-utils \
    && curl -fsSL "https://github.com/evilmartians/lefthook/releases/download/v${LEFTHOOK_VERSION}/lefthook_${LEFTHOOK_VERSION}_Linux_$(uname -m).gz" \
        | gunzip > /usr/local/bin/lefthook \
    && chmod +x /usr/local/bin/lefthook \
    && curl -fsSL "https://github.com/gitleaks/gitleaks/releases/download/v${GITLEAKS_VERSION}/gitleaks_${GITLEAKS_VERSION}_linux_$(uname -m | sed 's/x86_64/x64/; s/aarch64/arm64/').tar.gz" \
        | tar xz -C /usr/local/bin gitleaks

# install node
RUN apt-get update && \
    apt-get install -y curl gettext-base && \
    curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && \
    apt-get install -y nodejs

# install PlantUML
RUN apt-get update && apt-get install -y wget graphviz fonts-noto-cjk && rm -rf /var/lib/apt/lists/* && \
    wget https://github.com/plantuml/plantuml/releases/latest/download/plantuml.jar \
        -O /usr/local/bin/plantuml.jar && \
    echo '#!/bin/sh' > /usr/local/bin/plantuml && \
    echo 'exec java -Dfile.encoding=UTF-8 -jar /usr/local/bin/plantuml.jar "$@"' >> /usr/local/bin/plantuml && \
    chmod 755 /usr/local/bin/plantuml && \
    ln -s /usr/local/bin/plantuml /usr/local/bin/puml

USER ${USERNAME}

# install uv
ARG UV_VERSION=0.8.17
RUN --mount=type=cache,target=/var/lib/apt/lists,sharing=locked \
    --mount=type=cache,target=/var/cache/apt,sharing=locked \
    sudo apt-get update \
    && sudo apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
    && curl -LsSf https://astral.sh/uv/${UV_VERSION}/install.sh | sh \
    && echo 'eval "$(uv generate-shell-completion bash)"' >> /home/${USERNAME}/.bashrc \
    && echo 'eval "$(uvx --generate-shell-completion bash)"' >> /home/${USERNAME}/.bashrc
ENV PATH=/home/${USERNAME}/.local/bin/:${PATH} \
    UV_NO_CACHE=1 \
    UV_LINK_MODE=copy

# install python
ARG PYTHON_VERSION=3.13.7
RUN uv python install ${PYTHON_VERSION} --default --preview
