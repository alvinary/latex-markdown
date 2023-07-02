import re
from collections import defaultdict

MUTE = 'mute'
DEFAULT_PRECEDENCE = 10 # Default precedence
TAGGED = 'tagged'
INVENTORY = lambda: defaultdict(lambda: set())
IDENTITY = lambda x : x

# Markdown constants

BEGIN = '\\begin'
END = '\\end'
LEFT_CURLY = '{'
RIGHT_CURLY = '}'
LEFT_SQUARE = '['
RIGHT_SQUARE = ']'
BACKSLASH = '\\'

NEWLINE = '\n'
BREAK = '\n\n'
TAB = '\t'
SPACE = ' '

UNDERSCORE = '_'
THIN_BAR = '_' * 66
STAR = '*'
TITLE = '#'
SECTION = '##'
SUBSECTION = '###'
SHORT_THICK_BAR = '=='
THICK_BAR = '=' * 44
DOUBLE_SPACE = '  '
EXPLICIT_TAB = '@TAB@'
EXPLICIT_NEWLINE = '@NEWLINE@'
DOUBLE_STAR = '**'
WIGGLE = '~'

SPECIAL_TOKENS = [STAR, TITLE, SECTION, SUBSECTION, THICK_BAR, SHORT_THICK_BAR, UNDERSCORE, THIN_BAR, EXPLICIT_NEWLINE, EXPLICIT_TAB, DOUBLE_STAR, WIGGLE]

underscores = re.compile('_____[_]+')
thickBar = re.compile('=====[=]+')

TEXT_TOKEN = 'texttoken'
SPECIAL_TOKEN = 'specialtoken'


'''

El input es

input = '2 + 5'
tokens = tokenize(input)) -> ['2', '+', '5']
tags = tag(tokens) -> [int, symbol, int]
tagged_tokens = zip(tokens, tags) # [('2', 'int'), ('+', 'symbol'), ('5', 'int')]

parser = Parser.from_grammar(dsl)

dsl = '
title -> [titleMark] text
paragraph -> text [long_break]
long_break -> [newline] [newline]
long_break -> [newline] [longbreak]
'

'# Mi super titulo

Hola gente, esto es un parrafo

Como hay dos enter serguidos, esto es otro parrafo

Y esto tambien
'

Parser

    {
    'text' : [titleRule, paragraphRule],
    'titleMark' : [titleRule]
    }

{"symbol": "#", "string": "Mi super titulo"}

Parser(grammar)
    .rules
    .simbolo de pecedencia
    .simbolo de evaluacion

    .get_parse(input_tokens):
        new_parse = Parse(input_tokens)
        new_parse.execute()
        return new_parse


Parse(input_tokens)
    .parser = Parser()
    .spans :: (int, int) -> Node

    .execute()
    .value()

Parse.
    spans[0, 0] == Node(#)
    spans[1, 1] == Node('mi super titulo')
    spans[0, 1] == Node([#, mi super titulo])

    spans[i, j] tiene el parseado de tokens[i:j]
    .execute()


Parser.from_grammar(dsl)
    lines = get_lines(dsl) # para sacar las lineas en blanco


'''