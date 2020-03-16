
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

   $ git clone https://github.com/spack/spack.git
   
Enable shell support for Spack.

.. code-block:: sh

  # For bash/zsh users
  $ export SPACK_ROOT=/path/to/spack
  $ . $SPACK_ROOT/share/spack/setup-env.sh

  # For tcsh or csh users (note you must set SPACK_ROOT)
  $ setenv SPACK_ROOT /path/to/spack
  $ source $SPACK_ROOT/share/spack/setup-env.csh

Cloning the WDMapp-config repository
=====================================

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
   if you've previously set Spack up.

   
