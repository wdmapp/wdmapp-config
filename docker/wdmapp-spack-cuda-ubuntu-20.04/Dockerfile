
ARG VARIANT="ubuntu-20.04"
FROM ghcr.io/wdmapp/spack-cuda-${VARIANT}:latest

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    libopenmpi-dev ninja-build \
    apt-transport-https ca-certificates gnupg software-properties-common wget \
    libhdf5-openmpi-dev \
    libssl-dev \
    libbz2-dev liblz4-dev libfabric-dev libffi-dev libsodium-dev \
    libpkgconf-dev libzstd-dev libzmq3-dev zlib1g-dev \
    libpng-dev libblosc-dev libsnappy-dev \
    silversearcher-ag vim less \
    && rm -rf /var/lib/apt/lists/*

RUN wget -O - https://apt.kitware.com/keys/kitware-archive-latest.asc  \
    | gpg --dearmor - > /etc/apt/trusted.gpg.d/kitware.gpg \
    && apt-add-repository 'deb https://apt.kitware.com/ubuntu/ focal main' \
    && apt-get update \
    && apt-get -y install --no-install-recommends cmake \
    && rm -rf /var/lib/apt/lists/*

RUN spack config --scope system add "packages:all:target: [haswell]" \
    && spack external find --scope system && \
    echo "  libfabric: {externals: [{spec: libfabric@1.6.2, prefix: /usr}]}" >> /etc/spack/packages.yaml && \
    echo "  lz4: {externals: [{spec: lz4@1.9.2, prefix: /usr}]}" >> /etc/spack/packages.yaml && \
    echo "  libffi: {externals: [{spec: libffi@3.3, prefix: /usr}]}" >> /etc/spack/packages.yaml && \
    echo "  pkgconf: {externals: [{spec: pkgconf@1.6.3, prefix: /usr}]}" >> /etc/spack/packages.yaml && \
    echo "  zstd: {externals: [{spec: zstd@1.4.4, prefix: /usr}]}" >> /etc/spack/packages.yaml && \
    echo "  zlib: {externals: [{spec: zlib@1.2.11, prefix: /usr}]}" >> /etc/spack/packages.yaml && \
    echo "  libzmq: {externals: [{spec: libzmq@4.1.2, prefix: /usr}]}" >> /etc/spack/packages.yaml && \
    echo "  libpng: {externals: [{spec: libpng@1.6.37, prefix: /usr}]}" >> /etc/spack/packages.yaml && \
    echo "  c-blosc: {externals: [{spec: c-blosc@1.17.1, prefix: /usr}]}" >> /etc/spack/packages.yaml && \
    echo "  snappy: {externals: [{spec: snappy@1.1.8, prefix: /usr}]}" >> /etc/spack/packages.yaml && \
    echo "  hdf5: {externals: [{spec: hdf5@1.10.4 +hl, prefix: /usr}]}" >> /etc/spack/packages.yaml && \
    echo "  libsodium: {externals: [{spec: libsodium@1.0.17, prefix: /usr}]}" >> /etc/spack/packages.yaml

#    echo "  sz: {externals: [{spec: sz@1.0.4, prefix: /usr}]}" >> /etc/spack/packages.yaml && \

RUN spack env create -d wdmapp-env && \
    spack env activate wdmapp-env && spack add adios2 \
    && spack install && spack clean -a

COPY spack/ spack

RUN spack repo add --scope system spack/wdmapp

RUN spack env activate wdmapp-env \
    && spack add cuda thrust \
    && spack install && spack clean -a

