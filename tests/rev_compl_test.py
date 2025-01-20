import unittest
from main import ReadSimulator

class TestSequenceFunctions(unittest.TestCase):
    def setUp(self):
        self.readSim = ReadSimulator()
        
    def test_reverse_complement(self):
        self.assertEqual(self.readSim.reverse_complement(self, 'ATCG'), 'CGAT')
        self.assertEqual(self.readSim.reverse_complement(self, 'GGCC'), 'GGCC')
        # Dodajte dodatne testove prema potrebi

if __name__ == '__main__':
    unittest.main()