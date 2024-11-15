FROM mcr.microsoft.com/devcontainers/base:alpine
USER root
RUN apk add npm python3 ruff && \
    apk add uv --repository=https://dl-cdn.alpinelinux.org/alpine/edge/community
USER vscode