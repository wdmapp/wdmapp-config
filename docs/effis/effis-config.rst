.. _composition:

Workflow Composition in EFFIS
===================================

EFFIS jobs are composed with a YAML configuration file.

* ``effis-compose.py <config file name>`` builds the job
* ``effis-submit <job directory>`` submits the job to the queue.

Bulding and submitting the example Rhea job below looks something like:

.. code-block:: sh

   $ effis-compose.py ~/testcases/run_1/rhea/run_1.yaml
   $ effis-submit /gpfs/alpine/proj-shared/csc143/esuchyta/effis/rhea/wdmapp/xgc-gene-1


Detailed YAML Paramter Example
-----------------------------------

Below is a configuration file from our `run repository <https://github.com/wdmapp/testcases>`_ 
for `core-edge coupling on Rhea <https://github.com/wdmapp/testcases/blob/master/run_1/rhea/run_1.yaml>`_.
To better itemize the discussion, it has been broken up into to several smaller units.

Some top-level keywords set where on the file system the job will run, as well as scheduler configurations.

.. code-block:: yaml

	jobname: xgc-gene  # Name of job given to scheduler (default = kittie-job, but setting is recommended)
	walltime: 3600     # Job walltime request in seconds (default = 3600)

	# EFFIS required parameter: directory for job output, each code runs in separte subdirectory
	rundir: /gpfs/alpine/proj-shared/csc143/esuchyta/effis/rhea/wdmapp/xgc-gene-1

	# EFFIS required section: setup for the machine to run on
	machine:
	  name: rhea                  # rhea, summit, theta, cori, local
	  queue: batch
	  charge: csc143
	  job_setup: run_1_setup.sh   # Shell script to run once job has started (on service node)

Users can define their own variables, for referencing throughout the file.
Deferencing looks like ``${variable-name}``. (See further below.)

.. code-block:: yaml

	# User defined variables, see dereferencing in file-edits
	period_1d: 1   # XGC output frequency for diagnosis.1D
	period_3d: 1   # XGC output frequency for field3D
	steps: 100     # Number of simulation steps to run
	planes: 8      # Number of poloidal plans
	rho: 4         # XGC radial parameter

Shell commands, copies, regular expression file search and replace (using Python ``re`` syntax)
are available during job configuration. (See subsequent file sections as well.)

.. code-block:: yaml

	# Shell commands to run during job composition, i.e. before submission to scheduler
	pre-submit-commands: ["mkdir coupling"]

	# NOTE some EFFIS instructions can live in top-level or code level scope, e.g.
	#  * pre-submit-commands
	#  * copy, copy-contents
	#  * link
	#  * file-edit

``run`` is the section where to specify the codes to run, along with their process decompositions.

.. code-block:: yaml

	# EFFIS required section: Codes to run and their setups
	run:

Each code has a scope under ``run``, where users can adjust settings specific to that code. 
ADIOS I/O groups can be configured, and matched where relevant for coupling.

Starting with ``gene``.

.. code-block:: yaml

	  # 'gene' (or others below) is just a label name, and will run in subdirectory name gene/
	  gene:
	    pre-submit-commands: ["mkdir out"]   # Like pre-submit-commands above
	    processes: 16            # Number of MPI ranks
	    processes-per-node: 16   # Number of MPI ranks per node
	    cpus-per-process: 1      # Number of CPUs per MPI rank

	    # File path to executable to run
	    executable_path: /autofs/nccs-svm1_home1/esuchyta/spack/spack/opt/spack/linux-rhel7-sandybridge/gcc-8.4.0/gene-app-coupling-pysy5qk373yqzlfjotayvxq3w4r4tjjh/bin/gene

	    # Environment variables
	    env:
	      OMP_NUM_THREADS: 1
	      HDF5_USE_FILE_LOCKING: 'FALSE'
	    
	    # Files to copy
	    copy:
	      - ../GENE/parameters
	      - ../GENE/XGC_map_circular_2020_new.h5
	      - ../GENE/adios2cfg.xml
	      - ../GENE/tracer_fast
	      - ../GENE/profiles_ions
	      - ../GENE/coupling.in

	    # Files to edit (paramters is the main GENE configuration file)
	    file-edit:
	      parameters:
	        - ['^\s*ntimesteps\s*=.*$', 'ntimesteps=${steps}']
	        - ['^\s*n_planes\s*=.*$', 'n_planes=${planes}']

	    # ADIOS groups are prefaced with leading .

	    .density_coupling:
	      output_path: density.bp
	      adios_engine: SST

	    # 'reads' matching for coupling reading
	    .field_coupling:
	      reads: xgc.field_coupling

``xgc`` looks similar to ``gene`` but has different input files.

.. code-block:: yaml

	  xgc:
	    pre-submit-commands: ["mkdir restart_dir"]
	    processes: 64            # Number of MPI ranks
	    processes-per-node: 8    # Number of MPI ranks per node
	    cpus-per-process: 1      # Number of CPUs per MPI rank

	    # File path to executable to run
	    executable_path: /autofs/nccs-svm1_home1/esuchyta/spack/spack/opt/spack/linux-rhel7-sandybridge/gcc-8.4.0/xgc-devel-cmake-suchyta-z5m7gdz6miin7ypf6hpv2yuxszkn4rqd/bin/xgc-es

	    # Environment variables
	    env:
	      OMP_NUM_THREADS: 1
	      HDF5_USE_FILE_LOCKING: 'FALSE'

	    # Files to copy
	    copy:
	      - ../XGC/input
	      - ../XGC/adioscfg.xml
	      - ../XGC/adios2cfg.xml
	      - ../XGC/petsc.rc
	      - ../XGC/geqdsk_gene_comp_case5_fix.eqd
	      - ../XGC/geqdsk_gene_comp_case5_fixed.eqd.node
	      - ../XGC/geqdsk_gene_comp_case5_fixed.eqd.ele
	      - ../XGC/den_gene_case5.prf
	      - ../XGC/temp_gene_case5_fix.prf
	      - ../XGC/perturbation.in
	      - ../XGC/ogyropsi_init_cond.bp

	    # Files to edit (input is the main XGC configuration file)
	    file-edit:
	      input:
	    	- ['^\s*sml_mstep\s*=.*$', 'sml_mstep=${steps}']
	    	- ['^\s*sml_nphi_total\s*=.*$', 'sml_nphi_total=${planes}']
	    	- ['^\s*sml_grid_nrho\s*=.*$', 'sml_grid_nrho=${rho}']
	    	- ['^\s*diag_1d_period\s*=.*$', 'diag_1d_period=${period_1d}']
	    	- ['^\s*diag_3d_period\s*=.*$', 'diag_3d_period=${period_3d}']
	    	- ['^\s*adios_stage_3d\s*=.*$', 'adios_stage_3d=.true.']


	    # ADIOS groups are prefaced with leading .

	    .diagnosis.1d:
	      output_path: xgc.oneddiag.bp
	      adios_engine: BP4

	    .field3D:
	      output_path: xgc.3d.bp
	      adios_engine: BP4

	    .diagnosis.mesh:
	      output_path: xgc.mesh.bp
	      adios_engine: BP4

	    # 'reads' matching for coupling reading
	    .density_coupling:
	      reads: gene.density_coupling

	    .field_coupling:
	      output_path: field.bp
	      adios_engine: SST


One and two dimensional plotting can be turned on with special ``run`` keyword sections.

.. code-block:: yaml

	  #  Plot all variable in XGC's diagnosis.1d that use psi as x-axis
	  plot-1D:
	    x: psi
	    data: xgc.diagnosis.1d

	  # Plot varables with same dimensions as XGC field3D's dpot on triangular mesh
	  plot-triangular:
	    commandline_args:
	      - rz               # Name in mesh file of variable for the nodes
	      - nd_connect_list  # Name im mesh file for the node connectivity
	      - dpot[0]          # Dimension setter
	    
	    .mesh:
	      reads: xgc.diagnosis.mesh
	    
	    .plotter:
	      plots: xgc.field3D

For clarity and completion, here is the full file.

.. code-block:: yaml

	jobname: xgc-gene  # Name of job given to scheduler (default = kittie-job, but setting is recommended)
	walltime: 3600     # Job walltime request in seconds (default = 3600)

	# User defined variables, see dereferencing in file-edits
	period_1d: 1   # XGC output frequency for diagnosis.1D
	period_3d: 1   # XGC output frequency for field3D
	steps: 100     # Number of simulation steps to run
	planes: 8      # Number of poloidal plans
	rho: 4         # XGC radial parameter

	# EFFIS required parameter: directory for job output, each code runs in separte subdirectory
	rundir: /gpfs/alpine/proj-shared/csc143/esuchyta/effis/rhea/wdmapp/xgc-gene-1

	# EFFIS required section: setup for the machine to run on
	machine:
	  name: rhea                  # rhea, summit, theta, cori, local
	  queue: batch
	  charge: csc143
	  job_setup: run_1_setup.sh   # Shell script to run once job has started (on service node)

	# Shell commands to run during job composition, i.e. before submission to scheduler
	pre-submit-commands: ["mkdir coupling"]

	# NOTE some EFFIS instructions can live in top-level or code level scope, e.g.
	#  * pre-submit-commands
	#  * copy, copy-contents
	#  * link
	#  * file-edit


	# EFFIS required section: Codes to run and their setups
	run:

	  # 'gene' (or others below) is just a label name, and will run in subdirectory name gene/
	  gene:
	    pre-submit-commands: ["mkdir out"]   # Like pre-submit-commands above
	    processes: 16            # Number of MPI ranks
	    processes-per-node: 16   # Number of MPI ranks per node
	    cpus-per-process: 1      # Number of CPUs per MPI rank

	    # File path to executable to run
	    executable_path: /autofs/nccs-svm1_home1/esuchyta/spack/spack/opt/spack/linux-rhel7-sandybridge/gcc-8.4.0/gene-app-coupling-pysy5qk373yqzlfjotayvxq3w4r4tjjh/bin/gene

	    # Environment variables
	    env:
	      OMP_NUM_THREADS: 1
	      HDF5_USE_FILE_LOCKING: 'FALSE'
	    
	    # Files to copy
	    copy:
	      - ../GENE/parameters
	      - ../GENE/XGC_map_circular_2020_new.h5
	      - ../GENE/adios2cfg.xml
	      - ../GENE/tracer_fast
	      - ../GENE/profiles_ions
	      - ../GENE/coupling.in

	    # Files to edit (paramters is the main GENE configuration file)
	    file-edit:
	      parameters:
	        - ['^\s*ntimesteps\s*=.*$', 'ntimesteps=${steps}']
	        - ['^\s*n_planes\s*=.*$', 'n_planes=${planes}']

	    # ADIOS groups are prefaced with leading .

	    .density_coupling:
	      output_path: density.bp
	      adios_engine: SST

	    # 'reads' matching for coupling reading
	    .field_coupling:
	      reads: xgc.field_coupling

	  xgc:
	    pre-submit-commands: ["mkdir restart_dir"]
	    processes: 64            # Number of MPI ranks
	    processes-per-node: 8    # Number of MPI ranks per node
	    cpus-per-process: 1      # Number of CPUs per MPI rank

	    # File path to executable to run
	    executable_path: /autofs/nccs-svm1_home1/esuchyta/spack/spack/opt/spack/linux-rhel7-sandybridge/gcc-8.4.0/xgc-devel-cmake-suchyta-z5m7gdz6miin7ypf6hpv2yuxszkn4rqd/bin/xgc-es

	    # Environment variables
	    env:
	      OMP_NUM_THREADS: 1
	      HDF5_USE_FILE_LOCKING: 'FALSE'

	    # Files to copy
	    copy:
	      - ../XGC/input
	      - ../XGC/adioscfg.xml
	      - ../XGC/adios2cfg.xml
	      - ../XGC/petsc.rc
	      - ../XGC/geqdsk_gene_comp_case5_fix.eqd
	      - ../XGC/geqdsk_gene_comp_case5_fixed.eqd.node
	      - ../XGC/geqdsk_gene_comp_case5_fixed.eqd.ele
	      - ../XGC/den_gene_case5.prf
	      - ../XGC/temp_gene_case5_fix.prf
	      - ../XGC/perturbation.in
	      - ../XGC/ogyropsi_init_cond.bp

	    # Files to edit (input is the main XGC configuration file)
	    file-edit:
	      input:
	    	- ['^\s*sml_mstep\s*=.*$', 'sml_mstep=${steps}']
	    	- ['^\s*sml_nphi_total\s*=.*$', 'sml_nphi_total=${planes}']
	    	- ['^\s*sml_grid_nrho\s*=.*$', 'sml_grid_nrho=${rho}']
	    	- ['^\s*diag_1d_period\s*=.*$', 'diag_1d_period=${period_1d}']
	    	- ['^\s*diag_3d_period\s*=.*$', 'diag_3d_period=${period_3d}']
	    	- ['^\s*adios_stage_3d\s*=.*$', 'adios_stage_3d=.true.']


	    # ADIOS groups are prefaced with leading .

	    .diagnosis.1d:
	      output_path: xgc.oneddiag.bp
	      adios_engine: BP4

	    .field3D:
	      output_path: xgc.3d.bp
	      adios_engine: BP4

	    .diagnosis.mesh:
	      output_path: xgc.mesh.bp
	      adios_engine: BP4

	    # 'reads' matching for coupling reading
	    .density_coupling:
	      reads: gene.density_coupling

	    .field_coupling:
	      output_path: field.bp
	      adios_engine: SST

	  #  Plot all variable in XGC's diagnosis.1d that use psi as x-axis
	  plot-1D:
	    x: psi
	    data: xgc.diagnosis.1d

	  # Plot varables with same dimensions as XGC field3D's dpot on triangular mesh
	  plot-triangular:
	    commandline_args:
	      - rz               # Name in mesh file of variable for the nodes
	      - nd_connect_list  # Name im mesh file for the node connectivity
	      - dpot[0]          # Dimension setter
	    
	    .mesh:
	      reads: xgc.diagnosis.mesh
	    
	    .plotter:
	      plots: xgc.field3D
