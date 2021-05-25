# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Camtimers(CMakePackage):
    """Camtimers is a derivative version of  the GPTL timing library
    for use in the XGC code."""

    homepage = "https://github.com/wdmapp/camtimers"
    # FIXME, there is no tarball, but it still needs a URL, so it's fake
    url      = "https://github.com/wdmapp/camtimers.tar.gz"
    git      = "https://github.com/wdmapp/camtimers.git"

    maintainers = ['germasch', 'bd4']

    version('0.1.1', tag='v0.1.1', preferred=True)
    version('0.1.0', tag='v0.1.0')
    version('master', branch='master')

    depends_on('mpi')

