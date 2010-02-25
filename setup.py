#!/usr/bin/env python
"""GUPPI controller package



"""

from distutils.core import setup, Extension

doclines = __doc__.split("\n")

setup(
    name        = 'guppi'
  , version     = '0.0'
  , packages    = ['guppi', 'guppi.scripts']
  , package_dir = {'guppi' : 'src', 'guppi.scripts': 'src/scripts'}
  # , packages    = ['cicada', 'guppi']
  # , package_dir = {'cicada': 'src', 'guppi': path...})
  , scripts = ['scripts/guppi', 'scripts/guppi_server', 'scripts/run_guppi_server', 'scripts/run_guppi_server_gpu']
  , maintainer = "NRAO"
  , maintainer_email = "rduplain@nrao.edu"
  # , url = ""
  , license = "http://www.gnu.org/copyleft/gpl.html"
  , platforms = ["any"]
  , description = doclines[0]
  , long_description = "\n".join(doclines[2:])
  , requires=['guppi_daq']
  )
