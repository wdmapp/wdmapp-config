

Rhea and Summit share a common home directory. If you use Spack on
both machines, this leads to issues because both instances will share
their config files, which by default go into ```~/.spack/linux``. If
you only want to use just one or the other machine, you can ignore the following note.
	     
.. note::


   One way to deal with keeping separate spack setups on Rhea and Summit is to make separate
   ``~/.spack/linux-rhea`` and ``~/spack/linux-summit`` directories and
   symlink one or the other to ``~/.spack/linux``

   .. code-block:: sh

      $ # make sure ~/.spack/linux does exit yet -- if it does, move it  out of the way		
      $ mkdir -p ~/.spack/linux-rhea
      $ mkdir -p ~/.spack/linux-summit
      $ ln -snf ~/.spack/linux-rhea ~/.spack/linux # if on rhea
      $ ln -snf ~/.spack/linux-summit ~/.spack/linux # if on summit

   An alternative is to have two separate spack installs, and instead of keeping the config files
   in ``~/.spack``, they can be put into ``$SPACK_ROOT/etc``, so with two different roots they
   can be kept separate. You can then do this in your ``.bashrc``:

   .. code-block:: sh

       if [ `uname -m` == "ppc64le" ]; then
         export SPACK_ROOT=$HOME/spack-summit
       else
         export SPACK_ROOT=$HOME/spack-rhea
       fi
       source $SPACK_ROOT/share/spack/setup-env.sh		   

