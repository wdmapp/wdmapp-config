
WDMapp on Longhorn at TACC
*************************************

Setting up Spack
====================

.. include:: ../spack/setup-intro.rst

.. include:: ../spack/installing-spack.rst

.. include:: ../spack/cloning-wdmapp-config.rst
	     
Longhorn-Specific Setup
=========================

Employing our provided Spack configuration
--------------------------------------------

.. warning::

   The folllowing will overwrite an existing Spack configuration, so be careful
   if you've previously set up Spack. If you have an existing config, consider
   renaming ``~./spack`` to back it up.

Just copy the provided YAML configuration files to where Spack
expects them:

.. code-block:: sh

   $ mkdir -p ~/.spack/linux
   $ cp path/to/wdmapp-config/longhorn/spack/*.yaml ~/.spack/linux

.. note::

   Make sure that you don't have a ``spectrum-mpi`` loaded. By default, Longhorn will load the ``xl`` and
   ``spectrum-mpi`` modules for you, and those interfere when Spack
   tries to perform ``gcc`` based builds.
   You might want to consider adding this to your ``.bashrc`` or
   similar init file:

   .. code-block:: shell

      module unload xl spectrum-mpi
   
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

