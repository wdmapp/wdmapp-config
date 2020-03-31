
Setting up Spack
*****************

Setting up Spack on a given machine should be a one-time process, and
ideally shouldn't be specific to the codes you're planning to build.

.. note::

   In practice you might want to set up multiple compilers etc, and
   then have certain projects build using some specific compiler, and
   so on. Spack allows you to specify details like this when
   installating a package, but it might be useful to use Spack
   environments so that you don't have to remember to keep specifying
   those details over and over again.

Installing Spack
======================

Follow the instructions from the `Spack Documentation 
<http://https://spack.readthedocs.io/en/latest/getting_started.html/>`_.

.. code-block:: sh

   $ git clone -b releases/v0.14 https://github.com/spack/spack.git
   
.. note::

   v0.14 is the latest spack stable version on 2020-03-17; newer versions
   will likely work but have not been tested. Using the default 'develop'
   branch is not recommended, as it does break sometimes and introduces
   a lot of package version churn if you try to track it.

Enable shell support for Spack.

.. code-block:: sh

  # For bash/zsh users
  $ export SPACK_ROOT=/path/to/spack
  $ . $SPACK_ROOT/share/spack/setup-env.sh

  # For tcsh or csh users (note you must set SPACK_ROOT)
  $ setenv SPACK_ROOT /path/to/spack
  $ source $SPACK_ROOT/share/spack/setup-env.csh

Cloning the ``WDMapp-config`` repository
========================================

Just clone the repository from `github
<https://github.com/wdmapp/wdmapp-config/>`_ to the same machine that
you just set up Spack on.

.. code-block:: sh

   $ git clone https://github.com/wdmapp/wdmapp-config
   


Adding the WDMapp package repo to Spack
=============================================

This will let Spack search the WDMapp repository for packages that
aren't found in its builtin package repository.

.. code-block:: sh

  $ spack repo add path/to/wdmapp-config/spack/wdmapp
  ==> Added repo with namespace 'wdmapp'.

.. note::

  To update the wdmapp package repository to the latest, just run ``git
  pull`` in the directory where you cloned ``wdmapp-config/``.

Machine-Specific Setup
======================

OLCF Summit
---------------------

Copy a basic setup for Spack on Summit from the `wdmapp-config
<https://github.com/wdmapp/wdmapp-config/>`_ repository.

.. code-block:: sh

  $ mkdir -p ~/.spack/linux		
  $ cp path/to/wdmapp-config/spack/configs/summit/* ~/.spack/linux/

.. warning::
   This will overwrite an existing Spack configuration, so be careful
   if you've previously set Spack up. If you have existing config, consider
   using path/to/spack/etc/spack/package.yaml for packages instead, and add
   gcc 8.1.1 to your exising compilers.yaml if not already present.

Consider also configuring spack to use gpfs scratch space (i.e. `$MEMBERWORK`)
when building packages, rather than the home filesystem which tends to have
problems with high workload tasks:

.. code-block:: sh

  $ mkdir -p /gpfs/alpine/scratch/$USER/spack-stage

and add the following to `~/.spack/config.yaml`:

.. code-block:: yaml

  config:
    build_stage: /gpfs/alpine/scratch/$user/spack-stage
   
.. note::

   On Summit, the cuda module sets environment variables that set a
   path which nvcc does not otherwise add. Because of this, it is
   requried to `module load cuda/10.1.243` before building GENE, and
   probably other software that uses CUDA..

TACC longhorn
---------------------

Longhorn is currentlt pretty bare bones in terms of software
installed, but with some patience, Spack will install most things for
you.

The following describes how to use the installed openmpi 3.1.2 + gcc
7.3.0.

Using provided basic longhorn setup
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  
Copy a basic setup for Spack on Longhorn from the `wdmapp-config
<https://github.com/wdmapp/wdmapp-config/>`_ repository.

.. code-block:: sh

  $ mkdir -p ~/.spack/linux		
  $ cp path/to/wdmapp-config/spack/configs/longhorn/* ~/.spack/linux/

.. warning::
   This will overwrite an existing Spack configuration, so be careful
   if you've previously set Spack up. If you have existing config, consider
   using path/to/spack/etc/spack/package.yaml for packages instead, and add
   gcc 7.3.0 to your exising compilers.yaml if not already present.


Creating your own setup
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

 Alternatively, you can create your own config:

 .. code-block:: sh

  module load gcc/7.3.0
  spack compiler find

This should find a number of compilers, including gcc 7.3.0. You may
want to repeat this step for gcc 9.1.0 -- however, there is currently
no preinstalled MPI for this compiler.

he compilers on longhorn require LD_LIBRARY_PATH hackery to function, and spack sanitizes LD_LIBRARY_PATH. The workaround is described here. In this case, edit ``~/.spack/linux/compilers.yaml``:

spack config edit compilers
and modify the modules section for gcc 7 like this:


.. code-block:: yaml

   - compiler:
      spec: gcc@7.3.0
      paths:
        cc: /opt/apps/gcc/7.3.0/bin/gcc
        cxx: /opt/apps/gcc/7.3.0/bin/g++
        f77: /opt/apps/gcc/7.3.0/bin/gfortran
        fc: /opt/apps/gcc/7.3.0/bin/gfortran
      flags: {}
      operating_system: rhel7
      target: ppc64le
      modules: [gcc/7.3.0] # <-- ADD THIS
      environment: {}
      extra_rpaths: []

    similar is required for gcc/9.1.0, and possibly for xl.

Add a minimal ``packages.yaml`` in ``~/.spack/linux/packages.yaml`` that
registers the preinstalled openmpi and cuda modules:

.. code-block:: yaml

   packages:
     openmpi:
       variants: +cuda fabrics=verbs
       buildable: false
       version: []
       target: []
       compiler: []
       providers: {}
       paths:
         openmpi@3.1.2%gcc@7.3.0: /opt/apps/gcc7_3/openmpi/3.1.2
       modules: {}

     cuda:
       modules:
         cuda@10.1: cuda/10.1
       buildable: false
       version: []
       target: []
       compiler: []
       providers: {}
       paths: {}

   all:
       providers:
         mpi: [openmpi]
         blas: [netlib-lapack]
         lapack: [netlib-lapack]


The last section above sets defaults for all packages you'll
installing with Spack -- you might want to adjust those, or move them
to an environment.

Running a job on longhorn
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. warning::

   The pre-installed openmpi on longhorn seems to have issues with
   infiniband. In order to not have GENE hang, one has to pass ``--mca
   btl tcp,self`` and maybe also ``--mca pml ob1`` to ``mpirun``.

Fixing ``config.guess`` on longhorn
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Spack has logic that will replace an outdated ``config.guess`` in a
given package with a newer version -- which comes in handy, because
apparently the latest autoconf version is from 2012 and the
``config.guess`` that comes with it doesn't know about
``ppc64le``. However, on longhorn, Spack will not find a newer
``config.guess`` in ``/usr/share/automake*/`` , hence things still
don't work. To work around this, I hacked Spack like this:

.. code-block:: diff

  diff --git a/lib/spack/spack/build_systems/autotools.py b/lib/spack/spack/build_systems/autotools.py
  index c21b8dad7..f8e8f64fe 100644
  --- a/lib/spack/spack/build_systems/autotools.py
  +++ b/lib/spack/spack/build_systems/autotools.py
  @@ -133,11 +133,12 @@ def _do_patch_config_guess(self):
               if os.path.exists(path):
                   config_guess = path
           # Look for the system's config.guess
  -        if config_guess is None and os.path.exists('/usr/share'):
  -            automake_dir = [s for s in os.listdir('/usr/share') if
  +        path_am = '/opt/apps/autotools/1.2/share'
  +        if config_guess is None and os.path.exists(path_am):
  +            automake_dir = [s for s in os.listdir(path_am) if
                               "automake" in s]
               if automake_dir:
  -                automake_path = os.path.join('/usr/share', automake_dir[0])
  +                automake_path = os.path.join(path_am, automake_dir[0])
                   path = os.path.join(automake_path, 'config.guess')
                   if os.path.exists(path):
                       config_guess = path

Ubuntu 18.04
---------------------

On Ubuntu 18.04, nothing special needs to be done, though installation
can be sped up by adding a ``packages.yaml`` that teaches it about
system-installed software so that it doesn't have to build everything
from scratch.


