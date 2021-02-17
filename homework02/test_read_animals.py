import unittest
from read_animals import summary_stats

class TestReadAnimals(unittest.TestCase):

    def test_summary_stats(self):

        # Checks if averaging over 'head' works properly
        anims01 = [{'head': 'raven', 'arms': 1, 'legs': 1, 'tail': 1},
                  {'head': 'raven', 'arms': 1, 'legs': 1, 'tail': 1},
                  {'head': 'snake', 'arms': 1, 'legs': 1, 'tail': 1}]
        anim01exp = {'head': 'raven', 'arms': 1, 'legs': 1, 'tail': 1}
        self.assertDictEqual(summary_stats(anims01), anim01exp)

        # Checks if averaging over 'arms', 'legs', and 'tail' works as intended
        # with integer inputs and outputs
        anims02 = [{'head': 'raven', 'arms': 4, 'legs': 3, 'tail': 7},
                  {'head': 'raven', 'arms': 5, 'legs': 2, 'tail': 9},
                  {'head': 'raven', 'arms': 3, 'legs': 1, 'tail': 8}]
        anim02exp = {'head': 'raven', 'arms': 4, 'legs': 2, 'tail': 8}
        self.assertDictEqual(summary_stats(anims02), anim02exp)

        # Checks if integer type casting works with an integer output
        anims03 = [{'head': 'raven', 'arms': 15, 'legs': 15, 'tail': 15},
                  {'head': 'raven', 'arms': 4, 'legs': 4, 'tail': 4},
                  {'head': 'raven', 'arms': 10, 'legs': 10, 'tail': 10}]
        anim03exp = {'head': 'raven', 'arms': 9, 'legs': 9, 'tail': 9}
        self.assertDictEqual(summary_stats(anims03), anim03exp)

        # Checks if integer type casting works with an integer input
        anims04 = [{'head': 'raven', 'arms': 0, 'legs': 1, 'tail': 1},
                  {'head': 'raven', 'arms': 1.9, 'legs': 1, 'tail': 1}]
        anim04exp = {'head': 'raven', 'arms': 0, 'legs': 1, 'tail': 1}
        self.assertDictEqual(summary_stats(anims04), anim04exp)

        # Checks if excess keys have no effect on output
        anims05 = [{'head': 'raven', 'body': 'cow-chicken', 'arms': 1, 'legs': 1, 'tail': 1},
                  {'head': 'raven', 'arms': 1, 'legs': 1, 'tail': 1, 'teeth' : 7},
                  {'head': 'raven', 'arms': 1, 'legs': 1, 'tail': 1}]
        anim05exp = {'head': 'raven', 'arms': 1, 'legs': 1, 'tail': 1}
        self.assertDictEqual(summary_stats(anims05), anim05exp)
        
        #Checks if input is a list
        self.assertRaises(AssertionError, summary_stats, 1)
        self.assertRaises(AssertionError, summary_stats, True)
        self.assertRaises(AssertionError, summary_stats, {})

        #The following check if head is a string containing a valid value
        anims06 = [{'head': 'raven', 'arms': 1, 'legs': 1, 'tail': 1},
                  {'head': 'raven', 'arms': 1, 'legs': 1, 'tail': 1},
                  {'head': 'cow', 'arms': 1, 'legs': 1, 'tail': 1}]
        self.assertRaises(KeyError, summary_stats, anims06)

        anims07 = [{'head': 'raven', 'arms': 1, 'legs': 1, 'tail': 1},
                  {'head': 'raven', 'arms': 1, 'legs': 1, 'tail': 1},
                  {'head': True, 'arms': 1, 'legs': 1, 'tail': 1}]
        self.assertRaises(AssertionError, summary_stats, anims07)

        anims08 = [{'head': 'raven', 'arms': 1, 'legs': 1, 'tail': 1},
                  {'head': 'raven', 'arms': 1, 'legs': 1, 'tail': 1},
                  {'head': 5, 'arms': 1, 'legs': 1, 'tail': 1}]
        self.assertRaises(AssertionError, summary_stats, anims08)

        anims09 = [{'head': 'raven', 'arms': 1, 'legs': 1, 'tail': 1},
                  {'head': 'raven', 'arms': 1, 'legs': 1, 'tail': 1},
                  {'head': [3,4,'raven'], 'arms': 1, 'legs': 1, 'tail': 1}]
        self.assertRaises(AssertionError, summary_stats, anims09)

        #The following check if arms legs or tail are valid data types
        anims10 = [{'head': 'raven', 'arms': 1, 'legs': 1, 'tail': 1},
                  {'head': 'raven', 'arms': 1, 'legs': 1, 'tail': 1},
                  {'head': 'raven', 'arms': 'a', 'legs': 1, 'tail': 1}]
        self.assertRaises(AssertionError, summary_stats, anims10)

        anims11 = [{'head': 'raven', 'arms': 1, 'legs': 1, 'tail': 1},
                  {'head': 'raven', 'arms': 1, 'legs': 1, 'tail': 1},
                  {'head': 'raven', 'arms': [1], 'legs': 1, 'tail': 1}]
        self.assertRaises(AssertionError, summary_stats, anims11)

        anims12 = [{'head': 'raven', 'arms': 1, 'legs': 1, 'tail': 1},
                  {'head': 'raven', 'arms': 1, 'legs': 1, 'tail': 1},
                  {'head': 'raven', 'arms': True, 'legs': 1, 'tail': 1}]
        self.assertRaises(AssertionError, summary_stats, anims12)

        anims13 = [{'head': 'raven', 'arms': 1, 'legs': 1, 'tail': 1},
                  {'head': 'raven', 'arms': 1, 'legs': 1, 'tail': 1},
                  {'head': 'raven', 'legs': 1, 'tail': 1}]
        self.assertRaises(KeyError, summary_stats, anims13)

if __name__ == '__main__':
    unittest.main()