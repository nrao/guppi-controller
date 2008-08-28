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

"""Hardware level utilities for the BEE2.

Module to perform hardware I/O; layered over a basic Linux OS.
"""

__copyright__ = "Copyright (C) 2008 Associated Universities, Inc."
__license__ = "GPL"


import glob
import os
import re
import subprocess
import sys
import time


_bof_dir = '/srv/guppi/bof'
_proc_dir = '/proc/%s/hw/ioreg'
_re_fpga = r'fpga\d+'
_re_fpga_ps = r'fpga\d+.*\.bof'
_reg_format = '%s/%s'
_timestamp_fmt = '<%Y-%m-%d_%H:%M:%S>' # Used by time.strftime


class Bee2Utils:
    """Hardware interface class for the Bee2.
    
    Manages all low level utilities such as register I/O, starting
    and stopping borph processes, and retrieving information from
    the Bee2 hardware.
    """
    def __init__(self):
        # Simple cache of 'ps -eo pid,args'
        self.ps_list = None
        self.list_age = 0


    # Pseudo-private
    # Probably should be renamed something more generic
    def _findbof(self, regex):
        """Finds one or more matches in ps for 'regex'.

        Returns results in the form of [['process_name', 'pid'], ...]
        """
        result = []
        r = re.compile(regex, re.IGNORECASE)
        # Refresh the list every N seconds
        now = time.time()
        if (now - self.list_age) > 3:
            self.ps_list = subprocess.Popen(['/bin/ps', '-eo', 'pid,args'],
                                            stdout=subprocess.PIPE, shell=False
                                            ).communicate()[0].split('\n')
        for line in self.ps_list:
            proc = r.search(line)
            if proc:
                result.append([line.split(None, 1)[1],
                               re.compile('\d+').search(line).group()])
        # Default value to prevent iteration from breaking
        # IE 'for x,y in findbof(regex): ...'
        if result == []:
            result = [[None, None]]
        return result


    # Pseudo-private
    def _get_file_list(self, path, subdirs=None):
        """Lists all files in current directory and all subdirectories."""
        filelist = []
        (root, dirs, files) = os.walk(path).next()
        filelist += [os.path.join(root, afile) for afile in files]
        if subdirs:
            for dir in dirs:
                subdirs = self._get_file_list(os.path.join(root, dir), subdirs)
                filelist += subdirs
        return filelist


    def available_bofs(self):
        """Returns a list of bofs that are available (not running).

        Filters to only lists profiles which can be spawned onto an
        FPGA with no profiles already loaded (IE if FPGA2 is occupied,
        no profiles for FPGA2 will be shown).
        """
        result = []

        try:
            os.chdir(_bof_dir)
        except:
            self.debug('available_bofs: directory may not exist %s'
                       % _bof_dir)
        else:
            running = self.running_bofs()
            repo = glob.glob('*.bof')

            fpga_nums = []
            for bof in running:
                fpga_nums += bof[bof.find('fpga')+4]

            for bof in repo:
                if bof[bof.find('fpga')+4] not in fpga_nums:
                    result.append(bof)
        return result


    def bof_start(self, bofname):
        """Starts a single bof process."""
        result = 'False'
        try:
            os.chdir(_bof_dir)
            bofp = subprocess.Popen(['./' + bofname],
                                    stdout = subprocess.PIPE,
                                    close_fds = True, shell = False,
                                    cwd = _bof_dir, bufsize = 16)
            result = 'True'
        except OSError, detail:
            self.debug('bof_start: could not change directories for %s'
                       % bofname)
            result = 'False'
        except RuntimeError:
            self.debug('bof_start: cannot start ' + bofname)
            result = 'False'
        return result


    def bof_stop(self, bofname):
        """Stops a single bof process.

        Process names must be uniquely identifiable. In the case of
        substrings with more than a single match, no processes are
        stopped.
        """
        result = 'False'
        # Substrings must be able to be uniquely identified;
        # if they are not False is returned and a debug message
        # displayed.
        temp = self._findbof(bofname)
        if len(temp) > 1:
            self.debug('bof_stop: could not uniquely identify substring %s'
                       % bofname)
        else:
            temp_name, temp_pid = temp[0]
            if temp_name and temp_pid:
                os.kill(int(temp_pid), 15)
                result = 'True'
        return result


    def build_file_list(self):
        """Builds a list of names of all registers for running bof processes."""
        result = []
        for name, pid in self._findbof('.bof'):
            fpga = None
            if name and pid:
                fpga = re.compile(_re_fpga, re.IGNORECASE).search(name)
            if fpga:
                fpga = fpga.group()
                try:
                    os.chdir(_proc_dir % pid)
                    result += [_reg_format % (fpga.upper(), item[2:])
                               for item in self._get_file_list('.')]
                except OSError:
                    self.debug('build_file_list: %s directory may not exist'
                               % (_proc_dir % pid))
            else:
                self.debug('build_file_list: could not find fpga number for %s'
                           % name)
        return result
    

    def build_proc_list(self):
        """Builds a list of all bof profiles and their statuses.

        The status can be one of:
        available (a) - the bof is not currently running
        running   (r) - the bof is currently running
        unknown   (u) - the bof is running but not located in the repository

        Results are in the form:
        ['<name>,<status>', ...]
        where <name> is the profile's name and <status> is 'a', 'r', or 'u'.
        """
        result = []
        # Running bofs
        for proc, pid in self._findbof(_re_fpga_ps):
            if proc and pid:
                result.append(proc[2:] + ',u')
        # Repository bofs
        try:
            os.chdir(_bof_dir)
        except OSError:
            self.debug('build_proc_list: directory may not exist %s' % _bof_dir)
        else:
            for afile in glob.glob('*.bof'):
                if afile not in [r[:-2] for r in result]:
                    result.append(afile + ',a')
                else:
                    a = result.index(afile + ',u')
                    result[a] = result[a][:-1] + 'r'
        return tuple(result)


    def debug(self, message):
        """Displays a debug message to the controlling terminal."""
        timestamp = time.strftime(_timestamp_fmt)
        print >> sys.stderr, timestamp, message


    def reg_read(self, key):
        """Reads a value from the specified register."""
        result = ''
        if len(key.split('/')) == 2:
            try:
                dummy, pid = self._findbof(key.split('/', 1)[0])[0]
                os.chdir(_proc_dir % pid)
                fd = open(key.split('/', 1)[1])
                temp = fd.readlines()
                fd.close()
                result = ''.join(temp)
            except OSError:
                self.debug('reg_read: could not change directories for %s'
                           % key)
                result = 'KeyError'
            except IOError:
                self.debug('reg_read: could not operate on %s' % key)
                result = 'KeyError'
        else:
            self.debug('reg_read: %s does not have proper format' % key)
            result = 'KeyError'
        return result


    def reg_write(self, key, value):
        """Writes a value to the specified register."""
        result = ''
        if len(key.split('/', 1)) == 2:
            try:
                dummy, pid = self._findbof(key.split('/', 1)[0])[0]
                os.chdir(_proc_dir % pid)
                fd = open(key.split('/', 1)[1], 'w')
                fd.write(value)
                fd.close()
                result = 'True'
            except OSError:
                self.debug('reg_write: could not change directories for %s'
                           % key)
                result = 'False'
            except IOError:
                self.debug('reg_write: could not operate on %s' % key)
                result = 'False'
        else:
            self.debug('reg_write: %s does not have proper format' % key)
            result = 'False'
        return result


    def running_bofs(self):
        """Returns a list of bofs that are running."""
        result = []
        for proc, pid in self._findbof(_re_fpga_ps):
            if proc and pid:
                result.append(proc[2:])
        return result
