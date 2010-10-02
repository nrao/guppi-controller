#!/usr/bin/env python
"""GUPPI controller package

Software controller for the best damn pulsar instrument in the world.
"""

from setuptools import setup

doclines = __doc__.split("\n")

setup(
    name        = 'guppi'
  , version     = '2010.09.30' # TODO: need a means to automatically update.
  , packages    = ['guppi', 'guppi.scripts']
  , package_dir = {'guppi' : 'src', 'guppi.scripts': 'src/scripts'}
  , scripts = ['scripts/guppi', 'scripts/guppi_server', 'scripts/run_guppi_server', 'scripts/run_guppi_server_gpu',
               'scripts/clr_tengbe', 'scripts/clr_tengbe.txt', 'scripts/findbof', 'scripts/killbof', 'scripts/set_tengbe', 'scripts/set_tengbe.txt',
               ]
  , install_requires = [
        # 'guppi_daq', # not in pypi yet
        # 'soaplib', # currently uses 0.7.2 from Optio, which is out-of-date!
        'numpy',
        'matplotlib',
        'ipython', # for ipython option
        'pytz',
        'supervisor',
        'cherrypy',
        ]
  , maintainer = "NRAO"
  , maintainer_email = "ron.duplain@gmail.com"
  , url = "http://github.com/nrao/guppi-controller"
  , license = "http://www.gnu.org/copyleft/gpl.html"
  , platforms = ["any"]
  , description = doclines[0]
  , long_description = "\n".join(doclines[2:])
  , requires=['guppi_daq']
  )
