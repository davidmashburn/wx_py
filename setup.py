#!/usr/bin/env python

from distutils.core import setup

# Read the version number
with open("wx_py/version.py") as f:
    exec(f.read())

setup( name='wx_py',
       version=VERSION, # use the same version that's in version.py
       author = "David Mashburn / Patrick O'Brian",
       author_email = 'david.n.mashburn@gmail.com',
       url = 'http://www.wxpython.org/py.php',
       scripts = ['postinstall.py'],
       packages = ['wx_py'],
       package_dir={'wx_py': 'wx_py'},
       package_data={'wx_py': ['icons/*']},
       description = 'Py Suite including PyCrust and a revamped version, PySlices',
       long_description=open('README.rst').read(),
       install_requires=['wxPython>=2.8']
     )
