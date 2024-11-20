FROM mcr.microsoft.com/devcontainers/base:alpine
USER root
RUN apk add gcc linux-headers musl-dev npm python3 python3-dev ruff && \
    apk add uv --repository=https://dl-cdn.alpinelinux.org/alpine/edge/community
USER vscode