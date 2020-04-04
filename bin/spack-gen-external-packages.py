#!/usr/bin/env python3
"""
Usage: spack-gen-external-packages.py > /path/to/spack/etc/spack/packages.yaml

Requires python 3.3+

You can also save to ~/.spack/packages.yaml, but I prefer using the spack
dir because I typically keep multiple spack installs around and I don't
want them interfering with each other with common config.
"""

import sys
import subprocess
import shutil
import os.path


# spack names for packages
PACKAGES = [
  # build tools
  'autoconf', 'automake', 'bison', 'cmake', 'libtool', 'm4', 'flex',
  'pkg-config',

  # system utils
  'binutils', 'curl', 'gawk', 'diffutils', 'zsh',

  # compression
  'zlib', 'xz', 'tar', 'lz4', 'bzip2', 'snappy',

  # libs
  'openssl', 'gettext', 'ncurses', 'readline', 'gmp', 'libpng', 'libffi',
  'gdbm', 'expat', 'sqlite', 'libxml2',
]


RPM_NAME_MAP = {
    'pkg-config': 'pkgconfig',
    'bzip2': 'bzip2-dev',
    'gdbm': 'gdbm-dev',
    'expat': 'expat-dev',
    'sqlite': 'sqlite-dev',
    'libxml2': 'libxml2-dev',
}


DPKG_NAME_MAP = {
    'xz': 'liblzma-dev',
    'bzip2': 'libbz2-dev',
    'ncurses': 'libncurses-dev',
    'zlib': 'zlib1g-dev',
    'gmp': 'libgmp-dev',
    'readline': 'libreadline-dev',
    'libpng': 'libpng-dev',
    'libffi': 'libffi-dev',
    'snappy': 'libsnappy-dev',
    'gdbm': 'libgdbm-dev',
    'expat': 'libexpat1-dev',
    'sqlite': 'libsqlite3-dev',
    'libxml2': 'libxml2-dev',
}


# For packages that separate binary and dev library, it's common
# for only the binary to be installed. Don't use the binary
# version fallback method for these.
SKIP_BINARY_NAME = set([
   'bzip2'
])


def rpm_get_version(pkg_name):
    rpm_name = RPM_NAME_MAP.get(pkg_name, pkg_name)
    cmd = ['rpm', '-q', '--qf', '%{VERSION}', rpm_name]

    try:
        version_output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        return None

    version = version_output.splitlines()[0].decode('utf-8')
    return version


def _dpkg_to_spack_version(v):
    if '+' in v:
        # handle 1.1.1d-0+deb10u2 (openssl)
        parts = v.split('+')
        return parts[0]
    if ':' in v:
        # handle 4:8.3.0 (gcc)
        parts = v.split(':')
        return parts[1]
    return v


def dpkg_get_version(pkg_name):
    dpkg_name = DPKG_NAME_MAP.get(pkg_name, pkg_name)
    cmd = ['dpkg', '-s', dpkg_name]

    try:
        info_output = subprocess.check_output(cmd)
    except subprocess.CalledProcessError:
        return None

    installed = False
    version = None
    for line in info_output.splitlines():
        line = line.decode('utf-8')
        if line.startswith('Status:'):
            value = line[len('Status:'):].strip()
            parts = value.split()
            if 'installed' in parts:
                installed = True
            else:
                return None
        elif line.startswith('Version:'):
            value = line[len('Version:'):].strip()
            version = _dpkg_to_spack_version(value)
    if installed and version is not None:
        return version
    return None


yaml_format = """  {pkg_name}:
    paths:
      {pkg_name}@{pkg_version}%{compiler}: {path}
"""


yaml_format_no_compiler = """  {pkg_name}:
    paths:
      {pkg_name}@{pkg_version}: {path}
"""


def get_version_and_path(binary_name):
    """Fragile way to try to get version and basepath for a binary,
    use only if package system query fails."""
    binary_path = shutil.which(binary_name)
    if binary_path is None:
        return (None, None)

    cmd = [binary_path, '--version']

    version = None
    version_output = subprocess.check_output(cmd)
    version_line = version_output.splitlines()[0].decode('utf-8')
    for word in version_line.split():
        if word[0].isdigit():
            version = word
            break

    if version is None:
        print('version for %s not found' % binary_name)
        return

    # Path needed by spack is the parent of the bin dir
    root_dir = os.path.dirname(os.path.dirname(binary_path))

    return (version, root_dir)


def print_packages_yaml(pkg_name, compiler=None, pkg_fn=None, buildable=True):
    """Search if pkg exists in rpm database, if it does get the version
    number and parent directory name, and write spack packages.yaml config
    to stdout. Assumes all packages are in /usr
    """
    version = None
    if pkg_fn is not None:
        version = pkg_fn(pkg_name)
    if version is None:
        if pkg_name in SKIP_BINARY_NAME:
            return
        # for packages that happen to have same name as a command, try
        # to find the binary
        (version, path) = get_version_and_path(pkg_name)
        if version is None or path is None:
            return
    else:
        path = "/usr"

    if compiler is not None:
        print(yaml_format.format(pkg_name=pkg_name, pkg_version=version,
                                 compiler=compiler, path=path), end='')
    else:
        print(yaml_format_no_compiler.format(
                    pkg_name=pkg_name, pkg_version=version,
                    compiler=compiler, path=path),end='')
    if not buildable:
       print("    buildable: false")
    print()


def main():
    print("packages:")

    pkg_fn = None

    if os.path.exists('/etc/debian_version'):
        pkg_fn = dpkg_get_version
        gcc_version = dpkg_get_version("gcc")
    elif os.path.exists('/etc/redhat-release'):
        pkg_fn = rpm_get_version
        gcc_version = rpm_get_version("gcc")
    else:
        (gcc_version, _) = get_version_and_path('gcc')

    if gcc_version is None:
        print("Error: unable to find gcc version, exiting")
        sys.exit(1)

    compiler = "gcc@" + gcc_version

    # Note: specifying the compiler used to build external packages is
    # in theory a nice idea, however it has an unfortunate side effect
    # of encouraging spack to use the system compiler to build software
    # when it's dependencies are build with it, even when a newer compiler
    # is set as the default in concretization preferences in packages.yaml

    # setting buildable false can break things when a package requires
    # a new release. If spack is misbehaving and not properly favoring
    # already installed versions over new versions, we can try to
    # force the priority with lines like this:
    #    version: [{pkg_version}, "{pkg_version}:"]

    # List of binaries commonly found on a typical Linux system
    for pkg_name in PACKAGES:
        print_packages_yaml(pkg_name, compiler=None, pkg_fn=pkg_fn,
                            buildable=True)


if __name__ == '__main__':
    main()
