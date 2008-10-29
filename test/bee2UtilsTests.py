import os
import sys
import unittest

sys.path.insert(1, '../src')

from bee2_utils import Bee2Utils

class Bee2UtilsTests(unittest.TestCase):
    def setUp(self):
        self.__utils = Bee2Utils(debug = False)
        self.__prefix = '../data'
        self.__listFiles = ['../data/readFile', '../data/writeFile']

    def testGetProcInfo(self):
        # Success
        self.assertEqual('True', self.__utils.startProc('fpga1.bof', '../data'))
        info = list(self.__utils.getProcInfo(r'fpga\d+.*\.bof'))
        self.assertNotEqual([], info)
        name, pid = info[0]
        if name.count('/'):
            name = name.rsplit('/', 1)[1]
        self.assertEqual('fpga1.bof', name)
        self.assertEqual('True', self.__utils.stopProc('fpga1.bof'))
        # Failure
        self.assertEqual([], list(self.__utils.getProcInfo('notAProcess')))

    def testListFiles(self):
        # Success
        flist = [f for f in self.__utils.listFiles(self.__prefix)
                 if f.endswith('File')]
        self.assertEqual(flist, self.__listFiles)
        # Failure
        self.assertEqual([], self.__utils.listFiles('notAPath'))

    def testReadFile(self):
        # Success
        testFile = os.path.join(self.__prefix, 'readFile')
        expected = '1234567890abcdef'
        contents = self.__utils.readFile(testFile)
        self.assertEqual(contents, expected)
        # Failure
        testFile = os.path.join(self.__prefix, 'notThere')
        expected = 'KeyError'
        contents = self.__utils.readFile(testFile)
        self.assertEqual(contents, expected)

    def testStartProc(self):
        # Success
        self.assertEqual('True', self.__utils.startProc('/bin/ls ../data'))
        # Failure
        self.assertEqual('False', self.__utils.startProc('notAProgram'))

    def testStopProc(self):
        # Success
        self.assertEqual('True', self.__utils.startProc('fpga1.bof', '../data'))
        self.assertEqual('True', self.__utils.stopProc('fpga1.bof'))
        # Failure
        self.assertEqual('False', self.__utils.stopProc('notAProgram'))

    def testWriteFile(self):
        # Success
        testFile = os.path.join(self.__prefix, 'writeFile')
        contents = 'fedcba0987654321'
        if os.path.exists(testFile):
            os.remove(testFile)
        self.__utils.writeFile(testFile, contents)
        self.assertEqual(contents, self.__utils.readFile(testFile))
        # Failure
        #!!! Depends on file permissions

if __name__ == '__main__':
    unittest.main()
