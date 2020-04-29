# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cabana(CMakePackage):
    """The Exascale Co-Design Center for Particle Applications Toolkit
    """
    homepage = "https://github.com/ECP-copa/Cabana"
    git      = "https://github.com/ECP-copa/Cabana.git"
    url      = "https://github.com/ECP-copa/Cabana/archive/0.1.0.tar.gz"

    version('develop', branch='master')
    version('0.2.0', sha256='3e0c0e224e90f4997f6c7e2b92f00ffa18f8bcff72f789e0908cea0828afc2cb')
    version('0.1.0', sha256='3280712facf6932b9d1aff375b24c932abb9f60a8addb0c0a1950afd0cb9b9cf')
    version('0.1.0-rc0', sha256='73754d38aaa0c2a1e012be6959787108fec142294774c23f70292f59c1bdc6c5')

    depends_on("cmake@3.9:", type='build')
    depends_on("kokkos@3.1:")

    def cmake_args(self):
        options = [
            "-DCMAKE_CXX_COMPILER=%s" % self.spec["kokkos"].kokkos_cxx,
        ]

        return options
