import unittest
import argparse
from main import cmd_helper
from main import ReadSimulator

class TestSequenceFunctions(unittest.TestCase):
    def setUp(self):
        parser = argparse.ArgumentParser(description="test_parser")
        cmd_helper.defineArguments(parser)
        args = parser.parse_args(['.', '1', '.'])
        self.readSim = ReadSimulator(args)
        
    def test_reverse_complement(self):
        self.assertEqual(self.readSim.reverse_complement('ATCG'), 'CGAT')
        self.assertEqual(self.readSim.reverse_complement('GGCC'), 'GGCC')

if __name__ == '__main__':
    unittest.main()