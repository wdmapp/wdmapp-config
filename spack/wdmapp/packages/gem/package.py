# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gem(CMakePackage):
    """The GEM gyrokinetic turbulence code"""

    homepage = "http://www.gemgyrokinetic.org/"
    # FIXME, there is no tarball, but it still needs a URL, so it's fake
    url = "https://github.com/wdmapp/gem/gem.tar.gz"
    git = "git@github.com:wdmapp/GEM.git"

    maintainers = ['germasch', 'jycheng1989']

    version('wdmapp', branch='wdmapp')

    variant('openacc', default=False,
            description='Enable OpenACC')

    depends_on('mpi')
    depends_on('blas')
    depends_on('adios +fortran')
    depends_on('adios2@2.5.0: +fortran')
    depends_on('pspline@0.1.0:')
    depends_on('perfstubs@kg')

    def cmake_args(self):
        args = []
        args += ['-DGEM_USE_OPENACC={}'.format(
            'ON' if '+openacc' in self.spec else 'OFF')]

        return args
