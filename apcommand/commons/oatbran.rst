The OatBran
===========
.. currentmodule:: apcommand.commons.oatbran
Oat Bran helps with regular expressions. Names are uppercased to avoid keyword clashes


.. autosummary::
   :toctree: api

   OatBranGroup
   OatBranGroup.named
   OatBranGroup.not_followed_by
   OatBranGroup.not_preceded_by



OatBranClass
------------

A helper with character classes.

.. autosummary::
   :toctree: api

   OatBranClass
   OatBranClass.character_class
   OatBranClass.not_in      

.. code-block:: python

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
    
    INTEGER = (OatBranGroup.not_preceded_by(DECIMAL_POINT) +  "-" + ZERO_OR_ONE
     + NATURAL + 
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
    OCTET = OatBranGroup.group(expression=OR.join([SINGLE_DIGIT, TWO_DIGITS, ON
    E_HUNDREDS,
                             WORD_BOUNDARY("2[0-4][0-9]"), WORD_BOUNDARY("25[0-
    5]")]))
    
    IP_ADDRESS = DOT.join([OCTET] * 4)
    
    # from commons.expressions
    MAC_ADDRESS_NAME = "mac_address"
    HEX_PAIR = HEX + EXACTLY.format(2)
    MAC_ADDRESS = OatBranGroup.named(name=MAC_ADDRESS_NAME,
                                     expression=":".join([HEX_PAIR] * 6))
    
    



