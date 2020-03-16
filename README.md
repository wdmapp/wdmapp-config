
# WDMapp build configurations etc

*This is work-in-progress!*

## Spack

The initial goal here is to provide the ability to install the pieces that go into WDMapp via [Spack](https://spack.io).

### Configuring Spack

While in theory Spack can build an environment from scratch, in particular on supercomputers it helps to tell Spack about software that's already there, in particular MPI and compilers. Machine-specific configurations are in [spack/configs](spack/configs).



