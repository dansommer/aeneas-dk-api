FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONIOENCODING=UTF-8

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ffmpeg \
        espeak \
        espeak-data \
        libespeak1 \
        libespeak-dev \
        festival \
        build-essential \
        flac \
        libasound2-dev \
        libsndfile1-dev \
        vorbis-tools \
        libxml2-dev \
        libxslt-dev \
        zlib1g-dev \
        python3 \
        python3-dev \
        python3-pip \
        git \
        file \
        unzip && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir \
        numpy \
        boto3 \
        requests \
        tgt \
        youtube-dl \
        Pillow \
        flask \
        gunicorn \
        aeneas

WORKDIR /app

COPY ./ /app/

EXPOSE 5000

CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-5000} app:app"]
