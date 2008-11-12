#!/usr/bin/env python
"""GUPPI controller package



"""

from distutils.core import setup, Extension

doclines = __doc__.split("\n")

setup(
    name        = 'guppi'
  , version     = '0.0'
  , packages    = ['guppi']
  , package_dir = {'guppi' : 'src'}
  # , packages    = ['cicada', 'guppi']
  # , package_dir = {'cicada': 'src', 'guppi': path...})
  , maintainer = "NRAO"
  , maintainer_email = "rduplain@nrao.edu"
  # , url = ""
  , license = "http://www.gnu.org/copyleft/gpl.html"
  , platforms = ["any"]
  , description = doclines[0]
  , long_description = "\n".join(doclines[2:])
  , requires=['guppi_daq']
  )
