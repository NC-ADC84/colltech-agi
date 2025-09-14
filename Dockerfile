FROM python:3.11-slim
ENV TZ=UTC LC_ALL=C LANG=C PYTHONHASHSEED=1337 OFFLINE=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y --no-install-recommends     build-essential jq git curl unzip ffmpeg     && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.in .
RUN python -m pip install --upgrade pip setuptools wheel && pip install -r requirements.in

COPY . .

# CollTech-AGI consciousness demonstration
RUN mkdir -p /app/out

ENTRYPOINT ["make", "all"]
