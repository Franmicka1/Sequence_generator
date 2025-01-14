import unittest
from sequence_generator.main import reverse_complement

class TestSequenceFunctions(unittest.TestCase):
    def test_reverse_complement(self):
        self.assertEqual(reverse_complement('ATCG'), 'CGAT')
        self.assertEqual(reverse_complement('GGCC'), 'GGCC')
        # Dodajte dodatne testove prema potrebi

if __name__ == '__main__':
    unittest.main()