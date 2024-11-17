from enum import Enum, auto

class TokenType(Enum):
    # Keywords
    PROGRAM = auto()
    BEGIN = auto()
    END = auto()
    VAR = auto()
    INTEGER = auto()
    WHILE = auto()
    DO = auto()
    READ = auto()
    WRITE = auto()
    
    # Symbols
    PLUS = auto()          # +
    MINUS = auto()         # -
    MULTIPLY = auto()      # *
    LESS_EQUAL = auto()    # <=
    ASSIGN = auto()        # :=
    SEMICOLON = auto()     # ;
    COLON = auto()         # :
    DOT = auto()           # .
    COMMA = auto()         # ,
    LPAREN = auto()        # (
    RPAREN = auto()        # )
    
    # Others
    IDENTIFIER = auto()
    NUMBER = auto()
    EOF = auto()

class Token:
    def __init__(self, type, lexeme, line):
        self.type = type
        self.lexeme = lexeme
        self.line = line

    def __str__(self):
        return f"Token({self.type}, '{self.lexeme}', line={self.line})"