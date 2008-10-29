import sys
import unittest

sys.path.insert(1, '../src')

from bee2UtilsTests  import Bee2UtilsTests
from boardUtilsTests import BoardUtilsTests

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Bee2UtilsTests,  'test'))
    suite.addTest(unittest.makeSuite(BoardUtilsTests, 'test'))
    #suite.addTest(unittest.makeSuite(, 'test'))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
