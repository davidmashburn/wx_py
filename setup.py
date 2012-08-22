#!/usr/bin/env python

from distutils.core import setup

setup( name = 'wx_py',
       version = '0.9.8.11',
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
