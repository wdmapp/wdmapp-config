
WDMApp on Summit at OLCF
*****************************

Setting up Spack
====================

.. include:: ../spack/setup-intro.rst

.. include:: ../spack/installing-spack.rst

.. include:: ../spack/cloning-wdmapp-config.rst
	     
Summit-Specific Setup
-------------------------

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
   $ cp path/to/wdmapp-config/summit/spack/*.yaml ~/.spack/linux

      
You can have a choice of a basic or a more comprehensive setup for
Spack on Summit from the `wdmapp-config
<https://github.com/wdmapp/wdmapp-config/tree/master/summit/spack>`_
repository.

If you use the provided ``packages.yaml``, it only tells Spack about
essential existing pre-installed packages on Summit, ie., CUDA, MPI
and the corresponding compilers. Spack will therefore build and
install all other dependencies from scratch, which takes time but has
the advantage that it'll generate pretty much the same software stack
on any machine you use.

On the other hand, ``packages-extended.yaml`` (which needs to be
renamed to ``packages.yaml`` to be used), tells Spack comprehensively
about pre-installed software on Summit, so installation of WDMapp will
proceed more quickly and use system-provided libraries where possible.

.. warning ::

   Make sure that you don't have ``xl`` or ``spectrum-mpi`` loaded. By
   default, Summit will load the ``xl`` and ``spectrum-mpi`` modules
   for you, and those interfere when Spack tries to perform ``gcc``
   based builds.  You might want to consider adding this to your
   ``.bashrc`` or similar init file:

   .. code-block:: shell

      module unload xl spectrum-mpi
   
.. note::

   On Summit, the cuda module sets environment variables that set a
   path which ``nvcc`` does not otherwise add. Because of this, it is
   requried to ``module load cuda/10.1.243`` before building GENE, and
   probably other software that uses CUDA..

.. include:: note-olcf-spack-dir.rst

.. include:: ../spack/adding-wdmapp.rst

Building WDMapp
================

You should be able to just follow the generic instructions from
:ref:`build-wdmapp-label`.

Running the Cyclone Test Case
=============================

.. include:: cyclone-env.rst

Load the wdmapp modules:

.. code-block:: sh

  $ spack load effis +compose arch=linux-rhel7-power9le
  $ spack load wdmapp arch=linux-rhel7-power9le

Clone the testcases repo:

.. code-block:: sh

  $ git clone https://github.com/wdmapp/testcases.git
  $ cd testcases/run_1/summit

See the :ref:`composition` page for help editing the workflow composition file. As quick pointers, 
make sure to edit the path to the run directory (``/path/to/testDir`` below) called ``rundir``, 
the binaries labeled ``executable_path``, and the project, ``charge``,
in ``run_1.yaml``.

.. include:: cyclone-run.rst

..
    Running a Sample Job
    ====================
    
    .. todo::
    
       Complete instructions on how to get the test case set up and run.
    
    * You can get the setup for a coupled WDMapp run by cloning
      https://github.com/wdmapp/testcases.
    
    • Call the script ``testcases/run_1/summit/setup_run.sh <run-dir>``,
      which will set up job in the given directory.
      
    • Edit the generated batch script in ``<run-dir>`` to use the paths to
      the GENE and XGC executables that were built by spack in the
      previous step. You should be able to get them from ``spack
      find --paths --deps wdmapp``.
    
      Here is the job script:
    
    .. literalinclude:: ../../summit/submit_wdmapp.sh
       :language: shell
       :linenos:
      
    • Submit the batch script and cross your fingers.
          
    .. code-block:: sh
    
       $ bsub submit_wdmapp.sh
..
