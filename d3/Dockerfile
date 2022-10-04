FROM ghcr.io/flux-framework/flux-core-ubuntu:latest

# I'm rebuilding here because it was compiled without python unfortunately!
# docker build -t flux-vis .

RUN apt-get update \
 && apt-get -qq install -y --no-install-recommends \
        automake \
        libsodium-dev \
        libzmq3-dev \
        libczmq-dev \
        libjansson-dev \
        libmunge-dev \
        libncursesw5-dev \
        lua5.4 \
        liblua5.4-dev \
        liblz4-dev \
        libsqlite3-dev \
        uuid-dev \
        libhwloc-dev \
        libmpich-dev \
        libs3-dev \
        libevent-dev \
        libarchive-dev \
        python3 \
        python3-dev \
        python3-pip \
        python3-sphinx \
        libtool \
        git \
        vim \
        build-essential && \
        ldconfig && \
        rm -rf /var/lib/apt/lists/*

WORKDIR /code

RUN python3 -m pip install cffi pyaml jsonschema IPython

# rebuild with python
RUN ./autogen.sh && \
    ./configure --prefix=/usr/local && \
    make && \
    make install && \
    ldconfig

# Ensure we can find Python
RUN ln -s /usr/bin/python3 /usr/bin/python
COPY ./example.py ./example.py
COPY ./entrypoint.sh /entrypoint.sh
ENTRYPOINT ["flux", "start", "/bin/bash", "/entrypoint.sh"]
