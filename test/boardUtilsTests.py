import os
import sys
import unittest

sys.path.insert(1, '../src')

from board_utils import BoardUtils

class BoardUtilsTests(unittest.TestCase):
    def setUp(self):
        self.__utils = BoardUtils(debug=False)
        # Override the default bof directory to work for unittests
        self.__utils._BoardUtils__bof_dir = '../data'

    def tearDown(self):
        #!!! Get rid of any extra bof files that may have failed to unload
        pass
        
    def testListAllBofs(self):
        # Success
        self.assertEqual('True', self.__utils.loadBof('fpga1.bof'))
        self.assertEqual(['fpga1.bof,r', 'fpga2.bof,a'],
                         self.__utils.listAllBofs())
        self.assertEqual('True', self.__utils.unloadBof('fpga1.bof'))
        # Failure

    def testListFreeBofs(self):
        # Success
        self.assertEqual('True', self.__utils.loadBof('fpga1.bof'))
        self.assertEqual(['fpga2.bof'], self.__utils.listFreeBofs())
        self.assertEqual('True', self.__utils.unloadBof('fpga1.bof'))
        # Failure

    def testListRegisters(self):
        #!!! No good way to test yet
        #!!! Depends on finding a directory in /proc/ on the fly
        pass

    def testListRunningBofs(self):
        # Success
        self.assertEqual('True', self.__utils.loadBof('fpga1.bof'))
        self.assertEqual(['fpga1.bof'], self.__utils.listRunningBofs())
        self.assertEqual('True', self.__utils.unloadBof('fpga1.bof'))
        # Failure

    def testLoadBof(self):
        # Success
        self.assertEqual('True', self.__utils.loadBof('/bin/ls'))
        # Failure
        self.assertEqual('False', self.__utils.loadBof('notABof'))

    def testReadRegister(self):
        #!!! No good way to test yet
        #!!! Depends on finding a directory in /proc/ on the fly
        pass

    def testUnloadBof(self):
        # Success
        self.assertEqual('True', self.__utils.loadBof('fpga1.bof'))
        self.assertEqual('True', self.__utils.unloadBof('fpga1.bof'))
        # Failure
        self.assertEqual('False', self.__utils.unloadBof('notABof'))

    def testWriteRegister(self):
        #!!! No good way to test yet
        #!!! Depends on finding a directory in /proc/ on the fly
        pass

if __name__ == '__main__':
    unittest.main()
