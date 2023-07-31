from constants import *
from md_macros import *

latex_dsl = [
    ('title mark', 'title_mark', ("#",), DEFAULT_PRECEDENCE, IDENTITY),
    ('section mark', 'section_mark', ("##",), DEFAULT_PRECEDENCE, IDENTITY),
    ('subsection mark', 'subsection_mark', ("###",), DEFAULT_PRECEDENCE, IDENTITY),
    
    ('newlines from text', 'newline', (EXPLICIT_NEWLINE,), DEFAULT_PRECEDENCE, IDENTITY),
    ('thin bar', 'thin_bar', (THIN_BAR,), DEFAULT_PRECEDENCE, IDENTITY),
    ('double star', 'double_star', ('**',), DEFAULT_PRECEDENCE, IDENTITY),
    ('wiggle', 'wiggle', ('~',), DEFAULT_PRECEDENCE, IDENTITY),
    
    ('paragraph', 'paragraph', ('text', 'break'), DEFAULT_PRECEDENCE, lambda x, y: x + y),
    
    ('title', 'thin_bar', ('title_mark', 'text'), DEFAULT_PRECEDENCE, lambda _, x: title(x)),
    ('section', 'thin_bar', ('section_mark', 'text'), DEFAULT_PRECEDENCE, lambda _, x : section(x)),
    ('subsection', 'thin_bar', ('subsection_mark', 'text'), DEFAULT_PRECEDENCE, lambda _, x: subsection(x)),
    
    ('title', 'thin_bar', ('title_mark', 'text'), DEFAULT_PRECEDENCE, lambda _, x: title(x)),
    ('section', 'thin_bar', ('section_mark', 'text'), DEFAULT_PRECEDENCE, lambda _, x : section(x)),
    ('subsection', 'thin_bar', ('subsection_mark', 'text'), DEFAULT_PRECEDENCE, lambda _, x: subsection(x)),
    
    ('title', 'thin_bar', ('title_mark', 'text'), DEFAULT_PRECEDENCE, lambda _, x: title(x)),
    ('section', 'thin_bar', ('section_mark', 'text'), DEFAULT_PRECEDENCE, lambda _, x : section(x)),
    ('subsection', 'thin_bar', ('subsection_mark', 'text'), DEFAULT_PRECEDENCE, lambda _, x: subsection(x)),
    
    ('multiline text', 'text', ('text', 'newline', 'text'), DEFAULT_PRECEDENCE, lambda x, y, z: x + y + z),
    ('cite in text', 'text', ('text', 'citation', 'text'), DEFAULT_PRECEDENCE, lambda x, y, z: x + y + z),
    ('multiline text', 'text', ('text', 'newline', 'text'), DEFAULT_PRECEDENCE, lambda x, y, z: x + y + z),
    
    ('left citation mark', 'left_cite', ('[.',), DEFAULT_PRECEDENCE, IDENTITY),
    ('right citation mark', 'right_cite', ('.]',), DEFAULT_PRECEDENCE, IDENTITY),
    ('citation', 'citation', ('left_cite', 'text', 'right_cite'), DEFAULT_PRECEDENCE, lambda _, x, __:  citation(x)),
    
    ('basic break', 'break', ('newline', 'newline'), DEFAULT_PRECEDENCE, lambda _, __ : BREAK),
    ('long break', 'break', ('break', 'newline'), DEFAULT_PRECEDENCE, lambda _, __: BREAK)
]

delimiters = ['(', ')', '{', '}', '[', ']', '<', '>', '|']

math_tokens = [
    '(',
    ')',
    '{',
    '}',
    '<',
    '>',
    '=',
    '!=',
    '>=',
    '<=',
    '=>',
    'and',
    'or',
    'not',
    'iff',
    '<=>',
    '<==>',
    'in',
    'to',
    'maps',
    '|',
    'empty',
    'for',
    'all',
    'exists',
    'from',
    'over',
    'of',
    'sum',
    'product',
    'integral',
    'sup',
    'sub',
    '_]',
    '[_',
    '^]',
    '[^',
]

with_delimiters = {
    '=>' : '=@-',
    '<=>' : '-@=@-',
    '==>' : '==@-',
    '<==>' : '-@==@-',
    '>=' : '-%=',
    '<=' : '%-='
}

without_delimiters = {
    '=@-' : '=>',
    '-@=@-' : '<=>',
    '==@-' : '==>',
    '-@==@-' : '<==>',
    '-%=' : '>=',
    '%-=' : '<='
}

math_dsl = [
    # Core definitions
    # Delimiters
    ('left parenthesis', 'delim', ('(',), DEFAULT_PRECEDENCE, lambda x: x),
    ('right parenthesis', 'delim', (')',), DEFAULT_PRECEDENCE, lambda x: x),
    ('left brace', 'delim', ('{',), DEFAULT_PRECEDENCE, lambda _: '\\lbrace'),
    ('right brace', 'delim', ('}',), DEFAULT_PRECEDENCE, lambda _: '\\rbrace'),
    ('left angle bracket', 'delim', ('<',), DEFAULT_PRECEDENCE, lambda _: '\\langle'),
    ('right angle bracket', 'delim', ('>',), DEFAULT_PRECEDENCE, lambda _: '\\rangle'),
    # Common relations
    ('equal', 'inf', ('=',), DEFAULT_PRECEDENCE, lambda x: x),
    ('not equal', 'inf', ('!=',), DEFAULT_PRECEDENCE, lambda _: '\\\\neq'),
    ('greater or equal', 'inf', ('>=',), DEFAULT_PRECEDENCE, lambda _: '\\ge'),
    ('less or equal', 'inf', ('<=',), DEFAULT_PRECEDENCE, lambda _: '\\le'),
    # Basic notation for sets, functions, propositional and predicate logic
    ('and', 'inf', ('and',), DEFAULT_PRECEDENCE, lambda _: '\\land'),
    ('or', 'inf', ('or',), DEFAULT_PRECEDENCE, lambda _: '\\lor'),
    ('not', 'pref', ('not',), DEFAULT_PRECEDENCE, lambda _: '\\\\neg'),
    ('iff', 'inf', ('iff',), DEFAULT_PRECEDENCE, lambda _: '\\Leftrightarrow'),
    ('<=>', 'inf', ('<=>',), DEFAULT_PRECEDENCE, lambda _: '\\Leftrightarrow'),
    ('=>', 'inf', ('=>',), DEFAULT_PRECEDENCE, lambda _: '\\Rightarrow'),
    ('==>', 'inf', ('==>',), DEFAULT_PRECEDENCE, lambda _: '\\Longrightarrow'),
    ('<==>', 'inf', ('<==>',), DEFAULT_PRECEDENCE, lambda _: '\\Longleftrightarrow'),
    ('in', 'inf', ('in',), DEFAULT_PRECEDENCE, lambda x: '\\in'),
    ('not in', 'math', ('not', 'in',), DEFAULT_PRECEDENCE + 5, lambda _, __: '\\\\notin'),
    ('maps to', 'inf', ('maps', 'to',), DEFAULT_PRECEDENCE + 5, lambda _, __: '\\mapsto'),
    # maps to via
    # inclusion (left and right)
    ('empty', 'elem', ('empty',), DEFAULT_PRECEDENCE, lambda x : '\\emptyset'),
    ('empty', 'elem', ('ø',), DEFAULT_PRECEDENCE, lambda x : '\\emptyset'),
    ('for all', 'math', ('for', 'all',), DEFAULT_PRECEDENCE + 5, lambda _, __ : '\\forall'),
    ('exists', 'pref', ('exists',), DEFAULT_PRECEDENCE, lambda x : '\\exists'),
    ('vert', 'delim', ('|',), DEFAULT_PRECEDENCE, lambda x : '\\vert'),
    ('lvert', 'delim', ('|',), DEFAULT_PRECEDENCE, lambda x : '\\lvert'),
    ('rvert', 'delim', ('|',), DEFAULT_PRECEDENCE, lambda x : '\\rvert'),
    # Subindices, superindices and diacritics
    ('sub', 'math', ('math', '[_', 'math', '_]'), DEFAULT_PRECEDENCE, lambda x, _, y, __ : x + '_{' y '}'),
    ('super', 'math', ('math', '[^', 'math', '^]'), DEFAULT_PRECEDENCE, lambda x, _, y, __ : '^{' y '}'),
    ('short sub', 'math', ('math', 'sub', 'math'), DEFAULT_PRECEDENCE + 4, lambda x, _, y : x + '_{' y '}'),
    ('short super', 'math', ('math', 'sup', 'math'), DEFAULT_PRECEDENCE + 4, lambda x, _, y : '^{' y '}'),
    # ', ^, bar, hat, tilde
    # Common operations
    ('sum', 'op', ('sum',), DEFAULT_PRECEDENCE, lambda x : '\\sum'),
    ('product', 'op', ('product',), DEFAULT_PRECEDENCE, lambda x : '\\prod'),
    ('integral', 'op', ('integral',), DEFAULT_PRECEDENCE, lambda x : '\\int'),
    ('op from to', 'math', ('op', 'from', 'math', 'to', 'math', 'of', 'math',), DEFAULT_PRECEDENCE + 10, lambda o, _, s, __, b, ___, f : big_operator(o) + '_{' + s + '}^{' + b + '}' + f' {f}'),
    ('inf from to', 'math', ('inf', 'from', 'math', 'to', 'math', 'of', 'math',), DEFAULT_PRECEDENCE + 10, lambda o, _, s, __, b, ___, f : big_operator(o) + '_{' + s + '}^{' + b + '}' + f' {f}'),
    ('op over', 'math', ('inf', 'from', 'math', 'to', 'math', 'of', 'math',), DEFAULT_PRECEDENCE + 10, lambda o, _, s, __, b, ___, f : big_operator(o) + '_{' + s + '} ' + f),
    # R, Q, C, Z, aleph, epsilon, 
    # Greek
    ('math', 'math', ('math', 'math'), DEFAULT_PRECEDENCE - 5, lambda x, y : x + ' ' + y),
    ('element', 'math', ('elem',), DEFAULT_PRECEDENCE - 5, lambda x : x),
    ('infix', 'math', ('inf',), DEFAULT_PRECEDENCE - 5, lambda x : x),
    ('prefix', 'math', ('pref',), DEFAULT_PRECEDENCE - 5, lambda x : x),
    ('posfix', 'math', ('pos',), DEFAULT_PRECEDENCE - 5, lambda x : x),
    ('delimiter', 'math', ('delim',), DEFAULT_PRECEDENCE - 5, lambda x : x),
    ('name', 'math', ('name',), DEFAULT_PRECEDENCE - 5, lambda x : x)
]

f'''
italics -> [wiggle] text [wiggle]            := x : italics(x)
bold -> [doubleStar] text [doubleStar]       := x : bold(x)
'''

mathDSL = '''
delimiter -> _rparen                         := x : x
delimiter -> _lparen                         := x : x
delimiter -> _rangle                         := x : x
delimiter -> _langle                         := x : x
delimiter -> _lbrace                         := x : x
delimiter -> _rbrace                         := x : x

LETTER -> { a, b, c, d, e, f, g, h, i }      := x : x
LETTER -> { j, k, l, m, n, o, p, q, r }      := x : x
LETTER -> { s, t, u, v, w, x, y, z }         := x : x

letter -> LETTER                             := x : x

_hat -> hat                 := x : x
_bar -> bar                 := x : x
_tilde -> tilde             := x : x
_check -> check             := x : x
_ring -> ring               := x : x
_vector -> vector           := x : x

mhat -> letter [_hat]                   := x : '\\hat{' + x + '}'
mbar -> letter [_bar]                   := x : '\\bar{' + x + '}'
mtilde -> letter [_tilde]               := x : '\\tilde{' + x + '}'
mcheck -> letter [_check]               := x : '\\check{' + x + '}'
mring -> letter [_ring]                 := x : '\\mathring{' + x + '}'
mvector -> letter [_vector]             := x : '\\vec{' + x + '}'

lettermod -> mhat                       := x : x
lettermod -> mbar                       := x : x
lettermod -> mtilde                     := x : x
lettermod -> mcheck                     := x : x
lettermod -> mring                      := x : x
lettermod -> mvector                    := x : x

mathName -> lettermod                   := x : x
mathName -> letter                      := x : x
'''

'''
bigoperator -> sum                           := x : '\\sum'
bigoperator -> product                       := x : '\\prod'
bigoperator -> integral                      := x : '\\int'

_over -> over                                := x : x
_of -> of                                    := x : x
_from -> from                                := x : x
_to -> to                                    := x : x

bigop -> bigoperator [_over] math [_of] math            := x, y, z : x + '_{' + y + '} ' + z
bigop -> bigoperator [_from] math [_to] math [_of] math := x, y, z, w : x + '_{' + y + '}^{' + z + '} ' + w

_cross -> x                                  := x : '\\times'

cardinal -> _lvert math _rvert               := x, y, z : x + y + z

mathElem -> binaryRelation                   := x : x
mathElem -> mathName                         := x : x
mathElem -> bigop                            := x : x
mathElem -> delimiter                        := x : x
mathElem -> logic                            := x : x

mathElem -> ,                                := x : x

mathRest -> mathElem                         := x : x

math -> mathElem math                        := x, y : x + ' ' + y
math -> mathRest                             := x : x
'''
