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

"""Board level utilities for GUPPI."""

__copyright__ = "Copyright (C) 2008 Associated Universities, Inc."
__license__ = "GPL"

import re
from bee2_utils import Bee2Utils

class BoardUtils:
    def __init__(self, utils_class = Bee2Utils, debug = True):
        self.__bof_dir = '/srv/guppi/bof/'
        self.__debug = debug
        self.__proc_dir = '/proc/%s/hw/ioreg/'
        self.__ps_regex = r'fpga\d+.*\.bof'
        self.__sysutils = utils_class(debug)

    def debug(self, message):
        """Displays a debug message."""
        if self.__debug:
            self.__sysutils.debug(message)

    def listAllBofs(self):
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
        for name, pid in self.__sysutils.getProcInfo(self.__ps_regex):
            if name.count('/'):
                name = name.rsplit('/', 1)[1]
            result.append(name + ',u')
        for name in self.__sysutils.listFiles(self.__bof_dir):
            if name.count('/'):
                name = name.rsplit('/', 1)[1]
            if name.endswith('.bof'):
                if name not in [r[:-2] for r in result]:
                    result.append(name + ',a')
                else:
                    a = result.index(name + ',u')
                    result[a] = result[a][:-1] + 'r'
        return result

    def listFreeBofs(self):
        """Returns a list of bofs that are available (not running).

        Filters to only lists profiles which can be spawned onto an
        FPGA with no profiles already loaded (IE if FPGA2 is occupied,
        no profiles for FPGA2 will be shown).
        """
        result = []
        used_fpgas = []
        # Record the fpga number(s) occupied
        for name, pid in self.__sysutils.getProcInfo(self.__ps_regex):
            used_fpgas.append(name[name.find('fpga')+4])
        # Only show bofs for unoccupied FPGAs
        for name in self.__sysutils.listFiles(self.__bof_dir):
            if name.count('/'):
                name = name.rsplit('/', 1)[1]
            if name.endswith('.bof') and \
                    name[name.find('fpga')+4] not in used_fpgas:
                result.append(name)
        return result

    def listRegisters(self):
        """Lists all registers for currently occupied FPGAs."""
        result = []
        for name, pid in self.__sysutils.getProcInfo(self.__ps_regex):
            fpga = re.compile('fpga\d+').search(name)
            if fpga:
                fpga = fpga.group()
                for reg in self.__sysutils.listFiles(self.__proc_dir % pid):
                    if reg.count('/'):
                        reg = reg.rsplit('/', 1)[1]
                    result.append('%s/%s' % (fpga.upper(), reg))
            else:
                self.debug('regList: could not find fpga number for %s' % name)
        return result

    def listRunningBofs(self):
        """Returns a list of bofs that are running."""
        result = []
        for name, pid in self.__sysutils.getProcInfo(self.__ps_regex):
            if name.count('/'):
                name = name.rsplit('/', 1)[1]
            result.append(name)
        return result

    def loadBof(self, bofname):
        """Starts a single bof process."""
        return self.__sysutils.startProc(bofname, self.__bof_dir)

    def readRegister(self, register):
        """Reads a value from the specified register."""
        result = 'Error'
        if register.count('/') == 1:
            fpga, filename = register.split('/')
            info = list(self.__sysutils.getProcInfo(fpga))
            if info != []:
                procname, pid = info[0]
                filename = (self.__proc_dir + filename) % pid
                result = self.__sysutils.readFile(filename)
            else:
                self.debug('regRead: bof for %s not found (%s)'
                           % (fpga, register))
        else:
            self.debug('regRead: %s does not have proper format' % register)
        return result

    def unloadBof(self, bofname):
        """Stops a single bof process, if bofname is unique."""
        return self.__sysutils.stopProc(bofname)

    def writeRegister(self, register, value):
        """Reads a value from the specified register."""
        result = 'False'
        if register.count('/') == 1:
            fpga, filename = register.split('/')
            info = list(self.__sysutils.getProcInfo(fpga))
            if info != []:
                procname, pid = info[0]
                filename = (self.__proc_dir + filename) % pid
                result = self.__sysutils.writeFile(filename, value)
            else:
                self.debug('regWrite: bof for %s not found (%s)'
                           % (fpga, register))
        else:
            self.debug('regWrite: %s does not have proper format' % register)
        return result
