from constants import *
from macros import *

latex_tokens = set([
    "#",
    "##",
    "###",
    THIN_BAR,
    "*",
    "**",
    "[.",
    ".]",
    EXPLICIT_NEWLINE,
    EXPLICIT_BREAK,
    BEGIN_DOCUMENT,
    END_DOCUMENT,
    BEGIN_MATH,
    END_MATH
])

latex_dsl = [
    # A latex document is some trailing whitespace followed by the
    # document contents and some more trailing whitespace
    ('document', 'document', ('begin', 'content', 'end'), DEFAULT_PRECEDENCE, lambda _, x, __ : article(x)),
    ('newline whitespace', 'whitespace', ('newline',), DEFAULT_PRECEDENCE, lambda x : x),
    ('break whitespace', 'whitespace', ('break',), DEFAULT_PRECEDENCE, lambda x : x),
    ('begin', 'begin', (BEGIN_DOCUMENT,), DEFAULT_PRECEDENCE, lambda x, : x),
    ('end', 'end', (END_DOCUMENT,), DEFAULT_PRECEDENCE, lambda x : x),
    # Types of content
    ('blocks content', 'content', ('blocks',), DEFAULT_PRECEDENCE, lambda x : x),
    ('block', 'blocks', ('block',), DEFAULT_PRECEDENCE, lambda x : x), # todo: make this unique
    ('blocks plus block', 'blocks', ('blocks', 'block'), DEFAULT_PRECEDENCE, lambda x, y : x + BREAK + y),
    # Blocks for images, tables, equations, and so on
    # Whitespace
    ('break token', 'break', (EXPLICIT_BREAK,), DEFAULT_PRECEDENCE, IDENTITY),
    ('newline token', 'newline', (EXPLICIT_NEWLINE,), DEFAULT_PRECEDENCE, IDENTITY),
    # Paragraphs, breaks and basic text
    ('paragraph', 'block', ('text', 'break'), DEFAULT_PRECEDENCE, lambda x, _ : x + BREAK),
    ('text lines', 'text', ('text', 'newline', 'text'), DEFAULT_PRECEDENCE, lambda x, _, y : x + NEWLINE + y), # todo: make this right associative
    ('inline text', 'text', ('text', 'inline_text'), DEFAULT_PRECEDENCE, lambda x, y : x + SPACE + y),
    # Special symbols for titles, sections, and subsections
    ('section mark', 'section_mark', ("#",), DEFAULT_PRECEDENCE, IDENTITY),
    ('subsection mark', 'subsection_mark', ("##",), DEFAULT_PRECEDENCE, IDENTITY),
    ('subsubsection', 'subsubsection_mark', ("###",), DEFAULT_PRECEDENCE, IDENTITY),
    # Document hierarchy
    ('section', 'block', ('section_mark', 'text', 'break'), DEFAULT_PRECEDENCE, lambda _, x, __  : section(x) + BREAK),
    ('subsection', 'block', ('subsection_mark', 'text', 'break'), DEFAULT_PRECEDENCE, lambda _, x, __  : subsection(x) + BREAK),
    # Citations
    ('thin bar', 'thin_bar', (THIN_BAR,), DEFAULT_PRECEDENCE, IDENTITY),
    # Formatted text
    ('double star', 'double_star', ('**',), DEFAULT_PRECEDENCE, IDENTITY),
    ('wiggle', 'wiggle', ('~',), DEFAULT_PRECEDENCE, IDENTITY),
    ('inline citation', 'inline_text', ('citation',), DEFAULT_PRECEDENCE, lambda x : x), # todo: call relevant function
    # Images, citations, tables, indices, and references
    ('left citation mark', 'left_cite', ('[.',), DEFAULT_PRECEDENCE, IDENTITY),
    ('right citation mark', 'right_cite', ('.]',), DEFAULT_PRECEDENCE, IDENTITY),
    ('citation', 'citation', ('left_cite', 'text', 'right_cite'), DEFAULT_PRECEDENCE, lambda _, x, __:  citation(x)),
    ('basic break', 'break', ('newline', 'newline'), DEFAULT_PRECEDENCE, lambda _, __ : BREAK),
    ('long break', 'break', ('break', 'newline'), DEFAULT_PRECEDENCE, lambda _, __: BREAK),
    # Math
    ('begin math', 'begin_math', (BEGIN_MATH,), DEFAULT_PRECEDENCE, lambda x : x),
    ('begin math', 'end_math', (END_MATH,), DEFAULT_PRECEDENCE, lambda x : x),
    ('math block', 'block', ('latex_math', 'break'), DEFAULT_PRECEDENCE, lambda x, _ : x),
    ('latex math', 'latex_math', ('begin_math', 'math', 'end_math'), DEFAULT_PRECEDENCE, lambda _, x, __ : x),
    ('inline math', 'inline_text', ('latex_math',), DEFAULT_PRECEDENCE, lambda x : x),
    ('dummy math test', 'inline_text', ('$$$$',), DEFAULT_PRECEDENCE, lambda x : x)
]

delimiters = ['(', ')', '{', '}', '[', ']', '<', '>', '|']

math_tokens = set([
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
    'notin',
    'C', 'R', 'Q', 'Z', 'N',
    '+'
])

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
    # DSL-specific
    ('Magic wand', 'math', ('[:', 'math', ':]'), DEFAULT_PRECEDENCE + 15, lambda _, x, __ : x),
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
    ('not', 'inf', ('not',), DEFAULT_PRECEDENCE, lambda _: '\\\\neg'),
    ('iff', 'inf', ('iff',), DEFAULT_PRECEDENCE, lambda _: '\\Leftrightarrow'),
    ('<=>', 'inf', ('<=>',), DEFAULT_PRECEDENCE, lambda _: '\\Leftrightarrow'),
    ('=>', 'inf', ('=>',), DEFAULT_PRECEDENCE, lambda _: '\\Rightarrow'),
    ('==>', 'inf', ('==>',), DEFAULT_PRECEDENCE, lambda _: '\\Longrightarrow'),
    ('<==>', 'inf', ('<==>',), DEFAULT_PRECEDENCE, lambda _: '\\Longleftrightarrow'),
    ('in', 'inf', ('in',), DEFAULT_PRECEDENCE, lambda x: '\\in'),
    ('notin', 'inf', ('notin',), DEFAULT_PRECEDENCE, lambda _, __: '\\\\notin'),
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
    ('sub', 'math', ('math', '[_', 'math', '_]'), DEFAULT_PRECEDENCE, lambda x, _, y, __ : x + '_{' + y + '}'),
    ('super', 'math', ('math', '[^', 'math', '^]'), DEFAULT_PRECEDENCE, lambda x, _, y, __ : x + '^{' + y + '}'),
    ('short sub', 'math', ('math', 'sub', 'name'), DEFAULT_PRECEDENCE + 4, lambda x, _, y : x + '_{' + y + '}'),
    ('short super', 'math', ('math', 'sup', 'name'), DEFAULT_PRECEDENCE + 4, lambda x, _, y : x + '^{' + y + '}'),
    # ', ^, bar, hat, tilde
    # Common operations
    ('sum', 'op', ('sum',), DEFAULT_PRECEDENCE, lambda x : '\\sum'),
    ('product', 'op', ('product',), DEFAULT_PRECEDENCE, lambda x : '\\prod'),
    ('integral', 'op', ('integral',), DEFAULT_PRECEDENCE, lambda x : '\\int'),
    ('op from to', 'math', ('op', 'from', 'math', 'to', 'math', 'of', 'math',), DEFAULT_PRECEDENCE + 10, lambda o, _, s, __, b, ___, f : big_operator(o) + '_{' + s + '}^{' + b + '}' + f' {f}'),
    ('inf from to', 'math', ('op', 'from', 'math', 'to', 'math', 'of', 'math',), DEFAULT_PRECEDENCE + 10, lambda o, _, s, __, b, ___, f : big_operator(o) + '_{' + s + '}^{' + b + '}' + f' {f}'),
    ('op over', 'math', ('op', 'over', 'math', 'of', 'math',), DEFAULT_PRECEDENCE + 10, lambda o, _, s, __, f : big_operator(o) + '_{' + s + '} ' + f),
    # R, Q, C, Z, aleph, epsilon,
    ('reals', 'name', ('R',), DEFAULT_PRECEDENCE, lambda x : '\\R'),
    ('complex', 'name', ('C',), DEFAULT_PRECEDENCE, lambda x : '\\Complex'),
    ('rationals', 'name', ('Q',), DEFAULT_PRECEDENCE, lambda x : '\\Q'),
    ('integers', 'name', ('Z',), DEFAULT_PRECEDENCE, lambda x : '\\Z'),
    ('naturals', 'name', ('N',), DEFAULT_PRECEDENCE, lambda x : '\\N'),
    # Common operations
    ('plus', 'inf', ('+',), DEFAULT_PRECEDENCE, IDENTITY),
    # Greek
    ('math', 'math', ('math', 'math'), DEFAULT_PRECEDENCE - 5, lambda x, y : x + ' ' + y),
    ('element', 'math', ('elem',), DEFAULT_PRECEDENCE - 5, lambda x : x),
    ('infix', 'math', ('inf',), DEFAULT_PRECEDENCE - 5, lambda x : x),
    ('prefix', 'math', ('pref',), DEFAULT_PRECEDENCE - 5, lambda x : x),
    ('posfix', 'math', ('pos',), DEFAULT_PRECEDENCE - 5, lambda x : x),
    ('delimiter', 'math', ('delim',), DEFAULT_PRECEDENCE - 5, lambda x : x),
    ('name', 'math', ('name',), DEFAULT_PRECEDENCE - 5, lambda x : x)
]
