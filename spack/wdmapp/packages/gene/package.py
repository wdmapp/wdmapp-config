# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gene(CMakePackage, CudaPackage):
    """The GENE (Gyrokinetic Electromagnetic Numerical Experiment) code."""

    homepage = "http://genecode.org"
    # FIXME, there is no tarball, but it still needs a URL, so it's fake
    url      = "https://github.com/wdmapp/gene-wip.tar.gz"
    git      = 'git@github.com:wdmapp/gene.git'

    maintainers = ['germasch', 'bd4']

    version('wdmapp-0.1.0', tag='wdmapp-0.1.0', preferred=True,
            submodules=True, submodules_delete=['python-diag'])
    version('cuda_under_the_hood', git="git@gitlab.mpcdf.mpg.de:GENE/gene-dev.git",
            branch='cuda_under_the_hood',
            submodules=True, submodules_delete=['python-diag'])
    version('coupling', branch='coupling',
            submodules=True, submodules_delete=['python-diag'])
    version('passthrough', branch='rpi', git="git@github.com:Damilare06/gene.git",
            submodules=True, submodules_delete=['python-diag'])

    variant('pfunit', default=True,
            description='Enable pfunit tests')
    variant('cuda', default=False,
            description='Enable CUDA functionality')
    variant('perf', default='none', multi=False,
            description='Enable performance library for timing code regions',
            values=('perfstubs', 'nvtx', 'ht', 'none'))
    variant('adios2', default=False,
            description='Enable ADIOS2 I/O capabilities')
    variant('futils', default=False,
            description='Enable futils capabilities')
    variant('wdmapp', default=False,
            description='Enable WDMapp features')
    variant('diag_planes', default=False,
            description='Enable diag_planes')
    variant('effis', default=False,
            description='Enable EFFIS')

    depends_on('mpi')
    depends_on('fftw@3.3:')
    depends_on('lapack')
    depends_on('scalapack')
    depends_on('mpi')
    depends_on('pfunit@3.3.3:3.3.99+mpi max_array_rank=6', when='+pfunit')
    depends_on('adios2', when='+adios2')
    depends_on('hdf5+fortran', when='+futils')
    depends_on('effis@0.1.0', when='+effis')

    conflicts('+effis', when='~adios2',
              msg='+effis requires +adios2 to also be selected.')
    conflicts('+wdmapp', when='~futils',
              msg='+wdmapp requires +futils to also be selected.')

    def cmake_args(self):
        spec = self.spec
        args = ['-DGENE_PERF={0}'.format(spec.variants['perf'].value)]
        args += ['-DGENE_USE_ADIOS2={}'.format('ON' if '+adios2' in spec else 'OFF')]
        args += ['-DGENE_USE_FUTILS={}'.format('ON' if '+futils' in spec else 'OFF')]
        args += ['-DGENE_WDMAPP={}'.format('ON' if '+wdmapp' in spec else 'OFF')]
        args += ['-DGENE_DIAG_PLANES={}'.format('ON' if '+diag_planes' in spec else 'OFF')]
        args += ['-DGENE_USE_EFFIS={}'.format('ON' if '+effis' in spec else 'OFF')]
        if '+pfunit' in spec:
            args.append('-DPFUNIT={}'.format(spec['pfunit'].prefix))
        if '+cuda' in spec:
            args.append('-DGPU=ON')
            cuda_arch = spec.variants['cuda_arch'].value
            # if cuda_arch is not None:
            #     args.append('-DCUDA_FLAGS=-arch=sm_{0}'.format(cuda_arch[0]))

        return args
