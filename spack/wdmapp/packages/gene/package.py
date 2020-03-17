# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gene(CMakePackage, CudaPackage):
    """The GENE (Gyrokinetic Electromagnetic Numerical Experiment) code."""

    homepage = "http://genecode.org"
    # FIXME, there is no tarball, but it still needs a URL, so it's fake
    url = "https://github.com/wdmapp/gene-wip.tar.gz"
    git = "https://github.com/wdmapp/gene-wip"

    maintainers = ['germasch', 'bd4']

    # FIXME: Add proper versions and checksums here.
    version('cuda_under_the_hood',
            git='git@gitlab.mpcdf.mpg.de:GENE/gene-dev.git',
            branch='cuda_under_the_hood',
            submodules=True, submodules_delete=['python-diag'])
    version('cuth-wip', git='git@github.com:wdmapp/gene-wip.git',
            branch='cuth-wip',
            submodules=True, submodules_delete=['python-diag'])

    variant('pfunit', default=True,
            description='Enable pfunit tests')
    variant('cuda', default=False,
            description='Enable CUDA functionality')
    variant('perf', default='none', multi=False,
            description='Enable performance library for timing code regions',
            values=('perfstubs', 'nvtx', 'ht', 'none'))

    depends_on('mpi')
    depends_on('fftw@3.3:')
    depends_on('lapack')
    depends_on('scalapack')
    depends_on('mpi')
    depends_on('pfunit@3.3.3:3.3.99+mpi max_array_rank=6', when='+pfunit')

    def cmake_args(self):
        spec = self.spec
        args = ['-DGENE_PERF={0}'.format(spec.variants['perf'].value)]
        if '+pfunit' in spec:
            args.append('-DPFUNIT={}'.format(spec['pfunit'].prefix))
        if '+cuda' in spec:
            args.append('-DGPU=ON')
            cuda_arch = spec.variants['cuda_arch'].value
            if cuda_arch is not None:
                args.append('-DCUDA_FLAGS=-arch=sm_{0}'.format(cuda_arch[0]))

        return args
