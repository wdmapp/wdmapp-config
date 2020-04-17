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

    # FIXME: Add proper versions and checksums here.
    version('cuda_under_the_hood', git="git@gitlab.mpcdf.mpg.de:GENE/gene-dev.git",
            branch='cuda_under_the_hood', preferred=True,
            submodules=True, submodules_delete=['python-diag'])
    version('coupling', branch='coupling',
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
    variant('read_xgc', default=False,
            description='Enable reading of XGC files')
    variant('diag_planes', default=False,
            description='Enable diag_planes')
    variant('couple_xgc', default=False,
            description='Enable coupling with XGC')

    depends_on('mpi')
    depends_on('fftw@3.3:')
    depends_on('lapack')
    depends_on('scalapack')
    depends_on('mpi')
    depends_on('pfunit@3.3.3:3.3.99+mpi max_array_rank=6', when='+pfunit')
    depends_on('adios2', when='+adios2')
    depends_on('hdf5+fortran', when='+futils')

    def cmake_args(self):
        spec = self.spec
        args = ['-DGENE_PERF={0}'.format(spec.variants['perf'].value)]
        args += ['-DGENE_USE_ADIOS2={}'.format('ON' if '+adios2' in spec else 'OFF')]
        args += ['-DGENE_USE_FUTILS={}'.format('ON' if '+futils' in spec else 'OFF')]
        args += ['-DGENE_READ_XGC={}'.format('ON' if '+read_xgc' in spec else 'OFF')]
        args += ['-DGENE_DIAG_PLANES={}'.format('ON' if '+diag_planes' in spec else 'OFF')]
        args += ['-DGENE_COUPLE_XGC={}'.format('ON' if '+couple_xgc' in spec else 'OFF')]
        if '+pfunit' in spec:
            args.append('-DPFUNIT={}'.format(spec['pfunit'].prefix))
        if '+cuda' in spec:
            args.append('-DGPU=ON')
            cuda_arch = spec.variants['cuda_arch'].value
            # if cuda_arch is not None:
            #     args.append('-DCUDA_FLAGS=-arch=sm_{0}'.format(cuda_arch[0]))

        return args
