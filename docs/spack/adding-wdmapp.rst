
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

