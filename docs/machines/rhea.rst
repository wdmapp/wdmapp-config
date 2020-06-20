
WDMApp on Rhea at OLCF
*****************************

Setting up Spack
====================

.. include:: ../spack/setup-intro.rst

.. include:: ../spack/installing-spack.rst

.. include:: ../spack/cloning-wdmapp-config.rst
	     
Rhea-Specific Setup
======================

.. include:: note-olcf-shared-spack.rst

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
   $ cp path/to/wdmapp-config/rhea/spack/*.yaml ~/.spack/linux

On Rhea an ``olcf`` repo is also needed to make it possible to use
system-installed packages from our Spack. This repo is provided by the
`wdmapp-config` you cloned earlier:

.. code-block:: sh

  $ spack repo add path/to/wdmapp-config/rhea/spack/olcf
  ==> Added repo with namespace 'olcf'

.. include:: note-olcf-spack-dir.rst
  
.. include:: ../spack/adding-wdmapp.rst

Building WDMapp
================

You should be able to just follow the generic instructions from
:ref:`build-wdmapp-label`.

.. _rhea-running-cyclone-label:

Running the Cyclone Test Case
=============================

Enable shell support for Spack:

.. code-block:: sh

  # For bash/zsh users
  $ export SPACK_ROOT=/path/to/spack
  $ . $SPACK_ROOT/share/spack/setup-env.sh

  # For tcsh or csh users (note you must set SPACK_ROOT)
  $ setenv SPACK_ROOT /path/to/spack
  $ source $SPACK_ROOT/share/spack/setup-env.csh

Load the wdmapp modules:

.. code-block:: sh

  $ spack load effis arch=linux-rhel7-sandybridge
  $ spack load wdmapp arch=linux-rhel7-sandybridge

Clone the testcases repo:

.. code-block:: sh

  $ git clone https://github.com/wdmapp/testcases.git
  $ cd testcases/run_1/rhea

Edit the path to the run directory (reffered to as ``/path/to/testDir`` below),
``rundir``, binaries, ``executable_path``, and the project, ``charge``,
in ``run_1.yaml`` (and ``run_externalCpl.yaml`` if `wdmapp+passthrough` was
built in :ref:`build-wdmapp-label`).

.. note::

   Since we loaded the ``wdmapp`` module via Spack the binaries are in your ``PATH``
   and their location can be retrieved with the ``which xgc-es gene cpl``
   command.

Run the effis pre-processor:

.. code-block:: sh

  $ effis-compose.py run_1.yaml

Submit the job:

.. code-block:: sh

  $ effis-submit.py /path/to/testDir


Running the Cyclone Test Case - External Coupler
================================================

The cyclone test case can be executed with the external coupler
(``wdmapp+passthrough`` built in :ref:`build-wdmapp-label` by
following the instructions for :ref:`rhea-running-cyclone-label` using
``run_externalCpl.yaml`` instead of ``run_1.yaml``.

