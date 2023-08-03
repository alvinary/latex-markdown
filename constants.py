import re
from collections import defaultdict

MUTE = 'mute'
DEFAULT_PRECEDENCE = 10 # Default precedence
TAGGED = 'tagged'
INVENTORY = lambda: defaultdict(lambda: set())
IDENTITY = lambda x : x

WRAP = lambda x, y : [x, y]
WRAPPEND = lambda x, y : [x] + y

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
EXPLICIT_TAB = ' @TAB@ '
EXPLICIT_NEWLINE = '@NEWLINE@'
EXPLICIT_BREAK = ' @BREAK@'
DOUBLE_STAR = '**'
WIGGLE = '~'
BEGIN_DOCUMENT = '@_BEGIN_@'
END_DOCUMENT = '@_END_@'

underscores = re.compile('_____[_]+')
thickBar = re.compile('=====[=]+')

PUNCTUATION = [
        ".",
        ")",
        "(",
        "]",
        "[",
        "{",
        "}",
        "-",
        "_",
        ",",
        ":",
        ";"
        ]
