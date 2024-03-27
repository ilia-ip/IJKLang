import parser
import lexer
import sys
import codegen
from pycolors import colors as c
def handler(type, value, traceback):
    print(c.RED, c.BOLD)
    if str(value) == '<main> function not found!':
        print('Syntax error: function "main" not found')
    elif type is KeyError:
        print('Syntax error: Undeclared value', value)
    elif type is FileNotFoundError:
        print('File error: Input file not found, please check the file name')
    elif type is ValueError:
        print(value)
    else:
        print(type, value)
    print(c.RESET)

fname = ''
outname = 'IJKOUT'
generate = 'exe'
VERSION = '0.0.3'
ndebug = False

print(c.BOLD, c.DARK_GREEN, ' 𑨋 - IJKLang Compiler v0.0.2 by ILIⴷ IP - 𑨋 ', c.RESET)
for arg in sys.argv[1::]:
    match arg:
        case '-H':
            fname = 'NA'
            print(f'''Aviable flags for IJKCompiler v{VERSION}:\n -f : IJK file name\n -o : output file name\n -A : generate assembler file\n -O : generate object file\n -L : generate all of them\n -D all debug prints (do not use if not know what is it)''')
        case '-f':
            if sys.argv[sys.argv.index(arg)+1].startswith('-'):
                print('Input file name flag requires a file name at next parameter!')
                exit()
            fname = sys.argv[sys.argv.index(arg)+1]
        case '-o':
            if sys.argv[sys.argv.index(arg)+1].startswith('-'):
                print('Output file name flag requires a file name at next parameter!')
                exit()
            outname = sys.argv[sys.argv.index(arg) + 1]
        case '-A':
            generate = 'asm'
        case '-O':
            generate = 'obj'
        case '-L':
            generate = 'all'
        case '-D':
            generate = 'all'
            ndebug = True
sys.excepthook = handler

tokens = {'declare': '$declare', 'variable': 'def', 'system': '$', 'function': 'section', 'return': 'return', 'writeln': 'write', 'not': '!', 'sum': '+',
          'sub': '-', 'mul': '*', 'div': '/', 'assign': '=', 'lt': '<',
          'gt': '>', 'eq': '==', 'op3': '{', 'cp3': '}', 'op2': '[', 'cp2': ']', 'op1': '(', 'cp1': ')', 'comma': ',',
          'colon': ':', 'cc': "'", 'sc': '"', 'dot': '.', 'semicolon': ';', 'init': 'CONSOLE_INIT'}

#tokens2 = {'using': '$using', 'declare': '$declare', 'function': 'func', 'return': 'return', 'writeln': 'writeln', 'variable': 'let',
#                          'true': 'true', 'false': 'false', 'null': 'NA', 'and': '&&', 'or': '||', 'not': '!', 'sum': '+',
#                          'sub': '-', 'mul': '*', 'div': '/', 'assign': '=', 'lt': '<', 'gt': '>',
#                          'lte': '<=', 'gte': '>=', 'eq': '==', 'neq': '!=', 'op3': '{', 'cp3': '}', 'op2': '[', 'cp2': ']',
#                          'op1': '(', 'cp1': ')', 'comma': ',', 'colon': ':', 'cc': "'", 'sc': '"', 'dot': '.', 'integer': 'int',
#                          'float': 'float', 'bool': 'bool', 'char': 'char', 'string': 'str', 'semicolon': ';', 'if': 'if',
#                          'else': 'else', 'else if': 'elif', 'while': 'while'}
if '.' in outname:
    outname, NA = outname.split('.')
text = ''''''
if fname != 'NA':
    with open(fname, 'r') as f:
        for line in f:
            text += line

    lexer = lexer.IJKLexer(ndebug)
    for token in tokens:
        lexer.addToken(token, tokens[token])
    tokenized_text = lexer.lex(text)

    parser = parser.IJKParser(ndebug)
    ast = parser.parse(tokenized_text)

    gen = codegen.IJKCodeGenerator(outname, generate, VERSION, ndebug)
    gen.generate(ast)