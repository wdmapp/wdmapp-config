
.. note::
  
   Consider also configuring spack to use gpfs scratch space (i.e. ``$MEMBERWORK``)
   when building packages, rather than the home filesystem which tends to have
   problems with high workload tasks:

   .. code-block:: sh

      $ mkdir -p /gpfs/alpine/scratch/$USER/spack-stage

      and add the following to ``~/.spack/config.yaml``:

   .. code-block:: yaml

      config:
        build_stage: /gpfs/alpine/scratch/$user/spack-stage


