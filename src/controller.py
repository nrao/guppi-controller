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

import time

from agent import Agent, index, success, failure
from demux import Demux

def generate_mask(n):
    """Generates a bitmask of all 1s of the specified length."""
    return int('1' * n if n > 0 else '0', 2)

class Controller(Agent):
    def __init__(self):
        self.boards = Demux()

        # Controller has a demux, but for now, doesn't add much to methods.
        self.get = self.boards.get
        self.set = self.boards.set
        self.load = self.boards.load
        self.unload = self.boards.unload
        self.profiles = self.boards.profiles
        self.parameters = self.boards.parameters

    # Script to convert from the xilinx register representation to a
    # 'real' number. Only meaningful for fixed point numbers.
    # (int values are already human readable)
    def xstr2int(self, xstr, frac_bits=0, sign_bit=None, radix=16):
        """Converts a numeric string from xilinx fixed point to floating point.

        'xstr' is expected to be a hex string, but can be any base as long
        as the proper radix is provided. All xstr values must be in string
        format, however.
        """
        count = 0
        temp_fb = int(frac_bits)
        mask = generate_mask(temp_fb)
        upper = int(xstr, int(radix)) >> temp_fb
        lower = int(xstr, int(radix)) & mask
        #Account for a sign if present
        if sign_bit:
            temp_sb = int(sign_bit)-frac_bits-1
            sign_mask = 1 << temp_sb
            sign = sign_mask & upper
            upper = (upper & generate_mask(temp_sb)) - sign
        for i in range(0, temp_fb):
            temp_fb -= 1
            count += 1
            if (lower >> temp_fb) & 1:
                upper += 1.0/2**count
        return upper

    def int2xstr(self, num, frac_bits=0, sign_bit=None):
        """Converts a floating point number to a xilinx fixed point hex string.

        'num' can be either an integer or a string, positive or negative.
        Unlike xstr2int, this function does not (currently) allow a radix
        to be specified but instead always converts from base ten to hex.
        """
        count = 0
        temp_fb = int(frac_bits)
        upper = int(float(num))
        lower = float(num) - upper
        if sign_bit and (lower < 0 or upper < 0):
            lower = lower + 1
            lower -= int(lower)
            upper = 2**(int(sign_bit)-temp_fb-1) + upper
            # Make sure to round correctly
            if frac_bits > 0 and lower > 0:
                upper -= 1
        for i in range(0, temp_fb):
            count += 1
            upper = upper << 1
            if lower >= 1.0/2**count:
                upper = upper | 1
                lower -= 1.0/2**count
        # Account for sign bit if present
        if sign_bit and str(num)[0] == '-':
            sign_mask = 1 << (sign_bit-1)
            upper = upper | sign_mask
        upper = hex(upper)
        # Python 2.4+ hack (appends negative sign)
        if upper[0] == '-':
            upper = upper[1:]
        return upper[2:]

    def arm(self):
        set_result = self.set('BEE2/FPGA2/GUPPi_PIPES_ARM', '1')
        time.sleep(1)
        clr_result = self.set('BEE2/FPGA2/GUPPi_PIPES_ARM', '0')
        result = set_result[0] == 'True' and clr_result[0] == 'True'
        return (str(result),)

AgentClass = Controller
