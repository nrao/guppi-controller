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

"""Add to simulator.py with the currently running interpreter... hack job.

e.g. within interpreter:
cicada> execfile('update_simulator.py')
"""

__copyright__ = "Copyright (C) 2008 Associated Universities, Inc."
__license__ = "GPL"

def dot_stderr():
    sys.stderr.write('.')

sys.stdout = open('simulator.py', 'a')
sys.stderr.write('Appending to simulator.py ')
dot_stderr()

keys = get()
dot_stderr()

values = get(keys)
dot_stderr()

packed = []
for i in range(len(keys)):
    packed.append((keys[i], values[i]))
dot_stderr()

print '###################################################################'

print 'parameters = {'
for k,v in packed:
    if len(v) > 8:
        print ", '%s': '%s'" % (k, v[:32])
    else:
        print ", '%s': '%s'" % (k, v[:8])
print '}'
print
dot_stderr()

print 'profiles = {'
lookup = {'a': 'available', 'u': 'unknown', 'r': 'running'}
for token in profiles():
    k,v = token.split(',')
    print ", '%s': states['%s']" % (k, lookup.get(v, 'unknown'))
print '}'
print
dot_stderr()

sys.stdout.close()
sys.stdout = sys.__stdout__
dot_stderr()

sys.stderr.write(' done.\n')
print 'Do the following touchups in simulator.py:'
print '1. Clean out old data.'
print '2. Fix the syntax of the first parameter.'
print '3. Fix the syntax of the first profile.'
print '(remove the leading comma of each in 2 & 3)'
