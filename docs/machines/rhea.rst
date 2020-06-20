
WDMApp on Rhea at OLCF
*****************************

Setting up Spack
====================

Follow the generic instructions from  :ref:`setup-spack-label` to install Spack and add the
WDMapp package repository.

Rhea-Specific Setup
-------------------------

.. code-block:: sh

  $ mkdir -p ~/.spack/linux-rhea
  $ cp path/to/wdmapp-config/rhea/spack/*.yaml ~/.spack/linux-rhea
  $ ln -snf ~/.spack/linux-rhea linux

.. warning::

   This will overwrite an existing Spack configuration, so be careful
   if you've previously set Spack up. If you have an existing config, consider
   moving ``~./spack`` to back it up.

Consider also configuring spack to use gpfs scratch space (i.e. ``$MEMBERWORK``)
when building packages, rather than the home filesystem which tends to have
problems with high workload tasks:

.. code-block:: sh

  $ mkdir -p /gpfs/alpine/scratch/$USER/spack-stage

and add the following to ``~/.spack/config.yaml``:

.. code-block:: yaml

  config:
    build_stage: /gpfs/alpine/scratch/$user/spack-stage

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

