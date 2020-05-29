from spack import *
import os
import sys
import shutil


class Effis(CMakePackage):
    """Code Coupling framework"""

    homepage = "https://github.com/wdmapp/effis"
    url = homepage

    version('effis',   git='https://github.com/wdmapp/effis.git', branch='effis',   preferred=True)
    version('develop',   git='https://github.com/wdmapp/effis.git', branch='develop',   preferred=False)
    version('login',   git='https://github.com/wdmapp/effis.git', branch='login',   preferred=False)
    version('kittie',  git='https://github.com/wdmapp/effis.git', branch='kittie',  preferred=False)

    variant("mpi", default=True, description="Use MPI")
    variant("shared", default=True, description="Build shared library")

    depends_on('mpi', when="+mpi")
    depends_on('cmake')
    depends_on('adios2')
    depends_on('yaml-cpp')

    extends('python')
    depends_on('python@2.7:', type=('build', 'run'))
    depends_on('py-setuptools')
    depends_on('py-pyyaml')
    depends_on('py-numpy')
    depends_on('py-mpi4py', when="+mpi")

    depends_on('codar-cheetah', when="^python@3:")
    depends_on('py-matplotlib', when="^python@3:")


    def cmake_args(self):
        args = ['-DPYTHON_PREFIX=ON']

        if not self.spec.satisfies('+mpi'):
            args.append("-DUSE_MPI=OFF")
        else:
            args.append("-DCMAKE_CXX_COMPILER={0}".format(self.spec['mpi'].mpicxx))
            args.append("-DCMAKE_C_COMPILER={0}".format(self.spec['mpi'].mpicc))
            args.append("-DCMAKE_Fortran_COMPILER={0}".format(self.spec['mpi'].mpifc))

        if self.spec.satisfies("+shared"):
            args.append("-DBUILD_SHARED_LIBS:BOOL=ON")

        if self.spec.satisfies("^adios2@:2.3.99"):
            filter_file("OldStep = False", "OldStep = True", os.path.join(os.path.join('src', 'Python', 'kittie', 'kittie.py')))

        return args

