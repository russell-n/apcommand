
# python standard library
from random import choice, randrange, randint
from string import printable, letters


EMPTY_STRING = ''


class Randomizer(object):
    """
    A class to hold randomizing (static) methods
    """
    @staticmethod
    def random_string(maximum=100):
        """
        Return a random string composed of printable characters

        :param:

         - `maximum`: Max characters to use

        :return: random printable str of at least 1 and at most maximum characters
        """
        maximum = max(maximum, 1)
        return EMPTY_STRING.join([choice(printable) for ch in range(randrange(1, maximum+1))])

    @staticmethod
    def random_letters(maximum=100):
        """
        Create a string of upper and lowercase letters

        :param:

         - `maximum`: most characters allowed

        :return: random string of at least 1 and at most maximum characters
        """
        maximum = max(maximum, 1)
        return EMPTY_STRING.join([choice(letters) for ch in range(randrange(1, maximum+1))])

    @staticmethod
    def random_integer(minimum=0, maximum=100):
        """
        Creates a random integer from 0 to 100 (inclusive)

        :return: random integer
        """
        return randint(minimum, maximum)


# python standard library
import unittest
from types import IntType, StringType


class TestRandomizer(unittest.TestCase):
    def bounds(self):
        bounds = (randint(-100, 100), randint(-100,100))
        minimum = min(bounds)
        maximum = max(bounds)
        return minimum, maximum

    def test_random_integer(self):
        """
        Does the randomizer return an integer within bounds?
        """
        minimum, maximum = self.bounds()
        actual = Randomizer.random_integer(minimum=minimum,
                                           maximum=maximum)
        self.assertGreaterEqual(actual, minimum)
        self.assertLessEqual(actual, maximum)
        self.assertEqual(IntType, type(actual))
        return

    def test_random_letters(self):
        """
        Does it create a string of (alphabet) letters?
        """
        minimum, maximum = self.bounds()
        actual = Randomizer.random_letters(randint(minimum, maximum))
        self.assertGreaterEqual(len(actual), 1)
        self.assertLessEqual(len(actual), max(1, maximum))
        self.assertEqual(StringType, type(actual))
        for character in actual:
            self.assertIn(character, letters)
        return

    def test_random_string(self):
        """
        Does it create a string of printable characters?
        """
        minimum, maximum = self.bounds()
        
        actual = Randomizer.random_string(randint(minimum, maximum))
        self.assertGreaterEqual(len(actual), minimum)
        self.assertLessEqual(len(actual), max(1, maximum))
        for character in actual:
            self.assertIn(character, printable)
        return
