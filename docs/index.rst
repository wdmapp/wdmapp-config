.. WDMapp documentation master file, created by
   sphinx-quickstart on Mon Mar 16 16:46:16 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to WDMapp's documentation!
*******************************************************************

Overview
============

The Whole Device Model Application (WDMApp) in the DOE Exascale
Computing Project (ECP) is developing a high-fidelity model of
magnetically confined fusion plasmas, urgently needed to plan
experiments on ITER and optimize the design of next-step fusion
facilities. These devices will operate in high-fusion-gain physics
regimes not achieved by any experiment, making predictive numerical
simulation the best tool for the task. WDMApp is focused on building
the main driver and coupling framework for a WDM. The main driver is
based on the coupling of two advanced and highly scalable gyrokinetic
codes, XGC and GENE, where the former is a particle-in-cell code
optimized for the treating the edge plasma while the other is a
continuum code optimized for the core. As an alternative, the GEM
gyrokinetic code can be used instead of GENE to simulate the core
region. WDMApp aims to take advantage of the complementary nature of
the simulation codes to build the most advanced and efficient whole
device kinetic transport kernel for the WDM. A major part of the
technical development work is targeting the coupling framework, which
will be further developed for exascale and optimized for coupling most
of the physics modules that will operate at various space and time
scales. The current MPI +X is to be enhanced with
communication-avoiding methods, task-based parallelism, in situ
analysis with resources for load optimization workflows, and deep
memory hierarchy-aware algorithms.

Sample simulation results from the WDMApp codes are available at
http://wdmapp.pppl.gov/.

Building and Running WDMapp
===========================

In the following, we provide instructions on how to build and run
WDMapp on specific machines. We are using the Spack package manager,
so it should be relatively straightforward to install on other
machines as well, see also the generic instructions below.

Overall, the process works like this:

- Apply for access

- Install Spack and customize for your machine.

- Add the WDMapp Spack repo.

- Build and install WDMapp.

- Provide input parameters and setup for simulation run.

- Submit a job.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   access
   machines/summit
   machines/rhea
   machines/longhorn 
   machines/aimos

.. toctree::
   :maxdepth: 2
   :caption: Generic Instructions:

   spack/setup
   build/build
   effis/effis-main
   
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
