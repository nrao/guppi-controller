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

def xstr2float(xstr, frac_bits=0, sign_bit=None, radix=16):
    """Converts a numeric string from xilinx fixed point to floating point.

    'xstr' is expected to be a hex string, but can be any base as long
    as the proper radix is provided. All xstr values must be in string
    format, however.
    """
    mask = generate_mask(frac_bits)
    upper = int(xstr, radix) >> frac_bits
    lower = int(xstr, radix) & mask
    if sign_bit:
        temp = sign_bit - frac_bits - 1
        sign = upper & (1 << temp)
        upper = (upper & generate_mask(temp)) - sign
    for i in range(1, frac_bits + 1):
        if (lower >> (frac_bits - i)) & 1:
            upper += 1.0 / (1 << i)
    return float(upper)

def float2xstr(num, frac_bits=0, sign_bit=None):
    """Converts a floating point number to a xilinx fixed point hex string.

    'num' can be an integer or floating point, positive or negative.
    Unlike xstr2float, this function does not (currently) allow a radix
    to be specified but instead always converts from base ten to hex.
    """
    upper = int(num)
    lower = num - upper
    if sign_bit and (lower < 0 or upper < 0):
        upper += (1 << (sign_bit - frac_bits - 1))
        # Turn negative fractions into their positive complements of 1
        lower += 1 - int(lower + 1)
        # Correct for the above complementing in the whole number portion
        if (frac_bits > 0) and (lower > 0): upper -= 1
    # Quantize the fractional part of the number
    for i in range(1, frac_bits + 1):
        upper <<= 1
        test = 1.0 / (1 << i)
        if lower >= test:
            upper |= 1
            lower -= test
    # Apply sign bit if the number is negative
    if sign_bit and num < 0:
        sign_mask = 1 << (sign_bit - 1)
        upper |= sign_mask
    upper = hex(upper)
    # Python 2.4+ hack (hex() prepends negative sign)
    if upper.startswith('-'): upper = upper[1:]
    # Some versions append 'L' for long-size values
    if upper.endswith('L'): upper = upper[:-1]
    # Slice off the '0x' portion of the hex string
    return upper[2:]
