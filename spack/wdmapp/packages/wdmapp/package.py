# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Wdmapp(BundlePackage):
    """The ECP WDMapp "Whole Device Model Application".

    This bundle packages pulls in the proper versions/variants
    of GENE and XGC to run a coupled simulation.
    """

    homepage = "https://github.com/wdmapp"
    # There is no URL since there is no code to download.

    maintainers = ['germasch', 'bd4']

    version('0.0.1')

    # FIXME this is a hack to avoid Spack not finding a feasible hdf5 on its own
    depends_on('hdf5 +hl')
    depends_on('gene@coupling +adios2 +futils +wdmapp +diag_planes perf=perfstubs')
    depends_on('xgc1@master +coupling_core_edge +coupling_core_edge_field +coupling_core_edge_varpi2')
    depends_on('xgc-devel@rpi +coupling_core_edge_gene')
    depends_on('coupler@master')

