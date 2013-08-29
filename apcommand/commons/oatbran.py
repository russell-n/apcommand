
import string


LEFT_BRACKET = '['
RIGHT_BRACKET = ']'


class Group(object):
    """
    The Group helps with regular expression groups
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
    def not_followed_by(suffix):
        """
        Creates a (perl) negative lookahead expression

        e.g. 'alpha(?!beta)' matches 'alpha' and 'alphagamma', not 'alphabeta'

        :param:

           - `suffix`: suffix to avoid matching
        """
        return "(?!{s})".format(s=suffix)

    @staticmethod
    def not_preceded_by(prefix):
        """
        Creates a (perl) negative look behind expression

        :param:

         - `prefix`: expression to group
        """
        return "(?<!{e})".format(e=prefix)


class Quantifier(object):
    """
    A class to hold cardinality helpers
    """
    __slots__ = ()

    one_or_more = '+'
    zero_or_more = '*'
    zero_or_one = '?'

    @staticmethod
    def exactly(repetitions):
        """
        Creates suffix to match source repeated exactly n times

        :param:

         - `repetitions`: number of times pattern has to repeat to match
        """
        return "{{{0}}}".format(repetitions)

    @staticmethod
    def m_to_n(m, n):
        """
        Creates a repetition ranges suffix {m,n}
        
        :param:

        - `m`: the minimum required number of matches
        - `n`: the maximum number of  matches
        """
        return "{{{m},{n}}}".format(m=m, n=n)



class CharacterClass(object):
    """
    A class to help with character classes
    """
    __slots__ = ()

    alpha_num = r"\w"
    alpha_nums = alpha_num + Quantifier.one_or_more
    
    @staticmethod
    def character_class(characters):
        """
        Creates a character class from the expression

        :param:

         - `characters`: string to convert to a class

        :return: expression to match any character in expression
        """
        return "[{e}]".format(e=characters)

    @staticmethod
    def not_in(characters):
        """
        Creates a complement character class

        :param:

         - `characters`: characters to not match

        :return: expression to match any character not in expression
        """
        return "[^{e}]".format(e=characters)


class Boundaries(object):
    """
    A class to hold boundaries for expressions
    """
    __slots__ = ()

    string_start = "^"
    string_end = "$"

    @staticmethod
    def word(word):
        """
        Adds word boundaries to the word

        :param:

         - `word`: string to add word boundaries to

        :return: string (raw) with word boundaries on both ends
        """
        return r"\b{e}\b".format(e=word)

    @staticmethod
    def string(string):
        """
        Adds boundaries to only match an entire string

        :param:

         - `string`: string to add boundaries to

        :return: expression that only matches an entire line of text
        """
        return r"^{e}$".format(e=string)


class Numbers(object):
    """
    A class to hold number-related expressions
    """
    __slots__ = ()
    
    decimal_point = r'\.'
    digit = r'\d'
    non_digit = r'\D'
    non_zero = CharacterClass.character_class("1-9")
    single_digit = Boundaries.word(digit)
    two_digits = Boundaries.word(non_zero + digit)


# python standard library
import unittest
import random
import re

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
        sample = Randomizer.letters()
        exp = Group.group(sample)
        self.assertEqual("(" + sample + ")",exp)
        matched = re.search(exp,sample+Randomizer.letters()).groups()[0]
        self.assertEqual(matched, sample)
        return

    def test_named(self):
        """
        Does the named method create a named group?
        """
        name = Randomizer.letters()
        sample = Randomizer.letters()
        text = Randomizer.letters() + sample + Randomizer.letters()
        exp = Group.named(name=name, expression=sample)
        expected = '(?P<' + name + '>' + sample + ")"
        self.assertEqual(expected, exp)
        matched = re.search(exp, text).groupdict()[name]
        self.assertEqual(sample, matched)
        return

    def test_not_followed_by(self):
        """
        Does not_followed_by create a negative lookahead assertion?
        """

        prefix = Randomizer.letters(maximum=5)
        suffix = Randomizer.letters_complement(prefix)
        expr = Group.not_followed_by(suffix)
        text = Randomizer.letters() 
        self.assertEqual(L_PERL_GROUP + '!' + suffix + R_GROUP,
                         expr)

        self.assertIsNone(re.search(text + expr, text + suffix))
        self.assertIsNotNone(re.search(text + expr, text))
        return

    def test_not_preceded_by(self):
        '''
        Does it create a negative look-behind expression?
        '''
        prefix = Randomizer.letters()
        expr = Group.not_preceded_by(prefix)
        self.assertEqual(L_PERL_GROUP + "<!" + prefix + R_GROUP,
                         expr)
        text = Randomizer.letters(minimum=5)

        print expr
        print text
        is_preceded_by = prefix + text
        print is_preceded_by        
        self.assertIsNone(re.search(expr + text, is_preceded_by))
        self.assertIsNotNone(re.search(expr + text, text))
        return


class TestOatBranClass(unittest.TestCase):
    def test_class(self):
        '''
        Does it convert the string to a character class?
        '''
        sample = Randomizer.letters()
        expression = CharacterClass.character_class(sample)
        self.assertEqual(LEFT_BRACKET + sample + RIGHT_BRACKET, expression)
        sub_string = random.choice(sample)
        complement = Randomizer.letters_complement(sample)

        self.assertIsNotNone(re.search(expression, sub_string))
        self.assertIsNone(re.search(expression, complement))
        return

    def test_not(self):
        '''
        Does it convert the string to a non-matching class?
        '''
        sample = Randomizer.letters(maximum=10)
        complement = Randomizer.letters_complement(sample)
        expression = CharacterClass.not_in(sample)
        self.assertEqual(LEFT_BRACKET + '^' + sample + RIGHT_BRACKET,
                         expression)

        self.assertIsNone(re.search(expression, sample))
        self.assertIsNotNone(re.search(expression, complement))
        return

    def test_alpha_num(self):
        """
        Does it return alpha-num character class (plus underscore)?
        """
        expression = CharacterClass.alpha_num
        character = random.choice(string.letters + string.digits + '_')
        non_alpha = random.choice(string.punctuation)
        self.assertIsNotNone(re.search(expression, character))
        self.assertIsNone(re.search(expression, non_alpha))
        return

    def test_alpha_nums(self):
        """
        Does it return the expression to match one or more alpha-nums?
        """
        expression = CharacterClass.alpha_nums


class TestQuantifier(unittest.TestCase):
    def test_one_or_more(self):
        """
        Does it return the one-or-more metacharachter?
        """
        character = random.choice(string.letters)
        complement = Randomizer.letters_complement(character)
        expected = '+'
        text = Randomizer.letters() + character * random.randint(1,100) + Randomizer.letters()
        metacharacter = Quantifier.one_or_more
        self.assertEqual(expected, metacharacter)
        expression = character + metacharacter
        self.assertIsNone(re.search(expression, complement))
        self.assertIsNotNone(re.search(expression, text))
        return

    def test_zero_or_more(self):
        """
        Does it return the kleene star?
        """
        expected = '*'
        metacharacter = Quantifier.zero_or_more
        self.assertEqual(expected, metacharacter)
        substring = Randomizer.letters()
        text = Randomizer.letters()
        complement = text + Randomizer.letters_complement(substring)
        expression = text + "(" + substring + ")" + metacharacter
        text_1 = text + substring * random.randint(0, 10) + Randomizer.letters()
        self.assertIsNotNone(re.search(expression, complement))
        self.assertIsNotNone(re.search(expression, text_1))
        return

    def test_zero_or_one(self):
        """
        Does it return the zero-or-one quantifier?
        """
        expected = '?'
        metacharacter = Quantifier.zero_or_one
        self.assertEqual(expected, metacharacter)
        substring = Randomizer.letters()
        text = Randomizer.letters()
        expression = text +  "(" + substring + ")" + metacharacter
        text_1 = text + substring * Randomizer.integer()
        text_2 = text + substring * Randomizer.integer()
        self.assertIsNotNone(re.search(expression, text_1))
        self.assertEqual(re.search(expression, text_2).groups()[0], substring)
        return

    def test_exactly(self):
        """
        Does it return the repetition suffix?
        """
        repetitions = Randomizer.integer(minimum=1, maximum=5)
        repeater = Randomizer.letters()
        expected = "{" + "{0}".format(repetitions) + "}"
        quantifier = Quantifier.exactly(repetitions)
        self.assertEqual(expected, quantifier)
        expression = "(" + repeater + ")" + quantifier
        text = Randomizer.letters() + repeater * (repetitions + Randomizer.integer(minimum=0))
        self.assertIsNotNone(re.search(expression, text))
        self.assertEqual(re.search(expression, text).groups(), (repeater,))
        return

    def test_m_to_n(self):
        """
        Does it return the expression to match m-to-n repetitions
        """
        m = Randomizer.integer(minimum=5)
        n = Randomizer.integer(minimum=m+1)
        substring = Randomizer.letters()
        quantifier = Quantifier.m_to_n(m,n)
        expression = '(' + substring + ')' + quantifier
        self.assertEqual("{" + str(m) + ',' + str(n) + '}',quantifier)
        text = Randomizer.letters() + substring * Randomizer.integer(m, n)
        complement = (Randomizer.letters_complement(substring) +
                      substring * Randomizer.integer(0,m-1))
        too_many = substring * Randomizer.integer(n+1, n*2)
        self.assertIsNotNone(re.search(expression, text))
        self.assertIsNone(re.search(expression, complement))
        self.assertEqual(re.search(expression, too_many).groups(), (substring,))
        return



class TestBoundaries(unittest.TestCase):
    def test_word_boundary(self):
        """
        Does it add word-boundaries to the expression
        """
        word = Randomizer.letters()
        expected = r'\b' + word + r'\b'
        expression = Boundaries.word(word)
        bad_word = word + Randomizer.letters()
        text = ' '.join([Randomizer.letters(),word,Randomizer.letters()])
        self.assertIsNone(re.search(expression, bad_word))
        self.assertIsNotNone(re.search(expression, text))
        return

    def test_string_boundary(self):
        """
        Does it add boundaries to match a whole line?
        """
        substring = Randomizer.letters()
        expression = Boundaries.string(substring)
        expected = "^" + substring + "$"
        self.assertEqual(expected, expression)
        self.assertIsNotNone(re.search(expression, substring))
        self.assertIsNone(re.search(expression, ' ' + substring))
        return

    def test_string_start(self):
        """
        Does it have return a string start metacharacter?
        """
        metacharacter = Boundaries.string_start
        expected = '^'
        self.assertEqual(expected, metacharacter)
        word = Randomizer.letters()
        expression = Boundaries.string_start + word
        text = word + Randomizer.letters()
        self.assertIsNotNone(re.search(expression, text))
        self.assertIsNone(re.search(expression, " " + text))
        return

    def test_string_end(self):
        """
        Does it return the end of string metacharacter?
        """
        metacharacter = Boundaries.string_end
        word = Randomizer.letters()
        expression = word + metacharacter
        text = Randomizer.letters() + word
        self.assertIsNotNone(re.search(expression, text))
        self.assertIsNone(re.search(expression, text + Randomizer.letters()))
        return


class TestNumbers(unittest.TestCase):
    def test_decimal_point(self):
        """
        Does it return a decimal point literal?
        """
        metacharacter = Numbers.decimal_point
        test = random.uniform(0,100)
        self.assertIsNotNone(re.search(metacharacter, str(test)))
        self.assertIsNone(re.search(metacharacter, Randomizer.letters()))
        return

    def test_digit(self):
        """
        Does it return the digit character class?
        """
        metacharacter = Numbers.digit
        test = Randomizer.integer(maximum=9)
        self.assertIsNotNone(re.search(metacharacter, str(test)))
        self.assertIsNone(re.search(metacharacter, Randomizer.letters()))
        return

    def test_non_digit(self):
        """
        Does it return the anything-but-a-digit metacharacter?
        """
        metacharacter = Numbers.non_digit
        test = str(Randomizer.integer(maximum=9))
        self.assertIsNone(re.search(metacharacter, test))
        return

    def test_non_zero(self):
        """
        Does it return an expression to match 1-9 only?
        """
        expression = Numbers.non_zero
        test = str(random.choice(range(1,10)))
        self.assertIsNotNone(re.search(expression, test))
        self.assertIsNone(re.search(expression, '0'))
        return

    def test_single_digit(self):
        """
        Does it return an expression to match only one digit?
        """
        expression = Numbers.single_digit
        test = str(Randomizer.integer(maximum=9))
        two_many = str(Randomizer.integer(minimum=10))
        self.assertIsNotNone(re.search(expression, test))
        self.assertIsNone(re.search(expression, two_many))
        return

    def test_two_digits(self):
        """
        Does it return an expression to match exactly two digits?
        """
        expression = Numbers.two_digits
        test = str(Randomizer.integer(minimum=10,maximum=99))
        fail = random.choice([str(Randomizer.integer(0,9)), str(Randomizer.integer(100,1000))])
        self.assertIsNotNone(re.search(expression, test))
        self.assertIsNone(re.search(expression, fail))


# exceptions
L_BRACKET = r"\["
R_BRACKET = r"\]"

# operators
OR = "|"

# string help

#anything and everything
ANYTHING = r"."
EVERYTHING = ANYTHING + Quantifier.zero_or_more

# numbers
ONE_HUNDREDS = Boundaries.word("1" + Numbers.digit + Numbers.digit)
NATURAL = Numbers.digit + Quantifier.one_or_more

INTEGER = (Group.not_preceded_by(Numbers.decimal_point) +  "-" + Quantifier.zero_or_one + NATURAL + 
           Group.not_followed_by(Numbers.decimal_point))

FLOAT = "-" + Quantifier.zero_or_one + NATURAL + Numbers.decimal_point + NATURAL
REAL = Group.group(FLOAT + OR + INTEGER)
HEX = CharacterClass.character_class(string.hexdigits)
HEXADECIMALS = HEX + Quantifier.one_or_more

SPACE = r"\s"
SPACES = SPACE + Quantifier.one_or_more
NOT_SPACE = r'\S'
NOT_SPACES = NOT_SPACE + Quantifier.one_or_more
OPTIONAL_SPACES = SPACE + Quantifier.zero_or_more

# common constants
DASH = "-"
LETTER = CharacterClass.character_class(characters=string.ascii_letters)
LETTERS = LETTER + Quantifier.one_or_more
OPTIONAL_LETTERS = LETTER + Quantifier.zero_or_more

# SPECIAL CASES
# NETWORKING
DOT = Numbers.decimal_point
OCTET = Group.group(expression=OR.join([Numbers.single_digit, Numbers.two_digits, ONE_HUNDREDS,
                         Boundaries.word("2[0-4][0-9]"), Boundaries.word("25[0-5]")]))

IP_ADDRESS = DOT.join([OCTET] * 4)

# from commons.expressions
MAC_ADDRESS_NAME = "mac_address"
HEX_PAIR =  HEX + Quantifier.exactly(2)
MAC_ADDRESS = Group.named(name=MAC_ADDRESS_NAME,
                                 expression=":".join([HEX_PAIR] * 6))
