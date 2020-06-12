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

    version('0.0.1',preferred=True)

    variant('passthrough', default=False,
            description='Enable pass-through coupler')
    variant('xgc1_legacy', default=False,
            description='Build legacy XGC1/coupling code')
    variant('tau', default=True,
            description='Build TAU version needed for performance analysis of the coupled codes')

    # FIXME this is a hack to avoid Spack not finding a feasible hdf5 on its own
    # CWS - If the variant is not specified for hdf5 then there are
    # concretization errors associated with hdf5. I think this is related 
    # to https://github.com/spack/spack/issues/15478 .
    depends_on('hdf5 +hl', when='~passthrough')
    #normal
    depends_on('gene@coupling +adios2 +futils +wdmapp +diag_planes perf=perfstubs',
        when='~passthrough')
    depends_on('xgc-devel@wdmapp +coupling_core_edge_gene -cabana -adios2',
        when='~passthrough')
    depends_on('coupler@master',
        when='~passthrough')

    # variant +passthrough
    depends_on('hdf5 +hl', when='+passthrough')
    depends_on('gene@passthrough +adios2 +futils +wdmapp +diag_planes perf=perfstubs',
        when='+passthrough')
    depends_on('xgc-devel@rpi +coupling_core_edge_gene -cabana -adios2',
        when='+passthrough')
    depends_on('coupler@develop',
        when='+passthrough')

    # variant +xgc1_legacy
    depends_on('xgc1@master +coupling_core_edge +coupling_core_edge_field +coupling_core_edge_varpi2',
               when='+xgc1_legacy')

    # variant +tau
    depends_on('tau@develop +adios2 ~libunwind ~pdt +mpi', when='+tau')

