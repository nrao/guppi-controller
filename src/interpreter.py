# Copyright (C) 2008 Associated Universities, Inc. Washington DC, USA.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

__copyright__ = "Copyright (C) 2008 Associated Universities, Inc."
__license__ = "GPL"

import os
import re
import readline
import sys

from client import Client
from agent import index
from completer import Completer

# Enable cross-session history.
from os import path, environ, listdir
history_file = path.join(environ["HOME"], ".guppi_history")
try:
    readline.read_history_file(history_file)
except IOError:
    pass

import atexit
atexit.register(readline.write_history_file, history_file)

del history_file
del atexit
del path, environ

# Establish client.
# cicada = Client(host = 'bee2')
cicada = Client()
completer = Completer()

# Set the command prompt
def set_prompt(prompt, sentinel = '>', spacer = True):
    sys.ps1 = prompt + sentinel

    sys.ps2 = ''
    for c in sys.ps1:
        sys.ps2 += '.'

    if spacer:
        sys.ps1 += ' '
        sys.ps2 += ' '

# Register "command-line" functions.
arm = cicada.arm
get = cicada.get
set = cicada.set
parameters = cicada.parameters
profiles = cicada.profiles
load = cicada.load
unload = cicada.unload

from utility import xstr2float, float2xstr

readline.parse_and_bind("tab: complete")
readline.set_completer(completer.complete)

# Execute files called at command-line.
# set_prompt('', '', False)
# for i in range(1, len(sys.argv)):
#     execfile(sys.argv[i])

# Print welcome message(s).
set_prompt('guppi')
print 'Welcome to the NRAO GUPPI interpreter and command prompt.'
print
try:
    completer.get_functions()
except:
    pass
else:
    print 'functions:'
    for func in completer.get_functions(): print '   ', func
    print
    print 'Use tab auto-completion for functions and parameters.'
print 'All values are ASCII representation of hex values.'
print
print

# To do:

# Try next? "natural language processing"
#    * parameter -- for get(paramter)
#    * parameter = value -- for set(parameter, value)
#    * load profile -- for load(profile)
# ... complete with tab auto-completion.

# Support command_prompt history file?

# Support auto-completion of functions from execd files?

# Be ballsy and exec the scripts/exec.py bootstrap file.

try:
    print 'Loading console scripts...'
    thisdir = os.path.dirname(os.path.abspath(__file__))
    execfile(thisdir + '/' + 'scripts/exec.py')
except:
    print 'Failed to load custom scripts.'
    pass
    # from scripts import *
else:
    print 'Successfully added custom scripts.'
    pass
