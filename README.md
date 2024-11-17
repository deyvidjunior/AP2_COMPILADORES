# Compilador PascalLite para MEPA

## Informações do Projeto
**Disciplina:** Compiladores
**Professor:** Leonardo Massayuki Takuno
**Semestre:** 6º Semestre - 3º Ano
**Período:** 2º Semestre/2023
**Instituição:** Faculdade Impacta de Tecnologia
**Curso:** Engenharia da Computação

## Integrantes do Grupo
- DEYVID JUNIOR LIMACHI ALEJO - [RA:2201606]
- YAGO THANUS SANTOS LIMA - [RA:2200839] 
- JULIA BARBOSA - [RA:2200820]
- FERNAND GORGONIO DA SILVA - [RA:1903937]



## Descrição do Projeto
Este projeto implementa um compilador que traduz programas escritos em PascalLite (um subconjunto de Pascal) para código MEPA (Máquina de Execução de Pascal). O sistema realiza análise léxica, sintática e semântica, gerando código MEPA executável.

## Funcionalidades
- **Análise Léxica** com suporte para:
  - Palavras-chave (program, begin, end, etc.)
  - Operadores (+, -, *, div, etc.) 
  - Números e identificadores
  - Comentários
- **Análise Sintática** seguindo a gramática PascalLite
- **Análise Semântica**:
  - Verificação de declaração de variáveis
  - Verificação de tipos
  - Análise de escopo
- **Geração de código MEPA**

## Estrutura do Projeto
.
├── main.py # Ponto de entrada do compilador
├── lexer.py # Analisador léxico
├── parser.py # Analisador sintático e gerador de código
├── token_types.py # Definição de tipos de tokens
├── symbol_table.py # Implementação da tabela de símbolos
├── semantic_analyzer.py # Análise semântica
├── code_generator.py # Geração de código MEPA
└── test_compiler.py # Suite de testes

## Como Executar

bash
Executar o compilador
python main.py
Executar os testes
python -m unittest test_compiler.py

## Exemplo de Uso
pascal
program exemplo1;
var fat, num, cont: integer;
begin
read(num);
fat := 1;
cont := 2;
while cont <= num do
begin
fat := fat num;
cont := cont + 1
end;
write(fat)
end.

## Instruções MEPA Suportadas
- INPP: Início do programa
- AMEM: Reserva memória
- LEIT: Lê entrada
- ARMZ: Armazena em variável
- CRVL: Carrega valor de variável
- CRCT: Carrega constante
- SOMA: Soma
- MULT: Multiplica
- CMEG: Compara menor ou igual
- DSVF: Desvio se falso
- DSVS: Desvio incondicional
- IMPR: Imprime
- PARA: Fim do programa

## Limitações
- Suporte apenas para números inteiros
- Sem suporte para funções ou procedimentos
- Conjunto limitado de operadores
- Sem suporte para strings ou arrays

## Critérios de Avaliação
1. Funcionamento correto do programa
2. Implementação em Python
3. Fidelidade à especificação do projeto
4. Clareza e organização do código:
   - Comentários apropriados
   - Nomes significativos de variáveis
   - Estruturação adequada do código

## Agradecimentos
Agradecemos ao Professor Leonardo Massayuki Takuno pela orientação e suporte durante o desenvolvimento deste projeto.