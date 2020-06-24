
.. note::
  
   Consider also configuring spack to use gpfs scratch space (i.e. ``$MEMBERWORK``)
   as an alternative when building packages, in addition to the default ``tmpfs`` and
   home filesystem (which can have problems with high workload tasks):

   .. code-block:: sh

      $ mkdir -p /gpfs/alpine/scratch/<project-id>/$USER/spack-stage

   and add the following to ``~/.spack/config.yaml`` (``$SPACK_ROOT/etc/spack/config.yaml``).
   Spack tries each entry in order for precedence:

   .. code-block:: yaml

      config:
        build_stage:
          - $tempdir/$user/spack-stage
          - /gpfs/alpine/scratch/<project-id>/$user/spack-stage
          - ~/.spack/stage
