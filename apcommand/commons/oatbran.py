
import string


# the class-based expressions are mostly for organization
# but sometimes they're just too clunky
LEFT_BRACKET = '['
RIGHT_BRACKET = ']'



class FormalDefinition(object):
    """
    The basic operators and elements of a regular expression
    """
    empty_string = '^$'
    alternative = '|'
    OR = alternative
    kleene_star = "*"


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
    def followed_by(suffix):
        """
        Creates the expression to match if followed by the suffix
        """
        return "(?={0})".format(suffix)

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
    def preceded_by(prefix):
        """
        Creates a look-behind expression

        :param:

         - `prefix`: an expression of fixed-order (no quantifiers or alternatives of different length)
        """
        return "(?<={0})".format(prefix)
    
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

    @staticmethod
    def one_or_more(pattern):
        """
        Adds the one-or-more quantifier to the end of the pattern.
        """
        return '{0}+'.format(pattern)    

    @staticmethod
    def zero_or_one(pattern):
        """
        Adds the zero-or-one quantifier to the pattern
        """
        return '{0}?'.format(pattern)

    @staticmethod
    def exactly(repetitions):
        """
        Creates suffix to match source repeated exactly n times

        :param:

         - `repetitions`: number of times pattern has to repeat to match
        """
        return "{{{0}}}".format(repetitions)

    @staticmethod
    def zero_or_more(pattern):
        """
        Adds the kleene star to the pattern

        :return: pattern*
        """
        return "{0}*".format(pattern)

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
    alpha_nums = Quantifier.one_or_more(alpha_num)
    digit = r'\d'
    non_digit = r'\D'
    non_zero_digit = r"[1-9]"

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


class CommonPatterns(object):
    """
    The common patterns that were leftover
    """
    __slots__ = ()
    #anything and everything
    anything = r"."
    everything = Quantifier.zero_or_more(anything)
    letter = CharacterClass.character_class(characters=string.ascii_letters)
    letters = Quantifier.one_or_more(letter)
    optional_letters = Quantifier.zero_or_more(letter)
    space = r'\s'
    spaces = Quantifier.one_or_more(space)
    optional_spaces = Quantifier.zero_or_more(space)
    not_space = r'\S'
    not_spaces = Quantifier.one_or_more(not_space)


class Numbers(object):
    """
    A class to hold number-related expressions
    """
    __slots__ = ()
    
    decimal_point = r'\.'
    single_digit = Boundaries.word(CharacterClass.digit)
    digits = Quantifier.one_or_more(CharacterClass.digit)
    two_digits = Boundaries.word(CharacterClass.non_zero_digit + CharacterClass.digit)
    one_hundreds = Boundaries.word("1" + CharacterClass.digit * 2)
    optional_digits = Quantifier.zero_or_more(CharacterClass.digit)
    # python considers string-start and whitespace to be different lengths
    # so to avoid '.' (which is a word-boundary character) and use line-starts and ends
    # and whitespace requires four alternatives
    START_PREFIX = Group.preceded_by(Boundaries.string_start)
    END_SUFFIX = Group.followed_by(Boundaries.string_end)
    SPACE_PREFIX = Group.preceded_by(CommonPatterns.space)
    SPACE_SUFFIX = Group.followed_by(CommonPatterns.space)
    # Zero
    ZERO = '0'
    zero = (START_PREFIX + ZERO + END_SUFFIX +FormalDefinition.OR +
            START_PREFIX + ZERO + SPACE_SUFFIX +FormalDefinition.OR +
            SPACE_PREFIX + ZERO + END_SUFFIX +FormalDefinition.OR +
            SPACE_PREFIX + ZERO + SPACE_SUFFIX)
    # positive integer
    z_plus = CharacterClass.non_zero_digit + optional_digits
    positive_integer = (START_PREFIX + z_plus + END_SUFFIX +FormalDefinition.OR +
                        START_PREFIX + z_plus + SPACE_SUFFIX +FormalDefinition.OR +
                        SPACE_PREFIX + z_plus + END_SUFFIX +FormalDefinition.OR +
                        SPACE_PREFIX + z_plus + SPACE_SUFFIX )

    nonnegative_integer = (Group.not_preceded_by(decimal_point +FormalDefinition.OR + '0') +
                               CharacterClass.non_zero_digit + optional_digits +
                               r'\b' +FormalDefinition.OR + 
                               Boundaries.word('0'))
    
    integer = (Group.not_preceded_by(decimal_point +FormalDefinition.OR + '0') +
                               Quantifier.zero_or_one('-') + 
                               CharacterClass.non_zero_digit + optional_digits +
                               r'\b' +FormalDefinition.OR + 
                               Boundaries.word('0'))

    real = (Group.not_preceded_by(decimal_point +FormalDefinition.OR + '0') +
                               Quantifier.zero_or_one('-') + 
                               CharacterClass.digit + optional_digits +
                               '.' + optional_digits + 
                               r'\b' ) +FormalDefinition.OR + integer
    
    HEX = CharacterClass.character_class(string.hexdigits)
    hexadecimal = Quantifier.one_or_more(HEX)



class Networking(object):
    """
    Holds expressions to help with networking-related text.
    """
    __slots__ = ()
    octet = Group.group(expression=FormalDefinition.OR.join([Numbers.single_digit,
                                                             Numbers.two_digits,
                                                             Numbers.one_hundreds,
                                                             Boundaries.word("2[0-4][0-9]"),
                                                             Boundaries.word("25[0-5]")]))

    dot = Numbers.decimal_point

    ip_address = dot.join([octet] * 4)

    hex_pair =  Numbers.HEX + Quantifier.exactly(2)
    mac_address = ":".join([hex_pair] * 6)





# python standard library
import unittest
import random
import re

#third-party
try:
    import numpy.random as nrandom
except ImportError:
    pass
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

    def test_followed_by(self):
        """
        Does it match strings followed by a pattern?
        """
        body = Randomizer.letters()
        sub_string = Randomizer.letters()
        suffix = Randomizer.letters()
        text = body + sub_string + suffix
        name = 'followed'
        expression = Group.named(name,
                                 sub_string + Group.followed_by(suffix))
        match = re.search(expression, text)
        self.assertEqual(match.group(name), sub_string)

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

    def test_preceded_by(self):
        "Does it match a substring with a prefix?"
        name = 'preceded'
        body = Randomizer.letters()
        sub_string = Randomizer.letters()
        prefix = Randomizer.letters()
        expression = Group.named(name,
                                 Group.preceded_by(prefix) + sub_string)
        text = body + prefix + sub_string
        match = re.search(expression, text)
        self.assertEqual(match.group(name),
                         sub_string)

    def test_not_preceded_by(self):
        '''
        Does it create a negative look-behind expression?
        '''
        prefix = Randomizer.letters()
        expr = Group.not_preceded_by(prefix)
        self.assertEqual(L_PERL_GROUP + "<!" + prefix + R_GROUP,
                         expr)
        text = Randomizer.letters(minimum=5)

        is_preceded_by = prefix + text
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
        non_alpha = random.choice(string.punctuation.replace('_', ''))
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

        text = Randomizer.letters() + character * random.randint(1,100) + Randomizer.letters()
        expression = character + '+'
        self.assertIsNone(re.search(expression, complement))
        self.assertIsNotNone(re.search(expression, text))
        return

    def test_zero_or_more(self):
        """
        Does it return the kleene star?
        """
        substring = Randomizer.letters()
        text = Randomizer.letters()
        complement = text + Randomizer.letters_complement(substring)
        expression = text + Quantifier.zero_or_more('(' + substring + ')')
        text_1 = text + substring * random.randint(0, 10) + Randomizer.letters()
        self.assertIsNotNone(re.search(expression, complement))
        self.assertIsNotNone(re.search(expression, text_1))
        return

    def test_zero_or_one(self):
        """
        Does it return the zero-or-one quantifier?
        """
        substring = Randomizer.letters()
        text = Randomizer.letters()
        expression = text +  Quantifier.zero_or_one("(" + substring + ")")
        text_1 = text + substring * random.randint(1,100)
        text_2 = text + substring * random.randint(1,100)
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
        metacharacter = CharacterClass.digit
        test = Randomizer.integer(maximum=9)
        self.assertIsNotNone(re.search(metacharacter, str(test)))
        self.assertIsNone(re.search(metacharacter, Randomizer.letters()))
        return

    def test_non_digit(self):
        """
        Does it return the anything-but-a-digit metacharacter?
        """
        metacharacter = CharacterClass.non_digit
        test = str(Randomizer.integer(maximum=9))
        self.assertIsNone(re.search(metacharacter, test))
        return

    def test_non_zero(self):
        """
        Does it return an expression to match 1-9 only?
        """
        expression = CharacterClass.non_zero_digit
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
        return

    def test_one_hundreds(self):
        """
        Does it match values from 100-199?
        """
        number = "{0}".format(random.randint(100,199))
        low_number = str(random.randint(-99,99))
        high_number = str(random.randint(200,500))
        float_number = str(random.uniform(100,199))
        text = Randomizer.letters() + str(random.randint(100,199))
        name = 'onehundred'
        expression = re.compile(Group.named(name,
                                            Numbers.one_hundreds))
        self.assertIsNotNone(re.search(Numbers.one_hundreds, number))
        self.assertIsNone(re.search(Numbers.one_hundreds, low_number))
        self.assertIsNone(re.search(Numbers.one_hundreds, high_number))
        # it only checks word boundaries and the decimal point is a boundary
        self.assertIsNotNone(re.search(Numbers.one_hundreds, float_number))
        # it needs a word boundary so letters smashed against it will fail
        self.assertIsNone(re.search(Numbers.one_hundreds, text))
        return

    def test_digits(self):
        "Does it match one or more digits?"
        expression = Group.named(name='digits', expression=Numbers.digits)
        first = "{0}".format(random.randint(0,9))
        rest = str(random.randint(0,1000))
        test = first + rest
        self.assertIsNotNone(re.search(expression, test))
        match = re.search(expression, test)
        self.assertEqual(match.group('digits'), test)
        mangled = Randomizer.letters() + test + Randomizer.letters()
        match = re.search(expression, mangled)
        self.assertEqual(match.group('digits'), test)
        return

    def test_zero(self):
        "Does it match zero by itself?"
        name = 'zero'
        expression = Group.named(name,
                                 Numbers.zero)
        prefix = random.choice(['', ' '])
        suffix = random.choice(['', ' '])
        zero = '0'
        text = prefix + zero + suffix
        match = re.search(expression, text)
        self.assertEqual(match.group(name), zero)
        self.assertIsNone(re.search(expression, str(random.randint(1,100))))
        return
        

    def test_positive_integers(self):
        'Does it only match 1,2,3,...?'
        name = 'positiveintegers'
        expression = Group.named(name,
                                 Numbers.positive_integer)
        regex = re.compile(expression)
        # zero should fail
        self.assertIsNone(regex.search('0' ))

        # positive integer (without sign) should match
        first_digit = str(nrandom.randint(1,9))
        positive_integer = first_digit + ''.join(str(i) for i in nrandom.random_integers(1,9,
                                                                           size=nrandom.randint(100)))
        match = regex.search(positive_integer)
        self.assertEqual(match.group(name), positive_integer)

        # negative integer should fail
        negation = '-' + positive_integer
        self.assertIsNone(regex.search(negation))

        # surrounding white space should be trimmed off
        spaces = " " * nrandom.randint(100) + positive_integer + ' ' * nrandom.randint(100)
        match = regex.search(spaces)
        self.assertEqual(match.group(name), positive_integer)

        # leading zero should fail
        leading_zeros = '0' * nrandom.randint(1,100) + positive_integer
        self.assertIsNone(regex.search(leading_zeros))
        return

    def test_integers(self):
        """
        Does it match positive and negative integers?
        """
        name = 'integer'
        expression = Group.named(name, Numbers.integer)
        regex = re.compile(expression)
        # 0 alone should match
        zero = '0'
        match = regex.search(zero)
        self.assertEqual(match.group(name), zero)

        # positive_integers should match
        first_digit = str(nrandom.randint(1,9))
        positive = first_digit +''.join(str(i) for i in nrandom.random_integers(0,9, nrandom.randint(1, 100)))
        match = regex.search(positive)
        self.assertEqual(match.group(name), positive)

        # negatives should match
        negative = '-' + positive
        match = regex.search(negative)
        self.assertEqual(match.group(name), negative)

        # white space boundaries should work too
        number = nrandom.choice(('','-')) + positive
        text = " " * nrandom.randint(10) + number  + ' ' * nrandom.randint(10)
        match = regex.search(text)
        self.assertEqual(match.group(name), number)

        # punctuation should work (like for csvs)
        text = number + ','
        match = regex.search(text)
        self.assertEqual(match.group(name), number)

        # match prefix to decimal points
        # this is not really what I wanted but otherwise it's hard to use in text
        text = number + '.' + str(nrandom.randint(100))
        match = regex.search(text)
        self.assertEqual(match.group(name), number)
        return

    def test_nonnegative_integer(self):
        """
        Does it match positive integers and 0?
        """
        name = 'nonnegative'
        expression = Group.named(name,
                                 Numbers.nonnegative_integer)
        regex = re.compile(expression)
        number = str(nrandom.randint(1,9)) + str(nrandom.randint(1000))
        match = regex.search(number)
        self.assertEqual(number, match.group(name))

        # should match 0
        zero = '0'
        match = regex.search(zero)
        self.assertEqual(match.group(name), zero)

        # should not match negative
        # but, to allow it in text, it will grab the integer to the right
        # in other words, it assumes the `-` is part of a sentence but not part of the number
        negation = '-' + number
        match = regex.search(negation)
        self.assertEqual(match.group(name), number)
        return

    def assert_match(self, regex, text, name, expected):
        match = regex.search(text)
        self.assertEqual(match.group(name), expected)
        return

    def test_real(self):
        """
        Does it match floating-point numbers?
        """
        name = 'real'
        expression = Group.named(name,
                                 Numbers.real)
        regex = re.compile(expression)
        # does it match 0?
        zero = '0'
        self.assert_match(regex, zero, name, zero)

        # does it match a leading 0?
        number = '0.' + str(nrandom.randint(100))
        self.assert_match(regex, number, name, number)

        # does it match a whole decimal
        number = str(nrandom.randint(1,100)) + '.' + str(nrandom.randint(100))
        self.assert_match(regex, number, name, number)

        # what about positive and negative?
        number = (random.choice(('', '-')) + str(nrandom.randint(100)) +
                  random.choice(('', '.')) + str(nrandom.randint(100)))
        text = ' ' * nrandom.randint(5) + number + ' ' * nrandom.randint(5)
        self.assert_match(regex, text, name, number)

        # what happens if it comes at the end of a sentence?
        number = (random.choice(('', '-')) + str(nrandom.randint(100)) +
                  random.choice(('', '.')) + str(nrandom.randint(100)))
        text = number + '.'
        self.assert_match(regex, text, name, number)
        return

    def test_hexadecimal(self):
        """
        Does it match hexadecimal numbers?
        """
        name = 'hexadecimal'
        number = ''.join((random.choice(string.hexdigits) for char in xrange(random.randint(1,100))))
        non_hex = 'IJKLMNOPQRSTUVWXYZ'
        text = random.choice(non_hex) + number + non_hex
        expression = re.compile(Group.named(name,
                                 Numbers.hexadecimal))
        match = expression.search(text)
        self.assertEqual(match.group(name), number)
        return



class TestFormalDefinition(unittest.TestCase):
    def test_empty_string(self):
        "Does it match only an empty string?"
        name = 'empty'
        expression = Group.named(name,
                                 FormalDefinition.empty_string)
        empty = ''
        not_empty = Randomizer.letters()
        match = re.search(expression, empty)
        self.assertEqual(empty, match.group(name))
        self.assertIsNone(re.search(expression, not_empty))
        return

    def test_alternation(self):
        """
        Does it match alternatives?
        """
        name = 'or'
        # this might fail if one of the terms is a sub-string of another
        # and the longer term is chosen as the search term
        terms = [Randomizer.letters() for term in range(random.randint(10, 100))]
        expression = Group.named(name,
                                 FormalDefinition.alternative.join(terms))
        test = terms[random.randrange(len(terms))]
        match = re.search(expression, test)
        self.assertEqual(test, match.group(name))
        return

    def test_kleene_star(self):
        """
        Does it match zero or more of something?
        """
        name = 'kleene'
        term = random.choice(string.letters)
        expression = Group.named(name,
                                 term + FormalDefinition.kleene_star)
        test = term * random.randint(0, 100)
        match = re.search(expression, test)
        self.assertEqual(test, match.group(name))
        return


class TestNetworking(unittest.TestCase):
    def test_octet(self):
        """
        Does it match a valid octet?
        """
        name = 'octet'
        expression = re.compile(Group.named(name,
                                            Networking.octet))
        for t1 in '198 10 1 255'.split():
            match = expression.search(t1)
            self.assertEqual(t1, match.group(name))
        bad_octet = random.randint(256, 999)
        self.assertIsNone(expression.search(str(bad_octet)))
        return

    def test_ip_address(self):
        """
        Does it match a valid ip address?
        """
        name = 'ipaddress'
        expression = re.compile(Group.named(name,
                                            Networking.ip_address))
        for text in '192.168.0.1 10.10.10.2 76.83.100.234'.split():
            match = expression.search(text)
            self.assertEqual(match.group(name), text)
        for bad_ip in "10.10.10 12.9.49.256 ape".split():
            self.assertIsNone(expression.search(bad_ip))
        return

    def test_mac_address(self):
        name = 'macaddress'
        expression = re.compile(Group.named(name,
                                            Networking.mac_address))
        text = 'f8:d1:11:03:12:58'
        self.assertEqual(expression.search(text).group(name),
                         text)
        return
