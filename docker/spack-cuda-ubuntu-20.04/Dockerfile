FROM nvidia/cuda:11.3.0-devel-ubuntu20.04
#MAINTAINER Spack Maintainers <maintainers@spack.io>

ENV DOCKERFILE_BASE=ubuntu            \
    DOCKERFILE_DISTRO=ubuntu          \
    DOCKERFILE_DISTRO_VERSION=20.04   \
    SPACK_ROOT=/opt/spack             \
    DEBIAN_FRONTEND=noninteractive    \
    CURRENTLY_BUILDING_DOCKER_IMAGE=1 \
    container=docker

RUN apt-get -yqq update \
    && apt-get -yqq install --no-install-recommends \
    build-essential \
    ca-certificates \
    curl \
    file \
    g++ \
    gcc \
    gfortran \
    git \
    gnupg2 \
    iproute2 \
    lmod \
    locales \
    lua-posix \
    make \
    python3 \
    python3-pip \
    python3-setuptools \
    tcl \
    unzip \
    && locale-gen en_US.UTF-8 \
    && pip3 install boto3 \
    && rm -rf /var/lib/apt/lists/*

RUN git clone --depth 1 -b v0.16.1 https://github.com/spack/spack $SPACK_ROOT

RUN ln -s $SPACK_ROOT/share/spack/docker/entrypoint.bash \
    /usr/local/bin/docker-shell \
    && ln -s $SPACK_ROOT/share/spack/docker/entrypoint.bash \
    /usr/local/bin/interactive-shell \
    && ln -s $SPACK_ROOT/share/spack/docker/entrypoint.bash \
    /usr/local/bin/spack-env

# Add LANG default to en_US.UTF-8
ENV LANGUAGE en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8

RUN mkdir -p /root/.spack \
    && cp $SPACK_ROOT/share/spack/docker/modules.yaml \
    /root/.spack/modules.yaml \
    && rm -rf /root/*.* /run/nologin $SPACK_ROOT/.git

WORKDIR /root
SHELL ["docker-shell"]

# # TODO: add a command to Spack that (re)creates the package cache
# RUN spack spec hdf5+mpi
RUN spack list > /dev/null

ENTRYPOINT ["/bin/bash", "/opt/spack/share/spack/docker/entrypoint.bash"]
CMD ["interactive-shell"]