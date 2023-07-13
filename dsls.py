from constants import *

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
    'and',
    'or',
    'not',
    'iff',
    '<=>',
    '<==>',
    'in',
    'to',
    'maps',
    ':',
    '|'
]

math_dsl = [
    # Core definitions
    # Delimiters
    ('left parenthesis', 'lparen', ('(',), DEFAULT_PRECEDENCE, lambda _: '\\left'),
    ('right parenthesis', 'rparen', (')',), DEFAULT_PRECEDENCE, lambda _: '\\right'),
    ('left brace', 'lbrace', ('{',), DEFAULT_PRECEDENCE, lambda _: '\\lbrace'),
    ('right brace', 'rbrace', ('}',), DEFAULT_PRECEDENCE, lambda _: '\\rbrace'),
    ('left angle bracket', 'langle', ('<',), DEFAULT_PRECEDENCE, lambda _: '\\langle'),
    ('right angle bracket', 'rangle', ('>',), DEFAULT_PRECEDENCE, lambda _: '\\rangle'),
    # Common relations
    ('equal', 'rel', ('=',), DEFAULT_PRECEDENCE, lambda x: x),
    ('not equal', 'rel', ('!=',), DEFAULT_PRECEDENCE, lambda _: '\\\\neq'),
    ('greater or equal', 'rel', ('>=',), DEFAULT_PRECEDENCE, lambda _: '\\ge'),
    ('less or equal', 'rel', ('<=',), DEFAULT_PRECEDENCE, lambda _: '\\le'),
    # Basic notation for sets, functions, propositional and predicate logic
    ('and', 'op', ('and',), DEFAULT_PRECEDENCE, lambda _: '\\land'),
    ('or', 'op', ('or',), DEFAULT_PRECEDENCE, lambda _: '\\lor'),
    ('not', 'unary', ('not',), DEFAULT_PRECEDENCE, lambda _: '\\\\neg'),
    ('iff', 'rel', ('iff',), DEFAULT_PRECEDENCE, lambda _: '\\Leftrightarrow'),
    ('<=>', 'rel', ('<=>',), DEFAULT_PRECEDENCE, lambda _: '\\Leftrightarrow'),
    ('<==>', 'rel', ('<==>',), DEFAULT_PRECEDENCE, lambda _: '\\Longleftrightarrow'),
    ('in', 'rel', ('in',), DEFAULT_PRECEDENCE, lambda x: '\\in'),
    ('not in', 'rel', ('not', 'in',), DEFAULT_PRECEDENCE + 5, lambda _, __: '\\\\notin'),
    ('maps to', 'rel', ('maps', 'to',), DEFAULT_PRECEDENCE + 5, lambda _, __: '\\\\mapsto'),
    # maps to via
    # inclusion (left and right)
    # _empty -> ø                                  := x : '\\emptyset'
    # _dots -> :                                   := x : x
    # _forall -> all                               := x : '\\\\forall' 
    # _exists -> some                              := x : '\\exists'
    # _lvert -> |                                  := x : '\\lvert'
    # _rvert -> |                                  := x : '\\rvert'
    # _vert -> |                                   := x : '\\vert'
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
