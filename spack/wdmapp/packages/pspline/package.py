# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Pspline(CMakePackage):
    """Fork of pspline library used in XGC."""

    homepage = "https://w3.pppl.gov/ntcc/PSPLINE/"
    url      = "https://github.com/wdmapp/pspline.tar.gz"
    git      = "https://github.com/wdmapp/pspline.git"

    maintainers = ['germasch', 'bd4']

    version('0.1.0', tag='v0.1.0', preferred=True)
    version('master', branch='master')

