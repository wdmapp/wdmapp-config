
Installing Spack
======================

Follow the instructions from the `Spack Documentation 
<https://spack.readthedocs.io/en/latest/getting_started.html>`_.

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
