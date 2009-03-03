# Copyright (C) 2008 Associated Universities, Inc. Washington DC, USA.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 675 Mass Ave Cambridge, MA 02139, USA.

"""Connection to the IBOB (UC Berkeley/CASPER) over Ethernet.

Provide a connection to an IBOB over an Ethernet link.
"""

__author__ = "Ron DuPlain, Patrick Brandt, and John Ford"
__copyright__ = "Copyright (C) 2008 Associated Universities, Inc."
__credits__ = "This code is based on corr v0.0.1 from Aaron Parsons" +\
              "\nhttp://setiathome.ssl.berkeley.edu/~aparsons/python/corr.html"
__date__ = "07 Mar 2008"
__license__ = "GPLv2"

import telnetlib

class TelnetConnection(telnetlib.Telnet):
    """Connection to the IBOB (UC Berkeley/CASPER) over telnet.

    Provide a telnet connection to the IBOB over an Ethernet link.
    """
    def __init__(self, host = None, port = 0):
        telnetlib.Telnet.__init__(self, host, port)

        self.match = 'IBOB'
        self.timeout = 15

    def read(self):
        return self.read_until()

    def readlines(self):
        """Read over telnet.  Return data as a list of untrimmed lines.

        Note: Empty/blank lines are ignored.
        """
        response = []
        result = self.read()
        result = result or ''
        result = str(result)
        lines = result.split('\n')
        for line in lines:
            line = line.replace('\r', '')
            if line:
                response.append(line)
        return response

    def read_until(self, match = None, timeout = None):
        """Read over telnet until match is found."""
        match = match or self.match
        timeout = timeout or self.timeout

        match = str(match)
        timeout = int(timeout)

        result = ""
        try:
            result = telnetlib.Telnet.read_until(self, match, timeout)
        except EOFError, detail:
            raise IOError, detail
        return result

    def recv(self, bufsize, flags = None):
        if flags:
            self.get_socket().recv(bufsize, flags)
        else:
            self.get_socket().recv(bufsize)

    def roundtrip(self, payload = None, match = None, timeout = None):
        """Send payload over telnet and return the response,
        i.e. send payload then receive.
        """
        payload = str(payload)
        self.write(payload)
        return self.read_until(match, timeout)

    def roundtrip_command(self, command, return_list = False):
        payload = '%s\n\r' % str(command)
        if not return_list:
            return self.roundtrip(payload)
        else:
            self.write(payload)
            return self.readlines()

    def send(self, string, flags = None):
        if flags:
            self.get_socket().send(string, flags)
        else:
            self.get_socket().send(string)

    def send_command(self, command):
        payload = '%s\n\r' % str(command)
        self.write(payload)

    def write(self, buffer = None):
        """Send buffer over telnet.  If no buffer is given, write a
        'newline' (i.e. press Enter) over telnet.
        """
        buffer = buffer or ""
        buffer = str(buffer)
        try:
            telnetlib.Telnet.write(self, buffer)
        except AttributeError:
            errormsg = "unable to write %s; connection is closed."\
                       % buffer
            raise IOError, errormsg

def _test():
    """Run doctest on this module."""
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    _test()
