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

import re
import readline
import sys

from agent_client import AgentClient
from agent import index

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
# cicada = AgentClient(host = 'bee2')
cicada = AgentClient()

# Set the command prompt
def set_prompt(prompt, sentinel = '>', spacer = True):
    sys.ps1 = prompt + sentinel

    sys.ps2 = ''
    for c in sys.ps1:
        sys.ps2 += '.'

    if spacer:
        sys.ps1 += ' '
        sys.ps2 += ' '

# Prepare tab auto-completion for fuctions.
class Completer:
    def __init__(self):
        self.ignored = []

        self.prereg = globals().keys()
        self.functions = []
        self.parameters = []
        self.profiles_a = []
        self.profiles_r = []

        self.matches = [None]
        self.prefix = None
        self.term = dict(get = ')'
                         , load = ')'
                         , set = ', '
                         , unload = ')'
                         )
        self.noarg = ['is_locked', 'lock', 'unlock', 'arm']

    def complete(self, text, loc):
        tokens = text.split('(')
        func = tokens[0]
        if text.find('(') != -1:
            term = self.term.get(func, '')
            param = tokens[1].replace("'", '')
            if func in ('get', 'set'):
                self.matches = [func + '(' + "'" + p + "'" + term for p
                                in self.parameters if p.startswith(param)]
            elif func in ('load'):
                self.matches = [func + '(' + "'" + p + "'" + term for p
                                in self.profiles_a if p.startswith(param)]
            elif func in ('unload'):
                self.matches = [func + '(' + "'" + p + "'" + term for p
                                in self.profiles_r if p.startswith(param)]
        else:
            self.matches = []
            matches = [f + '(' for f in self.functions
                       if f.startswith(text)]
            for match in matches:
                if match.replace('(', '') in self.noarg:
                    match = match + ')'
                self.matches.append(match)
        try:
            return self.matches[loc]
        except IndexError:
            return [None]

    def ignore(self, key = None):
        if key:
            self.ignored.append(key)
            self.update_functions()
            self.update_parameters()
            self.update_profiles()
        else:
            return self.ignored

    def noargs(self, key):
        self.noarg.append(key)

    def trim(self, list):
        for key in self.ignored:
            try:
                list.remove(key)
            except ValueError:
                pass

    def update_functions(self):
        postreg = globals().keys()
        for key in self.prereg:
            postreg.remove(key)

        self.functions = postreg
        self.trim(self.functions)
        self.functions.sort()

    def update_parameters(self):
        self.parameters = get()
        self.trim(self.parameters)
        self.parameters.sort()

    def update_profiles(self):
        self.profiles_a = []
        self.profiles_r = []
        for token in profiles():
            profile, status = token.split(',')
            if status in ('a'):
                self.profiles_a.append(profile)
            elif status in ('r', 'u'):
                self.profiles_r.append(profile)
        self.trim(self.profiles_a)
        self.trim(self.profiles_r)
        self.profiles_a.sort()
        self.profiles_r.sort()

completer = Completer()

# Register "command-line" functions.
set = cicada.set
arm = cicada.arm
int2xstr = cicada.int2xstr
xstr2int = cicada.xstr2int

def get(keys = index):
    if isinstance(keys, str):
        keys = [keys]
        return cicada.get(keys)[0]
    return cicada.get(keys)

def parameters(keys = index):
    if isinstance(keys, str):
        keys = [keys]
        return cicada.parameters(keys)[0]
    return cicada.parameters(keys)

def profiles(keys = index):
    if isinstance(keys, str):
        keys = [keys]
        return cicada.profiles(keys)[0]
    return cicada.profiles(keys)

def load(keys = index):
    if isinstance(keys, str):
        keys = [keys]
        result = cicada.load(keys)[0]
    else:
        result = cicada.load(keys)
    completer.update_profiles()
    completer.update_parameters()
    return result

def unload(keys = index):
    if isinstance(keys, str):
        keys = [keys]
        result = cicada.unload(keys)[0]
    else:
        result = cicada.unload(keys)
    completer.update_profiles()
    completer.update_parameters()
    return result

completer.ignore('completer')
completer.update_functions()

# Prepare tab auto-completion for parameters.
completer.update_parameters()

# Prepare tab auto-completion for profiles.
completer.update_profiles()

# Set tab auto-completion in the readline module.
delims = readline.get_completer_delims()
delims = delims.replace('(', '').replace('/', '').replace("'", '')
# To do: see if FEW delims is the way to go.
delims = ' =)'
readline.set_completer_delims(delims)

readline.parse_and_bind("tab: complete")
readline.set_completer(completer.complete)

# Execute files called at command-line.
set_prompt('', '', False)
for i in range(1, len(sys.argv)):
    execfile(sys.argv[i])

# Print welcome message(s).
set_prompt('guppi')
print 'Welcome to the NRAO GUPPI interpreter and command prompt.'
print
print 'functions:'
for func in completer.functions: print '   ', func
print
print 'All values are ASCII representation of hex values.'
print 'Use tab auto-completion for functions and parameters.'
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
    execfile('scripts/exec.py')
except:
    pass
else:
    # print 'Successfully added custom scripts.'
    pass
