The OatBran
===========
.. currentmodule:: apcommand.commons.oatbran
Oat Bran helps with regular expressions. Names are uppercased to avoid keyword clashes
::

    # the class-based expressions are mostly for organization
    # but sometimes they're just too clunky
    LEFT_BRACKET = '['
    RIGHT_BRACKET = ']'
    OR = '|'
    
    



Formal Definition
-----------------

These are the basic building blocks of regular expressions.

.. csv-table:: Formal Definition
   :header: Name,Symbol

   empty_string,:math:`\varepsilon`
   alternative (OR),:math:`|`
   kleene_star, :math:`*`

.. autosummary::
   :toctree: api

   FormalDefinition.empty_string
   FormalDefinition.alternative
   FormalDefinition.OR
   FormalDefinition.kleene_star



Groups
------

.. autosummary::
   :toctree: api

   Group
   Group.named
   Group.not_followed_by
   Group.not_preceded_by



Quantifiers
-----------

.. autosummary::
   :toctree: api

   Quantifier
   Quantifier.one_or_more
   Quantifier.zero_or_more
   Quantifier.zero_or_one
   Quantifier.exactly
   Quantifier.m_to_n



Character Classes
-----------------

A helper with character classes.

.. autosummary::
   :toctree: api

   CharacterClass
   CharacterClass.alpha_num
   CharacterClass.alpha_nums
   CharacterClass.character_class
   CharacterClass.not_in      



Boundaries
----------

.. autosummary::
   :toctree: api

   Boundaries
   Boundaries.string_start
   Boundaries.string_end
   Boundaries.word
   Boundaries.string
   


Numbers
-------

The numbers are broken up into types based on those listed `here <http://mathworld.wolfram.com/CountingNumber.html>`_. I was originally using the more `traditional number types <http://en.wikipedia.org/wiki/List_of_types_of_numbers>`_ but I keep forgetting which ones have zero in them so I will work with just positive/negative, non-positive/non-negative, and integer/real.



.. autosummary::
   :toctree: api

   Numbers
   Numbers.decimal_point
   Numbers.digit
   Numbers.digits
   Numbers.non_digit
   Numbers.non_zero_digit
   Numbers.single_digit
   Numbers.two_digits
   Numbers.one_hundreds
   Numbers.natural
   


.. autosummary::
   :toctree: api

   TestQuantifier.test_one_or_more
   TestQuantifier.test_zero_or_more
   
::

    # exceptions
    L_BRACKET = r"\["
    R_BRACKET = r"\]"
    
    # operators
    OR = "|"
    
    # string help
    
    #anything and everything
    ANYTHING = r"."
    EVERYTHING = Quantifier.zero_or_more(ANYTHING)
    
    # numbers
    
    NATURAL = Numbers.digit + Quantifier.one_or_more
    
    INTEGER = (Group.not_preceded_by(Numbers.decimal_point) +  Quantifier.zero_
    or_one('-') + NATURAL + 
               Group.not_followed_by(Numbers.decimal_point))
    
    FLOAT = Quantifier.zero_or_one('-') + NATURAL + Numbers.decimal_point + NAT
    URAL
    REAL = Group.group(FLOAT + OR + INTEGER)
    HEX = CharacterClass.character_class(string.hexdigits)
    HEXADECIMALS = HEX + Quantifier.one_or_more
    
    SPACE = r"\s"
    SPACES = SPACE + Quantifier.one_or_more
    NOT_SPACE = r'\S'
    NOT_SPACES = NOT_SPACE + Quantifier.one_or_more
    OPTIONAL_SPACES = Quantifier.zero_or_more(SPACE)
    
    # common constants
    DASH = "-"
    LETTER = CharacterClass.character_class(characters=string.ascii_letters)
    LETTERS = LETTER + Quantifier.one_or_more
    OPTIONAL_LETTERS = Quantifier.zero_or_more(LETTER)
    
    # SPECIAL CASES
    # NETWORKING
    DOT = Numbers.decimal_point
    OCTET = Group.group(expression=OR.join([Numbers.single_digit, Numbers.two_d
    igits, Numbers.one_hundreds,
                             Boundaries.word("2[0-4][0-9]"), Boundaries.word("2
    5[0-5]")]))
    
    IP_ADDRESS = DOT.join([OCTET] * 4)
    
    # from commons.expressions
    MAC_ADDRESS_NAME = "mac_address"
    HEX_PAIR =  HEX + Quantifier.exactly(2)
    MAC_ADDRESS = Group.named(name=MAC_ADDRESS_NAME,
                                     expression=":".join([HEX_PAIR] * 6))
    
    


(?<!ULPXdDcbbsWJXijdQedVRFNSUHEWsgFVqqqyeKggZIleKBkpLhOPvEDaafJBjjyuvWCChgqavwMNDqKZj)
nBSiqlJoHvbvwEYqlYRAjAIUZMmmjQeegLPRpZBlNRHRKvPIhPBOPnapQLW
ULPXdDcbbsWJXijdQedVRFNSUHEWsgFVqqqyeKggZIleKBkpLhOPvEDaafJBjjyuvWCChgqavwMNDqKZjnBSiqlJoHvbvwEYqlYRAjAIUZMmmjQeegLPRpZBlNRHRKvPIhPBOPnapQLW
+
-57.42
(?P<integer>(?<!\.|0)-?[1-9]\d*(?!\.\d+)\b|\b0\b)
('2',)

