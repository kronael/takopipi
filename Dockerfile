FROM python:3.14-slim

RUN apt-get update -yy && \
  apt-get install -yy --no-install-recommends \
    ca-certificates curl git && \
  rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://deb.nodesource.com/setup_22.x \
    | bash - && \
  apt-get install -y nodejs && \
  rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
RUN npm install -g @anthropic-ai/claude-code vite

ENV PATH="/root/.local/bin:/root/.cargo/bin:$PATH"

WORKDIR /srv/app

# install takopi from upstream
RUN uv venv /srv/app/.venv && \
  uv pip install --python /srv/app/.venv/bin/python \
    "takopi @ git+https://github.com/banteg/takopi.git@v0.22.1"

ENV PATH="/srv/app/.venv/bin:$PATH"

# install plugins
COPY plugins/ /srv/plugins/
RUN for p in /srv/plugins/*/; do \
    uv pip install -e "$p"; \
  done

# seed template (survives volume overlay on /cfg/)
COPY template/ /srv/app/template/

COPY cfg/ /cfg/
COPY takopipi ./takopipi
RUN chmod +x ./takopipi
