
WDMApp on AiMOS
*****************************

AiMOS is a 268 node IBM AC922 system with 2x IBM P9 and 6x NVIDIA V100 GPUs with
32GiB of memory each.  More info is available on the AiMOS wiki:

`<https://secure.cci.rpi.edu/wiki/index.php?title=DCS_Supercomputer>`_

Github access requires setting up the http(s) proxy 

`<https://secure.cci.rpi.edu/wiki/index.php?title=Proxy>`_

and you'll need to create an ssh key-pair for running MPI jobs

.. code-block:: sh

  $ ssh-keygen # accept defaults

.. warning::

   This will overwrite an existing ``id_rsa`` key pair.


Manual Install For Coupler Developers
==========================================

XGC-Devel
-------------------------

Clone the repo

.. code-block:: sh

  $ git clone https://github.com/wdmapp/XGC-Devel.git
  $ cd XGC-Devel
  $ git checkout rpi

Create a environment file with the following contents named
``envAimosGcc74OpenMPI.sh``.

.. code-block:: sh

  module use /gpfs/u/software/dcs-spack-install/v0133gcc/lmod/linux-rhel7-ppc64le/gcc/7.4.0-1/
  module load gcc/7.4.0/1 openmpi/3.1.4-mm5hjuq cmake/3.15.4-mnqjvz6
  module load \
    adios/1.13.1-ev2p4am \
    adios2/2.5.0-mklg6ph \
    petsc/3.7.7-int32-hdf5+ftn-real-c-7ewou4w \
    fftw/3.3.8-b2oxdb5 \
    pkg-config/system-cyeqmxc


``source`` the environment file

.. code-block:: sh

  $ source envAimosGcc74OpenMPI.sh

Create a build directory ``build-xgcDevel-aimosGcc74OpenMPI``, ``cd`` into it,
and run ``CMake``:

.. code-block:: sh

  $ mkdir build-xgcDevel-aimosGcc74OpenMPI
  $ cd !$
  $ # specify the path to the XGC-Devel repo
  $ cmake /path/to/xgc-devel/repo \
    -DCMAKE_CXX_COMPILER=g++ \
    -DCMAKE_C_COMPILER=gcc \
    -DCMAKE_Fortran_COMPILER=gfortran \
    -DXGC_USE_ADIOS1=ON \
    -DXGC_USE_ADIOS2=OFF \
    -DXGC_USE_CABANA=OFF \
    -DUSE_SYSTEM_PSPLINE=OFF \
    -DXGC_GENE_COUPLING=ON \
    -DBUILD_TESTING=OFF \
    -DCMAKE_INSTALL_PREFIX=$PWD/install


Run ``make`` to compile and link XGC:

.. code-block:: sh

  $ make -j8

If all goes well the xgc binary will be created; ``bin/xgc-es-cpp``.


GENE
-------------------------

Clone the repo

.. code-block:: sh

  $ git clone https://github.com/wdmapp/gene.git
  $ git checkout rpi

Create a environment file with the following contents named
``envAimosGcc74OpenMPI.sh``.

.. code-block:: sh

  module use /gpfs/u/software/dcs-spack-install/v0133gcc/lmod/linux-rhel7-ppc64le/gcc/7.4.0-1/
  module load gcc/7.4.0/1
  module load openmpi/3.1.4-mm5hjuq
  module load \
    cmake/3.15.4-mnqjvz6 \
    adios/1.13.1-zrrxpbi \
    adios2/2.5.0-rqsvxj4 \
    fftw/3.3.8-b2oxdb5 \
    netlib-scalapack/2.0.2-7bndnga \
    openblas/0.3.7-x7m3b6w \
    zlib/1.2.11-lpgvqh7 \
    hdf5/1.10.3-ftn-tgragps 

  export OMPI_CXX=g++
  export OMPI_CC=gcc
  export OMPI_FC=gfortran 

``source`` the environment file

.. code-block:: sh

  $ source envAimosGcc74OpenMPI.sh

Create a build directory ``build-gene-aimosGcc74OpenMPI``, ``cd`` into it,
and run ``CMake``:

.. code-block:: sh

  $ mkdir build-gene-aimosGcc74OpenMPI
  $ cd !$
  $ # specify the path to the gene repo
  $ cmake /path/to/gene/repo \
    -DCMAKE_Fortran_COMPILER=gfortran \
    -DCMAKE_CXX_COMPILER=g++ \
    -DCMAKE_C_COMPILER=gcc \
    -DGENE_USE_FUTILS=on \
    -DGENE_USE_ADIOS2=on \
    -DGENE_DIAG_PLANES=on \
    -DGENE_PERF=none \
    -DGENE_WDMAPP=on


Run ``make`` to compile and link GENE:

.. code-block:: sh

  $ make -j8

If all goes well the gene binary will be created; ``src/gene``.

Run
-------------------------

Clone the testcases repo (https://github.com/wdmapp/testcases) then follow the instructions in `run_1/README.md`:

https://github.com/wdmapp/testcases/blob/master/run_1/README.md

