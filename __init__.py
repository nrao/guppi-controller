"""Initialize the package for testing.

This __init__ properly imports this package for testing without
building (since Python programmers don't often build between tests).

With this directory in the Python path or in the current directory:
import package

This allows for package subdirectories such as src, test, build, etc
and provides for testing without using setup.py.
"""

from src.__init__ import *
