from token_types import TokenType

class SemanticError(Exception):
    pass

class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.next_address = 0
    
    def declare(self, name):
        if name in self.symbols:
            raise SemanticError(f"Variable '{name}' already declared")
        self.symbols[name] = self.next_address
        self.next_address += 1
        return self.symbols[name]
    
    def get_address(self, name):
        if name not in self.symbols:
            raise SemanticError(f"Variable '{name}' not declared")
        return self.symbols[name]

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        self.symbols = SymbolTable()
        self.next_label = 1
        self.code = []

    def programa(self):
        # Início do programa
        self.emit("INPP")
        
        # Cabeçalho do programa
        self.consume(TokenType.PROGRAM)
        self.consume(TokenType.IDENTIFIER)
        self.consume(TokenType.SEMICOLON)
        
        # Declarações de variáveis
        if self.match(TokenType.VAR):
            self.declaracao_variaveis()
        
        # Corpo do programa
        self.comando_composto()
        self.consume(TokenType.DOT)
        
        # Fim do programa
        self.emit("PARA")
        return self.code

    def declaracao_variaveis(self):
        """Processa declarações de variáveis e aloca memória"""
        num_vars = 0
        while self.check(TokenType.IDENTIFIER):
            # Primeiro identificador
            num_vars += 1
            name = self.current_token().lexeme
            addr = self.symbols.declare(name)
            self.consume(TokenType.IDENTIFIER)
            
            # Identificadores adicionais após vírgula
            while self.match(TokenType.COMMA):
                num_vars += 1
                name = self.current_token().lexeme
                addr = self.symbols.declare(name)
                self.consume(TokenType.IDENTIFIER)
            
            self.consume(TokenType.COLON)
            self.consume(TokenType.INTEGER)
            self.consume(TokenType.SEMICOLON)
        
        self.emit(f"AMEM {num_vars}")

    def comando_composto(self):
        self.consume(TokenType.BEGIN)
        self.lista_comandos()
        self.consume(TokenType.END)

    def lista_comandos(self):
        self.comando()
        while self.match(TokenType.SEMICOLON):
            self.comando()

    def comando(self):
        if self.match(TokenType.IDENTIFIER):
            self.comando_atribuicao()
        elif self.match(TokenType.WHILE):
            self.comando_while()
        elif self.match(TokenType.READ):
            self.comando_read()
        elif self.match(TokenType.WRITE):
            self.comando_write()
        elif self.check(TokenType.BEGIN):
            self.comando_composto()

    def comando_atribuicao(self):
        name = self.previous_token().lexeme
        addr = self.symbols.get_address(name)
        
        self.consume(TokenType.ASSIGN)
        self.expressao()
        self.emit(f"ARMZ {addr}")

    def comando_atribuicao(self):
        name = self.previous_token().lexeme
        addr = self.symbols.get_address(name)
        
        self.consume(TokenType.ASSIGN)
        self.expressao()
        self.emit(f"ARMZ {addr}")

    def comando_while(self):
        L1 = self.proximo_rotulo()
        L2 = self.proximo_rotulo()

        self.emit(f"L1: NADA")

        # Procesa la condición del while
        self.expressao()  # Cambiado de self.fator()

        self.emit(f"DSVF L2")

        self.consume(TokenType.DO)
        self.comando()

        self.emit(f"DSVS L1")
        self.emit(f"L2: NADA")

    def comando_read(self):
        self.consume(TokenType.LPAREN)
        name = self.current_token().lexeme
        addr = self.symbols.get_address(name)
        self.consume(TokenType.IDENTIFIER)
        self.consume(TokenType.RPAREN)
        
        self.emit("LEIT")
        self.emit(f"ARMZ {addr}")

    def comando_write(self):
        self.consume(TokenType.LPAREN)
        self.expressao()
        self.consume(TokenType.RPAREN)
        self.emit("IMPR")

    def expressao(self):
        """Processa expressões aritméticas e relacionais"""
        self.termo()
        
        while (self.match(TokenType.PLUS) or 
               self.match(TokenType.MINUS) or 
               self.match(TokenType.LESS_EQUAL)):
            
            operator = self.previous_token().type
            self.termo()
            
            if operator == TokenType.PLUS:
                self.emit("SOMA")
            elif operator == TokenType.MINUS:
                self.emit("SUBT")
            elif operator == TokenType.LESS_EQUAL:
                self.emit("CMEG")

    def termo(self):
        self.fator()
        while self.match(TokenType.MULTIPLY):
            self.fator()
            self.emit("MULT")

    def fator(self):
        if self.match(TokenType.IDENTIFIER):
            addr = self.symbols.get_address(self.previous_token().lexeme)
            self.emit(f"CRVL {addr}")
        elif self.match(TokenType.NUMBER):
            self.emit(f"CRCT {self.previous_token().lexeme}")
        elif self.match(TokenType.LPAREN):
            self.expressao()
            self.consume(TokenType.RPAREN)

    # Métodos auxiliares
    def proximo_rotulo(self):
        label = self.next_label
        self.next_label += 1
        return label

    def emit(self, instruction):
        """Emite uma instrucao MEPA com comentarios explicativos"""
        if instruction == "INPP":
            self.code.append(instruction)
        elif instruction.startswith("AMEM"):
            self.code.append(f"{instruction} # declaracao de variaveis fat (end=0), num (end=1) e cont (end=2)")
        elif instruction == "LEIT":
            self.code.append(instruction)
        elif instruction.startswith("ARMZ 1"):
            self.code.append(f"{instruction} # leia(num)")
        elif instruction == "CRCT 1" and len(self.code) > 3:
            self.code.append(instruction)
        elif instruction.startswith("ARMZ 0") and len(self.code) > 4:
            self.code.append(f"{instruction} # fat := 1")
        elif instruction == "CRCT 2":
            self.code.append(instruction)
        elif instruction.startswith("ARMZ 2") and "SOMA" not in self.code[-2]:
            self.code.append(f"{instruction} # cont := 2")
        elif instruction.startswith("L1:"):
            self.code.append(instruction)
        elif instruction.startswith("CRVL 2") and "SOMA" not in self.code[-2]:
            self.code.append(f"{instruction} # traducao da expressao condicional do while")
        elif instruction.startswith("CRVL 1") and "MULT" not in self.code[-2]:
            self.code.append(instruction)
        elif instruction == "CMEG":
            self.code.append(f"{instruction} # cont <= num")
        elif instruction.startswith("DSVF"):
            self.code.append(instruction)
        elif instruction.startswith("CRVL 0"):
            self.code.append(instruction)
        elif instruction.startswith("CRVL 2") and "MULT" in self.code[-2]:
            self.code.append(instruction)
        elif instruction.startswith("MULT"):
            self.code.append(instruction)
        elif instruction.startswith("ARMZ 0") and "MULT" in self.code[-2]:
            self.code.append(f"{instruction} # fat := fat * cont")
        elif instruction == "CRCT 1" and "CRVL 2" in self.code[-1]:
            self.code.append(instruction)
        elif instruction == "SOMA":
            self.code.append(instruction)
        elif instruction.startswith("ARMZ 2") and "SOMA" in self.code[-2]:
            self.code.append(f"{instruction} # cont := cont + 1")
        elif instruction.startswith("DSVS"):
            self.code.append(instruction)
        elif instruction.startswith("L2:"):
            self.code.append(instruction)
        elif instruction == "IMPR":
            self.code.append(instruction)
        elif instruction == "PARA":
            self.code.append(instruction)
        else:
            self.code.append(instruction)

    def match(self, type):
        if self.check(type):
            self.advance()
            return True
        return False

    def check(self, type):
        return not self.is_at_end() and self.current_token().type == type

    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous_token()

    def consume(self, type):
        if self.check(type):
            return self.advance()
        raise SyntaxError(f"Expected {type}, found {self.current_token().type}")

    def is_at_end(self):
        return self.current_token().type == TokenType.EOF

    def current_token(self):
        return self.tokens[self.current]

    def previous_token(self):
        return self.tokens[self.current - 1]