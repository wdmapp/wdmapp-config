
.. _build-wdmapp-label:

Building WDMAPP
***********************

.. todo:: The develop instructions
	  should possibly move elsewhere.


.. note ::

   In order to install the non-public packages, one must 
   `upload their SSH keys to GitHub <https://help.github.com/en/enterprise/2.15/user/articles/adding-a-new-ssh-key-to-your-github-account>`_.


Standard Installation
===========================

Building WDMapp can be done following the standard Spack way:

.. code-block:: sh

  $ spack install wdmapp

Then, have a coffee and keep your fingers crossed.

The `wdmapp` packages is a metapackage ("BundlePackage" in Spack
parlance) that pulls in proper versions and variants of GENE, XGC, the
Coupler and TAU and all their dependencies to have everything in place
to run a coupled simulation:

.. code-block:: sh

  $ spack spec wdmapp
  Input spec
  --------------------------------
  wdmapp

  Concretized
  --------------------------------
  wdmapp@0.0.1%gcc@7.5.0+tau~xgc1_legacy arch=linux-ubuntu18.04-haswell
      ^coupler@master%gcc@7.5.0 build_type=RelWithDebInfo arch=linux-ubuntu18.04-haswell
      ^gene@coupling%gcc@7.5.0+adios2 build_type=RelWithDebInfo ~cuda cuda_arch=none +diag_planes+futils perf=perfstubs +pfunit+wdmapp arch=linux-ubuntu18.04-haswell
      ^tau@develop%gcc@7.5.0+adios2~bgq+binutils~comm~craycnl~cuda+fortran~gasnet+io+libdwarf+libelf~libunwind~likwid+mpi~ompt~opari~openmp+otf2+papi~pdt~phase~ppc64le~profilepa
      ^xgc-devel@wdmapp%gcc@7.5.0~adios2 build_type=RelWithDebInfo ~cabana+coupling_core_edge_gene arch=linux-ubuntu18.04-haswell

Then install effis:

.. code-block:: sh

  $ spack install effis

Installing for development
===============================

.. note ::

   The following describes how to do development builds of gene (XGC
   can be done correspondingly) using `spack setup`. This way appears
   to be deprecated in favor of `spack dev-build`. It does work, but
   requires some workarounds and can subtly vary from how things are
   built using `spack install` or `spack dev-build`.

Most of the time, one needs to be able to specify the exact version of the code, make changes, etc. Spack can still help with development.

First of all, get a local clone of the git repository for, e.g., GENE. You probably already have one, so you can use that. Otherwise:

.. code-block:: sh

  $ git clone git@gitlab.mpcdf.mpg.de:GENE/gene-dev.git
  $ git checkout cuda_under_the_hood

The method described here relies on the cmake build of GENE, though you could choose to just use Spack to install dependencies for you, and then handle things manually as usual.

Next, create a build director and change into it:

.. code-block:: sh

  $ cd gene-dev
  $ mkdir build
  $ cd build

Now, have Spack set up the build for you -- but not actually do it:

.. code-block:: sh

  $ spack setup gene@local
  [...]
  ==> Generating spconfig.py 
  
.. note::

   Something is currently broken with Spack, which likely gives you ``Error: 'SPACK_DEPENDENCIES'``. If that happens, you can work around it by setting ``export SPACK_DEPENDENCIES=""`` and trying agian.

The ``spack setup`` will install all required dependencies, and then creates ``spconfig.py`` file in the current directory. This script can be used as a replacement to the usual invocation of cmake.

.. code-block:: sh

  $ ./spconfig.py .. # .. is the path to the sources
  [...]
  -- Generating done
  -- Build files have been written to: /home/src/gene-dev/build

So then you're all set. Just call ``make``.

.. code-block:: sh

  $ make -j20
  [...]


.. todo::

  pfunit should depend on ``python`` being available at runtime, but it looks like it does not.
