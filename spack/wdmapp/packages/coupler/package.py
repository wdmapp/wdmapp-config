# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Coupler(CMakePackage):
    """XGC-GENE coupler."""

    homepage = "https://github.com/wdmapp/wdmapp_coupling"
    # FIXME, there is no tarball, but it still needs a URL, so it's fake
    url      = "git@github.com:wdmapp/wdmapp_coupling.tar.gz"
    git      = "git@github.com:wdmapp/wdmapp_coupling.git"

    maintainers = ['cwsmith','Damilare06','phyboyzhang']

    version('0.1.1', tag='v0.1.1', preferred=True)
    version('develop', branch='develop',
      git="git@github.com:SCOREC/wdmapp_coupling.git")
    version('gemExtCpl', branch='gemxgc',
      git="https://github.com/Damilare06/wdmapp_coupling.git")

    depends_on('pkgconfig', type='build')
    depends_on('cmake@3.13:', type='build')

    depends_on('adios2@2.5.0:')
    depends_on('kokkos@3.0.0:')
    depends_on('fftw@3.3.8:')

    def cmake_args(self):
        args = []
        args += ['-DCMAKE_CXX_COMPILER=%s' % self.spec['kokkos'].kokkos_cxx]
        args += ['-DBUILD_TESTING=OFF']
        return args
