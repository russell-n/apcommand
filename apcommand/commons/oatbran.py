
import string


LEFT_BRACKET = '['
RIGHT_BRACKET = ']'


class OatBranGroup(object):
    """
    The OatBranGroup helps with regular expression groups
    """
    __slots__ = ()

    @staticmethod
    def group(expression):
        """
        Create a grouped expression

        :param:

         - `expression`: the regular expression to group
        :return: uncompiled group expression for e
        """
        return "({e})".format(e=expression)

    @staticmethod
    def named(name, expression):
        """
        Creates a named group

        :param:

         - `name`: name to give the group
         - `expression`: expression to use in the group
        """
        return "(?P<{n}>{e})".format(n=name,
                                     e=expression)

    @staticmethod
    def not_followed_by(expression):
        """
        Creates a (perl) negative lookahead expression

        :param:

           - `expression`: expression to group
        """
        return "(?!{e})".format(e=expression)

    @staticmethod
    def not_preceded_by(expression):
        """
        Creates a (perl) negative look behind expression

        :param:

         - `expression`: expression to group
        """
        return "(?<!{e})".format(e=expression)



class OatBranClass(object):
    """
    A class to help with character classes
    """
    __slots__ = ()
    @staticmethod
    def character_class(expression):
        """
        Creates a character class from the expression

        :param:

         - `expression`: string to convert
        """
        return "[{e}]".format(e=expression)


# python standard library
import unittest
import random

# this package
from randomizer import Randomizer


L_GROUP = '('
R_GROUP = ')'
L_PERL_GROUP = L_GROUP + "?"


class TestOatBranGroup(unittest.TestCase):
    def test_group(self):
        """
        Does the group method add parentheses?
        """
        sample = Randomizer.random_letters()
        exp = OatBranGroup.group(sample)
        self.assertEqual("(" + sample + ")",exp)
        return

    def test_named(self):
        """
        Does the named method create a named group?
        """
        name = Randomizer.random_letters()
        sample = Randomizer.random_string()
        exp = OatBranGroup.named(name=name, expression=sample)
        expected = '(?P<' + name + '>' + sample + ")"
        self.assertEqual(expected, exp)
        return

    def test_not_followed_by(self):
        """
        Does not_followed_by create a negative lookahead assertion?
        """
        sample = Randomizer.random_string()
        expr = OatBranGroup.not_followed_by(sample)
        self.assertEqual(L_PERL_GROUP + '!' + sample + R_GROUP,
                         expr)
        return

    def test_not_preceded_by(self):
        '''
        Does it create a negative look-behind expression?
        '''
        sample = Randomizer.random_string()
        expr = OatBranGroup.not_preceded_by(sample)
        self.assertEqual(L_PERL_GROUP + "<!" + sample + R_GROUP,
                         expr)


class TestOatBranClass(unittest.TestCase):
    def test_class(self):
        '''
        Does it convert the string to a character class?
        '''
        sample = Randomizer.random_letters()
        expression = OatBranClass.character_class(sample)
        self.assertEqual(LEFT_BRACKET + sample + RIGHT_BRACKET, expression)


def NOT(e):
    return "[^{e}]+".format(e=e)


# cardinality
ONE_OR_MORE = "+"
ZERO_OR_MORE = '*'
ZERO_OR_ONE = "?"
EXACTLY = "{{{0}}}"

def M_TO_N(m, n, e):
    """
    :param:

     - `m`: the minimum required number of matches
     - `n`: the maximum number of  matches
     - `e`: the expression t match
    """
    return "{e}{{{m},{n}}}".format(m=m, n=n, e=e)

def M_TO_N_ONLY(m, n, e):
    """
    :param:

     - `m`: the minimum required number of matches
     - `n`: the maximum number of  matches
     - `e`: the expression t match
    """
    return r"\b{e}{{{m},{n}}}\b".format(m=m, n=n, e=e)
    
# exceptions
DECIMAL_POINT = r'\.'
L_BRACKET = r"\["
R_BRACKET = r"\]"

# operators
OR = "|"

def WORD_BOUNDARY(e):
    return r"\b{e}\b".format(e=e)

def STRING_BOUNDARY(e):
    """
    :return: expr that matches an entire line
    """
    return r"^{e}$".format(e=e)

# string help
STRING_START = "^"
STRING_END = "$"
ALPHA_NUM = r"\w"
ALPHA_NUMS = ALPHA_NUM + ONE_OR_MORE

#anything and everything
ANYTHING = r"."
EVERYTHING = ANYTHING + ZERO_OR_MORE

# numbers
DIGIT = r"\d"
NOT_DIGIT = r"\D"
NON_ZERO = OatBranClass.character_class("1-9")
SINGLE_DIGIT = WORD_BOUNDARY(DIGIT)
TWO_DIGITS = WORD_BOUNDARY(NON_ZERO + DIGIT)
ONE_HUNDREDS = WORD_BOUNDARY("1" + DIGIT + DIGIT)
NATURAL = DIGIT + ONE_OR_MORE

INTEGER = (OatBranGroup.not_preceded_by(DECIMAL_POINT) +  "-" + ZERO_OR_ONE + NATURAL + 
           OatBranGroup.not_followed_by(DECIMAL_POINT))

FLOAT = "-" + ZERO_OR_ONE + NATURAL + DECIMAL_POINT + NATURAL
REAL = OatBranGroup.group(FLOAT + OR + INTEGER)
HEX = OatBranClass.character_class(string.hexdigits)
HEXADECIMALS = HEX + ONE_OR_MORE

SPACE = r"\s"
SPACES = SPACE + ONE_OR_MORE
NOT_SPACE = r'\S'
NOT_SPACES = NOT_SPACE + ONE_OR_MORE
OPTIONAL_SPACES = SPACE + ZERO_OR_MORE

# common constants
DASH = "-"
LETTER = OatBranClass.character_class(expression=string.ascii_letters)
LETTERS = LETTER + ONE_OR_MORE
OPTIONAL_LETTERS = LETTER + ZERO_OR_MORE

# SPECIAL CASES
# NETWORKING
DOT = DECIMAL_POINT
OCTET = OatBranGroup.group(expression=OR.join([SINGLE_DIGIT, TWO_DIGITS, ONE_HUNDREDS,
                         WORD_BOUNDARY("2[0-4][0-9]"), WORD_BOUNDARY("25[0-5]")]))

IP_ADDRESS = DOT.join([OCTET] * 4)

# from commons.expressions
MAC_ADDRESS_NAME = "mac_address"
HEX_PAIR = HEX + EXACTLY.format(2)
MAC_ADDRESS = OatBranGroup.named(name=MAC_ADDRESS_NAME,
                                 expression=":".join([HEX_PAIR] * 6))
