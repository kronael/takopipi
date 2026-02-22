FROM python:3.14-slim

RUN apt-get update -yy && \
  apt-get install -yy --no-install-recommends \
    ca-certificates curl git && \
  rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://deb.nodesource.com/setup_22.x \
    | bash - && \
  apt-get install -y nodejs && \
  rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv
RUN npm install -g @anthropic-ai/claude-code vite

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /srv/app

# install takopi from upstream
RUN uv venv /srv/app/.venv && \
  uv pip install --python /srv/app/.venv/bin/python \
    "takopi @ git+https://github.com/banteg/takopi.git@v0.22.1"

ENV PATH="/srv/app/.venv/bin:$PATH"

# install plugins
COPY plugins/takopi-reload/ /srv/plugins/takopi-reload/
COPY plugins/takopi-ship/ /srv/plugins/takopi-ship/
COPY plugins/takopi-info/ /srv/plugins/takopi-info/
COPY plugins/takopi-login/ /srv/plugins/takopi-login/
RUN cd /srv/plugins/takopi-reload && uv pip install -e . && \
  cd /srv/plugins/takopi-ship && uv pip install -e . && \
  cd /srv/plugins/takopi-info && uv pip install -e . && \
  cd /srv/plugins/takopi-login && uv pip install -e .

# seed template (survives volume overlay on cfg/)
COPY cfg/example/ ./seed/example/

COPY cfg/ ./cfg/
COPY takopipi ./takopipi
RUN chmod +x ./takopipi
