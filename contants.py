import re

PUNCTUATION = {';', '->', '!=', '=', '(', ')', ',', '<'}
TOKEN = 'token label'
MUTE = 'mute'
LBRACE = '{'
RBRACE = '}'
NEWLINE = '\n'
TAB = '\t'
SPACE = ' '
COMMENT = '--'
DEFAULT_PRECEDENCE = 10.0 # Default precedence
RULE_ARROW = "->"


# Constants

BEGIN = '\\begin'
END = '\\end'
LEFT_CURLY = '{'
RIGHT_CURLY = '}'
LEFT_SQUARE = '['
RIGHT_SQUARE = ']'
BACKSLASH = '\\'

NEWLINE = '\n'
BREAK = '\n\n'

UNDERSCORE = '_'
THIN_BAR = '_' * 66
STAR = '*'
TITLE = '#'
SECTION = '##'
SUBSECTION = '###'
SHORT_THICK_BAR = '=='
THICK_BAR = '=' * 44
DOUBLE = '  '
EXPLICIT_TAB = '@TAB@'
EXPLICIT_NEWLINE = '@NEWLINE@'
DOUBLE_STAR = '**'
WIGGLE = '~'

SPECIAL_TOKENS = [STAR, TITLE, SECTION, SUBSECTION, THICK_BAR, SHORT_THICK_BAR, UNDERSCORE, THIN_BAR, EXPLICIT_NEWLINE, EXPLICIT_TAB, DOUBLE_STAR, WIGGLE]

underscores = re.compile('_____[_]+')
thickBar = re.compile('=====[=]+')

TEXT_TOKEN = 'texttoken'
SPECIAL_TOKEN = 'specialtoken'
