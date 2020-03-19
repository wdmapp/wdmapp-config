
Building codes
***************

Standard Installation
===========================

Building a package can be done following the standard Spack way:

.. code-block:: sh

  $ spack install gene

Then, have a coffee and keep your fingers crossed.

Installing for development
===============================

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
