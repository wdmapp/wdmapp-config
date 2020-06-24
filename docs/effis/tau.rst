.. _tau:

Performance Monitoring with TAU
===================================

We have instrumented our codes, and to run XGC/GENE with TAU, 
``tau_exec`` becomes the executable to run and the application is a command line argument to ``tau_exec``.
For example, a snippet for XGC might look like.

.. code-block:: yaml

	tau:  /autofs/nccs-svm1_home1/esuchyta/spack/wdmapp/rhea/spack/opt/spack/linux-rhel7-sandybridge/gcc-8.4.0/tau-develop-ezg374unf3gephlxov5avmmagsplidn2/bin/tau_exec
	xgc:  /autofs/nccs-svm1_home1/esuchyta/spack/wdmapp/rhea/spack/opt/spack/linux-rhel7-sandybridge/gcc-8.4.0/xgc-devel-wdmapp-pvku3hgsn5pfzx3apmkn3fwrfefvu37a/bin/xgc-es
	
	run:
	  xgc:
	    executable_path: ${tau}
	    commandline_args:
	      - -T
	      - mpi
	      - -monitoring
	      - -adios2
	      - ${xgc}
	      - -no_signal_handle

TAU expects the directory in which ``tau_exec`` lives to be ``PATH``, so make sure to 
``spack load tau`` in the ``job_setup`` file when using TAU, e.g.
`our example on Rhea <https://github.com/wdmapp/testcases/blob/master/run_1/rhea/run_1_setup.sh>`_.

EFFIS is able to generate plots of the performance data TAU collects, in a way similar to the one-dimensional plotting:

.. code-block:: yaml

	run:

	  plot-tau-xgc:
	    data: xgc.tau
	    commandline_options:
	      pattern: (BP4Writer|ADIOS_WRITE|MAIN_LOOP\s/)
	      step: "MAIN_LOOP / Calls"

``pattern`` uses Python `re <https://docs.python.org/3/library/re.html>`_ syntax to pick which variable to plot.
``step`` is which variable identifies the code's time step.
