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

    version('0.1.0',preferred=True)

    variant('externalCpl', default=False,
            description='Enable external coupler')
    variant('xgc1_legacy', default=False,
            description='Build legacy XGC1/coupling code')
    variant('tau', default=True,
            description='Build TAU version needed for performance analysis of the coupled codes')
    variant('effis', default=True,
            description='Enable EFFIS')

    # normal
    depends_on('gene@wdmapp-0.1.0 +adios2 +futils +wdmapp +diag_planes perf=perfstubs',
        when='~externalCpl')
    depends_on('xgc-devel@wdmapp-0.1.0 +coupling_core_edge_gene -cabana +adios2',
        when='~externalCpl')
    depends_on('coupler@master',
        when='~externalCpl')

    # variant +externalCpl
    depends_on('gene@externalCpl +adios2 +futils +wdmapp +diag_planes perf=perfstubs',
        when='+externalCpl')
    depends_on('xgc-devel@rpi +coupling_core_edge_gene -cabana +adios2',
        when='+externalCpl')
    depends_on('coupler@wdmapp-0.1.0',
        when='+externalCpl')

    # variant +xgc1_legacy
    depends_on('xgc1@master +coupling_core_edge +coupling_core_edge_field +coupling_core_edge_varpi2',
               when='+xgc1_legacy')

    # variant +tau
    depends_on('tau@develop +adios2 ~libunwind ~pdt +mpi', when='+tau')

    # variant +effis
    depends_on('effis@0.1.0 -python -compose', when='+effis')
    depends_on('gene@wdmapp-0.1.0 +effis', when='~externalCpl +effis')
    depends_on('xgc-devel@wdmapp-0.1.0 +effis', when='~externaCpl +effis')


    # FIXME these are hacks to avoid Spack not finding a feasible packages on its own
    # CWS - If the variant is not specified for hdf5 then there are
    # concretization errors associated with hdf5. I think this is related 
    # to https://github.com/spack/spack/issues/15478 .

    # Contretization fixes
    depends_on('adios  +fortran +sz')
    depends_on('adios2 +fortran +sz')   # The ADIOS +sz (+fortran) is to be explicit, but it's the default
    depends_on('sz@:1.4.12.99')         # ADIOS1 needs sz < 2.0.0, ADIOS2 defaults to sz > 2.0.0
    depends_on('hdf5 +hl +fortran')     # PETSc needes +hl, Apps need +fortran
    depends_on('python@:2.9.99')        # PETSc 3.7.7 needs Python 2.7, EFFIS defaults to Python 3
    depends_on('hwloc@:1.99.99')

