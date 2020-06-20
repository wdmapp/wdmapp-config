
WDMapp on Longhorn at TACC
*************************************

Setting up Spack
====================

Follow the generic instructions from  :ref:`setup-spack-label` to install Spack and add the
WDMapp Spack package repository.

.. todo:: adopt the following for longhorn

Using Provided Basic Spack Setup for Longhorn
----------------------------------------------
	  
Longhorn is currentlt pretty bare bones in terms of software
installed, but with some patience, Spack will install most things for
you.

The following describes how to use the pre-installed openmpi 3.1.2 + gcc
7.3.0.

You can copy your choice of a basic or a more comprehensive setup for
Spack on Longhorn from the
`<https://github.com/wdmapp/wdmapp-config/tree/master/longhorn/spack>`_ repository.
 
.. code-block:: sh

  $ mkdir -p ~/.spack/linux		
  $ cp path/to/wdmapp-config/longhorn/spack/*.yaml ~/.spack/linux/

.. warning::
   This will overwrite an existing Spack configuration, so be careful
   if you've previously set Spack up. If you have existing config, consider
   you might want to follow the instructions below for :ref:`longhorn-own-setup-label`.

If you use the provided ``packages.yaml``, it only tells Spack about
essential existing pre-installed packages on Summit, ie., CUDA, MPI
and the corresponding compilers. Spack will therefore build and
install all other dependencies from scratch, which takes time but has
the advantage that it'll generate pretty much the same software stack
on any machine you use.

On the other hand, ``packages-extended.yaml`` (which needs to be
renamed to ``packages.yaml`` to use it), tells Spack comprehensively
about pre-installed software on Summit, so installation of WDMapp will
proceed more quickly and use system-provided libraries where possible.

.. note::

   Make sure that you don't have a ``spectrum-mpi`` loaded. By default, Longhorn will load the ``xl`` and
   ``spectrum-mpi`` modules for you, and those interfere when Spack
   tries to perform ``gcc`` based builds.
   You might want to consider adding this to your ``.bashrc`` or
   similar init file:

   .. code-block:: shell

      module unload xl spectrum-mpi
   
.. note::

   On Longhorn, the cuda module sets environment variables that set a
   path which ``nvcc`` does not otherwise add. Because of this, it is
   requried to ``module load cuda/10.1.243`` before building GENE, and
   probably other software that uses CUDA..

.. _longhorn-own-setup-label:

Creating your own setup for Longhorn
-------------------------------------------------

Alternatively, you can create your own config:

 .. code-block:: sh

  module load gcc/7.3.0
  spack compiler find

This should find a number of compilers, including gcc 7.3.0. You may
want to repeat this step for gcc 9.1.0 -- however, there is currently
no preinstalled MPI for this compiler.

The compilers on longhorn require ``LD_LIBRARY_PATH`` hackery to function, and spack sanitizes ``LD_LIBRARY_PATH``. The workaround is described `here <https://spack.readthedocs.io/en/latest/basic_usage.html#compiler-environment-variables-and-additional-rpaths>`_. In this case, edit ``~/.spack/linux/compilers.yaml`` using ``spack config edit compilers``
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

Fixing ``config.guess`` on longhorn
-----------------------------------------

Spack has logic that will replace an outdated ``config.guess`` in a
given package with a newer version. This comes in handy, because
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


   
Building WDMapp
================

You should be able to just follow the generic instructions from
:ref:`build-wdmapp-label`.

Running a Sample Job
====================

.. todo::

   Complete instructions on how to get the test case set up and run.

You can get the setup for a coupled WDMapp run by cloning
https://github.com/wdmapp/testcases.

The sample sample job from
https://github.com/wdmapp/wdmapp-config/longhorn/submit_wdmapp.sh will
run the `run_1` coupled case.

.. literalinclude:: ../../summit/submit_wdmapp.sh
   :language: shell
   :linenos:

Submit as usal:

.. code-block:: sh

   $ sbatch submit_wdmapp.sh

 
