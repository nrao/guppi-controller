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

Hides the hardware interactions from the upper utility classes.  Uses
standard Linux OS command line features (pipes, ps, etc).
"""

__copyright__ = "Copyright (C) 2008 Associated Universities, Inc."
__license__ = "GPL"

import os
import re
import sys
from subprocess import PIPE, Popen
from time       import strftime, time

class Bee2Utils:
    """Utilities for the Berkeley Emulation Engine 2 (BEE2).

    Runs on a linux-like OS and uses standard command line features.
    """
    def __init__(self, debug = True):
        self.__debug = debug
        self.__list_age = 0
        self.__ps_list = []
        self.__timestamp_fmt = '<%Y-%m-%d_%H:%M:%S>'

    def debug(self, message):
        """Displays a debug message to the controlling terminal."""
        if self.__debug:
            timestamp = strftime(self.__timestamp_fmt)
            print >> sys.stderr, timestamp, message

    def getProcInfo(self, re_str):
        """Returns the full name and PID of processes matching 'regex'.

        Results are returned in ['name', 'pid'] pairs by a generator object.
        """
        regex = re.compile(re_str, re.IGNORECASE)
        # Refresh the list every N seconds
        now = time()
        if (now - self.__list_age) > 3:
            self.__ps_list = Popen(['/bin/ps', '-eo', 'pid,args'],
                                   stdout=PIPE, shell=False
                                   ).communicate()[0].split('\n')
            self.__list_age = now
        for line in self.__ps_list:
            proc = regex.search(line)
            if proc:
                yield [line.split(None, 1)[1],
                       re.compile('\d+').search(line).group()]

    def listFiles(self, path, levels = 0):
        """Returns a list containing all files in the current directory tree.

        Builds a list of all files in the current directory tree up to the
        specified depth in the tree.

        Options:
        path   : specifies the location to search
        levels : specifies search depth of folders in the directory path
        """
        filelist = []
        if os.path.exists(path):
            (root, dirs, files) = os.walk(path).next()
            filelist += [os.path.join(root, afile) for afile in files]
            if levels > 0:
                for dir in dirs:
                    subdirs = self.listFiles(os.path.join(root, dir), levels-1)
                    filelist += subdirs
        else:
            self.debug('listFiles: specified path does not exist %s' % path)
        return filelist

    def readFile(self, filename):
        """Reads from the specified file."""
        result = 'Error'
        try:
            # Make sure there are no file errors before writing the result
            fd = open(filename, 'r')
            temp = fd.read()
            fd.close()
            result = temp
        except IOError:
            self.debug('readFile: could not operate on %s' % filename)
        return result

    def startProc(self, procname, procdir = '.'):
        """Starts a single process.
        
        Assumes that any processes not fully qualified, IE '/bin/ps',
        will be located in the directory specified by the 'procdir'
        parameter (defaults to '.', or current working directory).
        """
        result = 'False'
        try:
            args = procname.split()
            if not args[0].startswith('/'):
                args[0] = './' + args[0]
            bofp = Popen(args, stdout=PIPE, close_fds=True,
                         shell=False, cwd=procdir, bufsize=16)
            result = 'True'
        except (OSError, RuntimeError):
            self.debug('startProc: process cannot be loaded %s' % procname)
        return result

    def stopProc(self, procname):
        """Stops a single process.

        Process names must be uniquely identifiable. In the case of
        substrings with more than a single match, no processes are
        stopped.
        """
        result = 'False'
        info = list(self.getProcInfo(procname))
        if info == [] or len(info) > 1:
            self.debug('stopProc: could not uniquely identify substring %s'
                       % procname)
        else:
            name, pid = info[0]
            if name and pid:
                os.kill(int(pid), 15)
                result = 'True'
        return result

    def writeFile(self, filename, data, mode='w'):
        """Writes data to the specified file."""
        result = 'False'
        try:
            fd = open(filename, mode)
            fd.write(data)
            fd.close()
            result = 'True'
        except IOError:
            self.debug('writeFile: could not operate on %s' % filename)
        return result
