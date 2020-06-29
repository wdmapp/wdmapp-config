.. _dashboard:

Enabling the Dashboard
===================================

To turn on the processing that packages up EFFIS images for use with the dashboard,
one needs to configure a ``dashboard`` top-scope section in the configuration file.

.. code-block:: yaml

	base: wdmapp-1
	rundir: /gpfs/alpine/proj-shared/csc143/esuchyta/effis/rhea/wdmapp/${base}
	adios-nompi: /autofs/nccs-svm1_home1/esuchyta/spack/wdmapp/rhea/spack/opt/spack/linux-rhel7-sandybridge/gcc-8.4.0/adios2-2.6.0-k62srrf7btzanzeattmk35orgqd6uyvn
	dashboard:
	  use: true
	  shot_name: ${base}
	  run_name:  run-1
	  http: /ccs/wwwproj/phy122/esuchyta/wdmapp-dashboard/shots
	  env:
	    ADIOS: ${adios-nompi}/lib/python3.7/site-packages

``http`` is a directory that is web accessible for remote download.
At OLCF, there is one such area, and it is only accessible from the service/login nodes, where MPI does not work.
This is why an ADIOS2 build without MPI is needed, which can be built with:

.. code-block:: sh
	
	$ spack install adios2 -mpi +python

``shot-name`` and ``run-name`` are both text labels, where ``run-name`` is meant to allow multiple restarted runs in the same shot.


Deploying the Remote Dashboard
-----------------------------------

Instructions for how to deploy a run an instance of the dashboard that connects to this data can be found on
in the `eSimMon documentation <https://github.com/Kitware/eSimMon>`_.
In short, a monitoring service will given the web address for the ``http`` directory,
pull new data when it becomes available, and then display the images
thorugh a web server that multiple uers can connect to.
