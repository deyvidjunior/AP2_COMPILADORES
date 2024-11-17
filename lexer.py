from token_types import TokenType, Token

class Lexer:
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1
        
        self.keywords = {
            'program': TokenType.PROGRAM,
            'begin': TokenType.BEGIN,
            'end': TokenType.END,
            'var': TokenType.VAR,
            'integer': TokenType.INTEGER,
            'while': TokenType.WHILE,
            'do': TokenType.DO,
            'read': TokenType.READ,
            'write': TokenType.WRITE
        }

    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        
        self.tokens.append(Token(TokenType.EOF, "", self.line))
        return self.tokens

    def scan_token(self):
        c = self.advance()
        
        if c.isspace():
            if c == '\n':
                self.line += 1
            return

        if c.isdigit():
            self.number()
            return

        if c.isalpha():
            self.identifier()
            return

        match c:
            case '+': self.add_token(TokenType.PLUS)
            case '-': self.add_token(TokenType.MINUS)
            case '*': self.add_token(TokenType.MULTIPLY)
            case ';': self.add_token(TokenType.SEMICOLON)
            case ':':
                if self.match('='):
                    self.add_token(TokenType.ASSIGN)
                else:
                    self.add_token(TokenType.COLON)
            case '.': self.add_token(TokenType.DOT)
            case ',': self.add_token(TokenType.COMMA)
            case '(': self.add_token(TokenType.LPAREN)
            case ')': self.add_token(TokenType.RPAREN)
            case '<':
                if self.match('='):
                    self.add_token(TokenType.LESS_EQUAL)
            case _:
                if not c.isspace():
                    raise SyntaxError(f"Unexpected character at line {self.line}")

    def identifier(self):
        while not self.is_at_end() and (self.peek().isalnum() or self.peek() == '_'):
            self.advance()

        text = self.source[self.start:self.current].lower()
        print(f"Identificador encontrado: '{text}'")  # Debug
        type = self.keywords.get(text, TokenType.IDENTIFIER)
        print(f"Tipo do token: {type}")  # Debug
        self.add_token(type)

    def number(self):
        while not self.is_at_end() and self.peek().isdigit():
            self.advance()
        self.add_token(TokenType.NUMBER)

    def is_at_end(self):
        return self.current >= len(self.source)

    def advance(self):
        self.current += 1
        return self.source[self.current - 1]

    def peek(self):
        if self.is_at_end():
            return '\0'
        return self.source[self.current]

    def match(self, expected):
        if self.is_at_end() or self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def add_token(self, type):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, self.line))