
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

.. note::

   The E4S prjoect has created a build cache for Rhea. This provides many
   packages as precompiled binaries, so will reduce the installation
   time. To use it:

   .. code-block:: sh

      $ wget https://oaciss.uoregon.edu/e4s/e4s.pub
      $ spack gpg trust e4s.pub
      $ spack mirror add E4S https://cache.e4s.io/e4s
		  

   

Building WDMapp
================

You should be able to just follow the generic instructions from
:ref:`build-wdmapp-label`.

.. _rhea-running-cyclone-label:

Running the Cyclone Test Case
=============================

.. include:: cyclone-env.rst

Load the wdmapp modules:

.. code-block:: sh

  $ spack load wdmapp arch=linux-rhel7-sandybridge
  $ spack load effis +compose arch=linux-rhel7-sandybridge

Clone the testcases repo:

.. code-block:: sh

  $ git clone https://github.com/wdmapp/testcases.git
  $ cd testcases/run_1/rhea

See the :ref:`composition` page for help editing the workflow composition file. As quick pointers, 
make sure to edit the path to the run directory (``/path/to/testDir`` below) called ``rundir``, 
the binaries labeled ``executable_path``, and the project, ``charge``,
in ``run_1.yaml`` (or ``run_externalCpl.yaml`` if `wdmapp+passthrough` was
built in :ref:`build-wdmapp-label`).

.. include:: cyclone-run.rst

Running the Cyclone Test Case - External Coupler
================================================

The cyclone test case can be executed with the external coupler
(``wdmapp+passthrough`` built in :ref:`build-wdmapp-label` by
following the instructions for :ref:`rhea-running-cyclone-label` using
``run_externalCpl.yaml`` instead of ``run_1.yaml``.

