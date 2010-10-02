==================
 GUPPI Controller
==================

This is the software controller for GUPPI, "the best damn pulsar instrument in
the world" (via http://www.cv.nrao.edu/~sransom/).  GUPPI started with the name
"Green Bank Ultimate Pulsar Processing Instrument", but really we just call it
"guppi" (though it is *ultimate*).

http://go.nrao.edu/guppi


Installation
============

Python Versions
---------------

The guppi controller was developed against Python 2.5 starting in 2008, and has
also been tested against Python 2.4.

Manual Dependencies
-------------------

Install ``guppi_daq`` first.  This has its own dependencies, including (but not
limited to) ``mysql-python``, ``pyfits``, and some slalib & shared memory
stuff.

This project was developed against Optio's soaplib package, version 0.7.2.  One
of the enhancement requests on this project is to move away from SOAP entirely.
Until that happens, you'll have to track down a pre-0.8 version of soaplib or
update the project to use soaplib's successive (non-Optio) development.  As a
shortcut, this version is already available on beef.gb.nrao.edu.  Go there
first::

    beef.gb.nrao.edu:/home/pulsar64/lib/python2.5/site-packages
    cp -a soaplib-0.7.2dev_r27-py2.5.egg/soaplib somedestination

The ``matplotlib`` dependency (which depends on ``numpy`` and some GUI toolkit)
might not install as easily as the others when installing from the Python
package index, so manual intervention may be required here.


Install with Available Dependencies
-----------------------------------

With setuptools (from ``easy_install``) installed::

    python setup.py install --prefix=/path/to/guppi

Be sure to set a good prefix or remove it altogether.  This command installs
the guppi controller to the given prefix and the required dependencies as
listed in ``setup.py`` to the site packages.  ``python setup.py install`` may
require administrative access when installing these dependencies.  If
dependencies are already installed, any user with write permissions to the
prefix location should be able to install an updated version of the guppi
controller.


supervisord
-----------

Deployments use ``supervisord`` to manage all running processes for the guppi
controller.  Example configurations are available in the ``etc/`` area of the
project.


Versioning
==========

For various reasons, the guppi controller was never versioned.  Instead use a
datestring of ``yyyy.mm.dd``.  Currently this datestring is set manually in
``setup.py``.

You can find your installed version by noting the version in the file path::

    python -c 'import guppi; print guppi.__file__'
