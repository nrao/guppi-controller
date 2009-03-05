import sys
import unittest

sys.path.insert(1, '../src')

import utility

class UtilityTests(unittest.TestCase):
    def test_xstr2float(self):
        # All numbers will be 32_16
        sign_bit = 32
        frac_bits = 16
        # Positive, integer
        xstr = '00040000'
        self.assertEqual(4, utility.xstr2float(xstr, frac_bits, sign_bit))
        # Positive, fractional
        xstr = '0004c000'
        self.assertEqual(4.75, utility.xstr2float(xstr, frac_bits, sign_bit))
        # Negative, integer
        xstr = 'fffc0000'
        self.assertEqual(-4, utility.xstr2float(xstr, frac_bits, sign_bit))
        # Negative, fractional
        xstr = 'fffb4000'
        self.assertEqual(-4.75, utility.xstr2float(xstr, frac_bits, sign_bit))
        # Zero
        xstr = '0'
        self.assertEqual(0, utility.xstr2float(xstr, frac_bits, sign_bit))

    def test_float2xstr(self):
        # All numbers will be 32_16
        sign_bit = 32
        frac_bits = 16
        # Positive, integer
        f = 4
        self.assertEqual('40000',
                         # Seems like different python versions use different
                         # capitalization for hex()
                         utility.float2xstr(f, frac_bits, sign_bit).lower())
        # Positive, fractional
        f = 4.75
        self.assertEqual('4c000',
                         utility.float2xstr(f, frac_bits, sign_bit).lower())
        # Negative, integer
        f = -4
        self.assertEqual('fffc0000',
                         utility.float2xstr(f, frac_bits, sign_bit).lower())
        # Negative, fractional
        f = -4.75
        self.assertEqual('fffb4000',
                         utility.float2xstr(f, frac_bits, sign_bit).lower())
        # Zero
        f = 0
        self.assertEqual('0', utility.float2xstr(f, frac_bits, sign_bit))

    def test_generate_mask(self):
        self.assertEqual(0,          utility.generate_mask(0))
        self.assertEqual(1,          utility.generate_mask(1))
        self.assertEqual(3,          utility.generate_mask(2))
        self.assertEqual(7,          utility.generate_mask(3))
        self.assertEqual(15,         utility.generate_mask(4))
        self.assertEqual(4294967295, utility.generate_mask(32))

if __name__ == '__main__':
    unittest.main()
