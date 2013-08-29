The OatBran
===========
.. currentmodule:: apcommand.commons.oatbran
Oat Bran helps with regular expressions. Names are uppercased to avoid keyword clashes


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
   Quantifier.exactly



Character Classes
-----------------

A helper with character classes.

.. autosummary::
   :toctree: api

   CharacterClass
   CharacterClass.character_class
   CharacterClass.not_in      



Boundaries
----------

.. autosummary::
   :toctree: api

   Boundaries
   Boundaries.word
   Boundaries.string
   


Numbers
-------

.. autosummary::
   :toctree: api

   Numbers



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
    EVERYTHING = ANYTHING + Quantifier.zero_or_more
    
    # numbers
    ONE_HUNDREDS = Boundaries.word("1" + Numbers.digit + Numbers.digit)
    NATURAL = Numbers.digit + Quantifier.one_or_more
    
    INTEGER = (Group.not_preceded_by(Numbers.decimal_point) +  "-" + Quantifier
    .zero_or_one + NATURAL + 
               Group.not_followed_by(Numbers.decimal_point))
    
    FLOAT = "-" + Quantifier.zero_or_one + NATURAL + Numbers.decimal_point + NA
    TURAL
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
    OCTET = Group.group(expression=OR.join([Numbers.single_digit, Numbers.two_d
    igits, ONE_HUNDREDS,
                             Boundaries.word("2[0-4][0-9]"), Boundaries.word("2
    5[0-5]")]))
    
    IP_ADDRESS = DOT.join([OCTET] * 4)
    
    # from commons.expressions
    MAC_ADDRESS_NAME = "mac_address"
    HEX_PAIR =  HEX + Quantifier.exactly(2)
    MAC_ADDRESS = Group.named(name=MAC_ADDRESS_NAME,
                                     expression=":".join([HEX_PAIR] * 6))
    
    


(?<!bXuQveMnZEDuPcCZDrAyMJqRttzcrcHysrNpwjCcRarwGdvmwTICWJAzQVjfyZZAiNlhYIOvUFBSdgMxOznWmxEv)
etnAlQneYXZnNzrYRaFVnceTtZQbgpxnfvhBBPtkvkMtbHxCHbojoNdPyAnlkItnzvLfxMNiHDWlgv
bXuQveMnZEDuPcCZDrAyMJqRttzcrcHysrNpwjCcRarwGdvmwTICWJAzQVjfyZZAiNlhYIOvUFBSdgMxOznWmxEvetnAlQneYXZnNzrYRaFVnceTtZQbgpxnfvhBBPtkvkMtbHxCHbojoNdPyAnlkItnzvLfxMNiHDWlgv

