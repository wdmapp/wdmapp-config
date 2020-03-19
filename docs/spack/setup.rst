
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

Summit
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
  
Ubuntu 18.04
---------------------

On Ubuntu 18.04, nothing special needs to be done, though installation
can be sped up by adding a ``packages.yaml`` that teaches it about
system-installed software so that it doesn't have to build everything
from scratch.


