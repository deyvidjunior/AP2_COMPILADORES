from lexer import Lexer
from parser import Parser

def main():
    source = """
    program exemplo1;
    var fat, num, cont: integer;
    begin
        read(num);
        fat := 1;
        cont := 2;
        while cont <= num do
            begin
                fat := fat * num;
                cont := cont + 1
            end;
        write(fat)
    end.
    """
    
    try:
        # Análise léxica
        print("Iniciando análise léxica...")
        lexer = Lexer(source)
        tokens = lexer.scan_tokens()
        
        # Debug: mostra os tokens gerados
        print("\nTokens gerados:")
        for token in tokens:
            print(token)
        
        # Análise sintática, semântica e geração de código
        print("\nIniciando análise sintática...")
        parser = Parser(tokens)
        code = parser.programa()  # Mudou de parse() para programa()
        
        # Imprime código MEPA gerado
        print("\nCódigo MEPA gerado:")
        for instruction in code:
            print(instruction)
            
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

if __name__ == "__main__":
    main()