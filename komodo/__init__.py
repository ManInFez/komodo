"""Komodo software distribution build system."""

import os

from .build import make, pypaths
from .fetch import fetch
from .shell import shell, pushd
from .lint import lint
from .cleanup import cleanup
from .maintainer import maintainers

def fixup_python_shebangs(prefix, release):
    """Fix shebang to $PREFIX/bin/python.

    Some packages installed with pip do not respect target executable, that is,
    they set as their shebang executable the Python executabl used to build the
    komodo distribution with instead of the Python executable that komodo
    deploys.  This breaks the application since the corresponding Python modules
    won't be picked up correctly.

    For now, we use sed to rewrite the first line in some executables.

    This is a hack that should be fixed at some point.

    """
    # TODO fix hardcoded fix of ipython, bokeh, ...
    binpath = os.path.join(args.prefix, args.release, 'root', 'bin')
    python_ = os.path.join(binpath, 'python')

    bins = []
    # executables with wrong shebang
    for bin_ in os.path.walk(binpath):
        try:
            with open(bin_, 'r') as f:
                shebang = f.readline()
            if 'python' in shebang and shebang[2:] != binpath:
                bins_.append(bin_)
        except:
            pass

    sedfxp = """sed -i 1c#!{0} {1}"""
    for bin_ in bins_:
        binpath_ = os.path.join(args.prefix, args.release, 'root', 'bin', bin_)
        if os.path.exists(binpath_):
            komodo.shell(sedfxp.format(python_, binpath_))


__version__ = '1.0'
__author__ = 'Software Innovation Bergen, Statoil ASA'

__copyright__ = 'Copyright 2017, Statoil ASA'
__license__ = 'GNU General Public License, version 3 or any later version'

__credits__ = __author__
__maintainer__ = __author__
__email__ = 'fg_gpl@statoil.com'
__status__ = 'Production'

__ALL__ = ['make', 'fetch', 'shell', 'lint', 'maintainers']
