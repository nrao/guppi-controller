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

def generate_mask(n):
    """Generates a bitmask of all 1s of the specified length."""
    return (1 << n) - 1

def xstr2float(xstr, frac_bits=0, sign_bit=32, radix=16):
    """Converts a numeric string from xilinx fixed point to floating point.

    'xstr' is expected to be a hex string, but can be any base as long
    as the proper radix is provided. All xstr values must be in string
    format, however.
    """
    n = int(xstr, radix)
    if sign_bit > 0 and n & (1 << (sign_bit - 1)):
        n -= (1 << sign_bit)
    return float(n) / float(1 << frac_bits)

def float2xstr(num, frac_bits=0, sign_bit=32):
    """Converts a floating point number to a xilinx fixed point hex string.

    'num' can be an integer or floating point, positive or negative.
    Unlike xstr2float, this function does not (currently) allow a radix
    to be specified but instead always converts from base ten to hex.
    """
    n = num * (1 << frac_bits)
    if sign_bit > 0 and num < 0:
        n += (1 << sign_bit)
    return '%x' % int(n)
