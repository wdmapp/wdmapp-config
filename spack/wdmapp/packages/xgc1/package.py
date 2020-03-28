# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xgc1(CMakePackage):
    """Old version of the XGC1 code used for potential-only coupling."""

    homepage = "https://hbps.pppl.gov/computing/xgc-1"
    # FIXME, there is no tarball, but it still needs a URL, so it's fake
    url      = "https://github.com/wdmapp/xgc1.tar.gz"
    git      = "git@github.com:wdmapp/xgc1.git"

    maintainers = ['germasch', 'bd4']

    version('master', branch='master')

    variant('coupling_core_edge', default=False,
            description='Enable XGC_COUPLING_CORE_EDGE')
    variant('coupling_core_edge_field', default=False,
            description='Enable XGC_COUPLING_CORE_EDGE_FIELD')
    variant('coupling_core_edge_varpi2', default=False,
            description='Enable XGC_COUPLING_CORE_EDGE_VARPI2')

    depends_on('petsc@3.7.0:3.7.999')
    depends_on('pkgconfig')
    #depends_on('parmetis')
    depends_on('pspline')
    depends_on('camtimers')
    depends_on('adios +fortran')
    depends_on('adios2 +fortran')

    def cmake_args(self):
        spec = self.spec
        args = []
        if '+coupling_core_edge' in spec:
            args.append('-DXGC_COUPLING_CORE_EDGE=ON')
        if '+coupling_core_edge_field' in spec:
            args.append('-DXGC_COUPLING_CORE_EDGE_FIELD=ON')
        if '+coupling_core_edge_varpi2' in spec:
            args.append('-DXGC_COUPLING_CORE_EDGE_VARPI2=ON')

        return args

