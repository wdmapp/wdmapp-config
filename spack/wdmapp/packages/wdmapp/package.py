# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Wdmapp(BundlePackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://github.com/wdmapp"
    # There is no URL since there is no code to download.

    maintainers = ['germasch', 'bd4']

    version('0.0.1')

    # FIXME this is a hack to avoid Spack not finding a feasible hdf5 on its own
    depends_on('hdf5 +hl')
    depends_on('gene@coupling +adios2 +futils +read_xgc +diag_planes +couple_xgc')
    depends_on('xgc1@master +coupling_core_edge +coupling_core_edge_field +coupling_core_edge_varpi2')

