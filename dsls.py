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
    "~[",
    "]~",
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
    ('single block', 'blocks', ('block',), DEFAULT_PRECEDENCE, lambda x : x),
    # ToDo: test if 'begin document' could be the first 'blocks' element,
    # so that not every block is 'blocks', and there are less valid parses
    ('blocks plus block', 'blocks', ('blocks', 'block'), DEFAULT_PRECEDENCE, lambda x, y : x + BREAK + y),
    # Blocks for images, tables, equations, and so on
    # Whitespace
    ('break token', 'break', (EXPLICIT_BREAK,), DEFAULT_PRECEDENCE, IDENTITY),
    ('newline token', 'newline', (EXPLICIT_NEWLINE,), DEFAULT_PRECEDENCE, IDENTITY),
    # Paragraphs, breaks and basic text
    ('paragraph', 'block', ('text', 'break'), DEFAULT_PRECEDENCE, lambda x, _ : x),
    ('text lines', 'text', ('text', 'newline', 'text'), DEFAULT_PRECEDENCE, lambda x, _, y : x + NEWLINE + y), # todo: make this right associative
    ('inline text', 'text', ('text', 'inline_text'), DEFAULT_PRECEDENCE, lambda x, y : x + SPACE + y),
    ('text and text', 'text', ('text', 'text'), DEFAULT_PRECEDENCE, lambda x, y : x + ' ' + SPACE + y),
    # Special symbols for titles, sections, and subsections
    ('section mark', 'section_mark', ("#",), DEFAULT_PRECEDENCE, IDENTITY),
    ('subsection mark', 'subsection_mark', ("##",), DEFAULT_PRECEDENCE, IDENTITY),
    ('subsubsection', 'subsubsection_mark', ("###",), DEFAULT_PRECEDENCE, IDENTITY),
    # Document hierarchy
    ('section', 'block', ('section_mark', 'text', 'break'), DEFAULT_PRECEDENCE, lambda _, x, __  : section(x) + BREAK),
    ('subsection', 'block', ('subsection_mark', 'text', 'break'), DEFAULT_PRECEDENCE, lambda _, x, __  : subsection(x)),
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
    ('begin math', 'begin_math', (BEGIN_MATH,), DEFAULT_PRECEDENCE, lambda x : '$'),
    ('end math', 'end_math', (END_MATH,), DEFAULT_PRECEDENCE, lambda x : '$'),
    ('begin math block', 'begin_math_block', ('~[',), DEFAULT_PRECEDENCE, lambda x : x),
    ('end math block', 'end_math_block', (']~',), DEFAULT_PRECEDENCE, lambda x : x),
    ('default math block', 'block', ('begin_math_block', 'math', 'end_math_block', 'break'), DEFAULT_PRECEDENCE + 10, lambda ___, x, _, __ : beginEnd('equation', [x])),
    ('latex math', 'latex_math', ('begin_math', 'math', 'end_math'), DEFAULT_PRECEDENCE, lambda _, x, __ : x),
    ('inline math', 'inline_text', ('latex_math',), DEFAULT_PRECEDENCE, lambda x : '$' + x + '$'),
    ('dummy math test', 'inline_text', ('$$$$',), DEFAULT_PRECEDENCE, lambda x : x)
]

math_tokens = set([
    '(', ')', '{', '}', '<', '>', '(|', '|)', '[:', ':]',
    '=', '!=',
    '>=','<=',
    '=>', 'and','or','not','iff','<=>','<==>',
    'in', 'to', 'maps', '->', 'notin',
    '|=', '|-',
    '|',
    'empty', 'for', 'all', 'exists',
    'from', 'over', 'of',
    'sum', 'product', 'integral', 'fraction',
    'sup',
    'sub',
    '_]',
    '[_',
    '^]',
    '[^',
    'C', 'R', 'Q', 'Z', 'N',
    '+', 'dot', 'times',
    'pi', 'theta', 'alpha', 'epsilon', 'xi',
    'Pi', 'Theta', 'Alpha', 'Epsilon', 'Xi',
    'vector', 'hat', 'check', 'bar', 'ring', 'tilde'
])

with_special = {t : f"@@token@@{i}" for (i, t) in enumerate(math_tokens) if set(t) & SPECIAL_CHARACTERS and len(t) > 1}
without_special = {v : k for (k, v) in with_special.items()}

math_dsl = [
    # DSL-specific
    ('Magic wand', 'math', ('[:', 'math', ':]'), DEFAULT_PRECEDENCE + 15, lambda _, x, __ : x),
    # Delimiters
    ('left parenthesis', 'delim', ('(',), DEFAULT_PRECEDENCE, lambda x: x),
    ('right parenthesis', 'delim', (')',), DEFAULT_PRECEDENCE, lambda x: x),
    ('left brace', 'delim', ('{',), DEFAULT_PRECEDENCE, lambda _: r'\lbrace'),
    ('right brace', 'delim', ('}',), DEFAULT_PRECEDENCE, lambda _: r'\rbrace'),
    ('left angle bracket', 'delim', ('<',), DEFAULT_PRECEDENCE, lambda _: r'\langle'),
    ('right angle bracket', 'delim', ('>',), DEFAULT_PRECEDENCE, lambda _: r'\rangle'),
    ('left vertical bar', 'delim', ('(|',), DEFAULT_PRECEDENCE, lambda _: r'\lvert'),
    ('right vertical bar', 'delim', ('|)',), DEFAULT_PRECEDENCE, lambda _: r'\rvert'),
    # Common relations
    ('equal', 'inf', ('=',), DEFAULT_PRECEDENCE, lambda x: x),
    ('not equal', 'inf', ('!=',), DEFAULT_PRECEDENCE, lambda _: r'\neq'),
    ('greater or equal', 'inf', ('>=',), DEFAULT_PRECEDENCE, lambda _: r'\ge'),
    ('less or equal', 'inf', ('<=',), DEFAULT_PRECEDENCE, lambda _: r'\le'),
    # Basic notation for sets, functions, propositional and predicate logic
    ('and', 'inf', ('and',), DEFAULT_PRECEDENCE, lambda _: r'\land'),
    ('or', 'inf', ('or',), DEFAULT_PRECEDENCE, lambda _: r'\lor'),
    ('not', 'inf', ('not',), DEFAULT_PRECEDENCE, lambda _: r'\neg'),
    ('iff', 'inf', ('iff',), DEFAULT_PRECEDENCE, lambda _: r'\Leftrightarrow'),
    ('<=>', 'inf', ('<=>',), DEFAULT_PRECEDENCE, lambda _: r'\Leftrightarrow'),
    ('=>', 'inf', ('=>',), DEFAULT_PRECEDENCE, lambda _: r'\Rightarrow'),
    ('==>', 'inf', ('==>',), DEFAULT_PRECEDENCE, lambda _: r'\Longrightarrow'),
    ('<==>', 'inf', ('<==>',), DEFAULT_PRECEDENCE, lambda _: r'\Longleftrightarrow'),
    ('in', 'inf', ('in',), DEFAULT_PRECEDENCE, lambda x: r'\in'),
    ('notin', 'inf', ('notin',), DEFAULT_PRECEDENCE, lambda _, __: r'\notin'),
    ('not in', 'math', ('not', 'in',), DEFAULT_PRECEDENCE + 5, lambda _, __: r'\notin'),
    ('maps to', 'inf', ('maps', 'to',), DEFAULT_PRECEDENCE + 5, lambda _, __: 'r\mapsto'),
    ('maps to', 'inf', ('->',), DEFAULT_PRECEDENCE + 5, lambda _, __: r'\rightarrow'),
    # maps to via
    # inclusion (left and right)
    ('empty', 'elem', ('empty',), DEFAULT_PRECEDENCE, lambda x : r'\emptyset'),
    ('empty', 'elem', ('ø',), DEFAULT_PRECEDENCE, lambda x : r'\emptyset'),
    ('for all', 'math', ('for', 'all',), DEFAULT_PRECEDENCE + 5, lambda _, __ : r'\forall'),
    ('exists', 'pref', ('exists',), DEFAULT_PRECEDENCE, lambda x : r'\exists'),
    ('vert', 'delim', ('|',), DEFAULT_PRECEDENCE, lambda x : r'\vert'),
    # Subindices, superindices and diacritics
    ('sub', 'math', ('math', 'sub', '[:', 'math', ':]'), DEFAULT_PRECEDENCE + 10, lambda x, _,__, y, ___ : x + '_{' + y + '}'),
    ('super', 'math', ('math', 'sup', '[:', 'math', ':]'), DEFAULT_PRECEDENCE + 10, lambda x, _, __, y, ___ : x + '^{' + y + '}'),
    ('short sub', 'math', ('math', 'sub', 'name'), DEFAULT_PRECEDENCE + 5, lambda x, _, y : x + '_{' + y + '}'),
    ('short super', 'math', ('math', 'sup', 'name'), DEFAULT_PRECEDENCE + 5, lambda x, _, y : x + '^{' + y + '}'),
    # ', ^, bar, hat, tilde, vector
    ('vector', 'name', ('name', 'vector'), DEFAULT_PRECEDENCE, lambda x, _ : r'\vec{x}'),
    ('hat', 'name', ('name', 'hat'), DEFAULT_PRECEDENCE, lambda x, _ : r'\bar{x}'),
    ('check', 'name', ('name', 'check'), DEFAULT_PRECEDENCE, lambda x, _ : r'\check{x}'),
    ('bar', 'name', ('name', 'bar'), DEFAULT_PRECEDENCE, lambda x, _ : r'\bar{x}'),
    ('ring', 'name', ('name', 'ring'), DEFAULT_PRECEDENCE, lambda x, _ : r'\mathring{x}'),
    ('tilde', 'name', ('name', 'tilde'), DEFAULT_PRECEDENCE, lambda x, _ : r'\tilde{x}'),
    # Common operations
    ('sum', 'op', ('sum',), DEFAULT_PRECEDENCE, lambda x : r'\sum'),
    ('product', 'op', ('product',), DEFAULT_PRECEDENCE, lambda x : r'\prod'),
    ('integral', 'op', ('integral',), DEFAULT_PRECEDENCE, lambda x : r'\int'),
    ('op from to', 'math', ('op', 'from', 'math', 'to', 'math', 'of', 'math',), DEFAULT_PRECEDENCE + 10, lambda o, _, s, __, b, ___, f : big_operator(o) + '_{' + s + '}^{' + b + '}' + f' {f}'),
    ('inf from to', 'math', ('op', 'from', 'math', 'to', 'math', 'of', 'math',), DEFAULT_PRECEDENCE + 10, lambda o, _, s, __, b, ___, f : big_operator(o) + '_{' + s + '}^{' + b + '}' + f' {f}'),
    ('op over', 'math', ('op', 'over', 'math', 'of', 'math',), DEFAULT_PRECEDENCE + 10, lambda o, _, s, __, f : big_operator(o) + '_{' + s + '} ' + f),
    # R, Q, C, Z, aleph, epsilon,
    ('reals', 'name', ('R',), DEFAULT_PRECEDENCE, lambda x : r'\R'),
    ('complex', 'name', ('C',), DEFAULT_PRECEDENCE, lambda x : r'\Complex'),
    ('rationals', 'name', ('Q',), DEFAULT_PRECEDENCE, lambda x : r'\Q'),
    ('integers', 'name', ('Z',), DEFAULT_PRECEDENCE, lambda x : r'\Z'),
    ('naturals', 'name', ('N',), DEFAULT_PRECEDENCE, lambda x : r'\N'),
    # Common operations
    ('plus', 'inf', ('+',), DEFAULT_PRECEDENCE, IDENTITY),
    ('dot', 'inf', ('dot',), DEFAULT_PRECEDENCE, lambda x : r'\cdot'),
    ('times', 'inf', ('times',), DEFAULT_PRECEDENCE, lambda x : r'\times'),
    ('large fraction', 'math', ('fraction', '(', 'math', 'over', 'math', ')'), DEFAULT_PRECEDENCE, lambda _, __, x, ___, y, ____ : r'\frac{ ' + x + ' }{ ' + y + ' }'),
    ('small fraction', 'math', ('name', 'over', 'name'), DEFAULT_PRECEDENCE, lambda x, _, y : r'\frac{ ' + x + ' }{ ' + y + ' }'),
    # Greek
    ('pi', 'name', ('pi',), DEFAULT_PRECEDENCE, lambda x : r'\pi'),
    ('Pi', 'name', ('pi',), DEFAULT_PRECEDENCE, lambda x : r'\Pi'),
    ('theta', 'name', ('theta',), DEFAULT_PRECEDENCE, lambda x : r'\theta'),
    ('Theta', 'name', ('Theta',), DEFAULT_PRECEDENCE, lambda x : r'\Theta'),
    ('alpha', 'name', ('alpha',), DEFAULT_PRECEDENCE, lambda x : r'\alpha'),
    ('Alpha', 'name', ('Alpha',), DEFAULT_PRECEDENCE, lambda x : r'\Alpha'),
    ('xi', 'name', ('xi',), DEFAULT_PRECEDENCE, lambda x : r'\xi'),
    ('Xi', 'name', ('Xi',), DEFAULT_PRECEDENCE, lambda x : r'\Xi'),
    ('epsilon', 'name', ('epsilon',), DEFAULT_PRECEDENCE, lambda x : r'\varepsilon'),
    ('Epsilon', 'name', ('Epsilon',), DEFAULT_PRECEDENCE, lambda x : r'E'),
    # Logic
    ('derives', 'inf', ('|-',), DEFAULT_PRECEDENCE, lambda x : r'\vdash'),
    ('consequence', 'inf', ('|=',), DEFAULT_PRECEDENCE, lambda x : r'\vDash'),
    # Math elements
    ('math', 'math', ('math', 'math'), DEFAULT_PRECEDENCE - 5, lambda x, y : x + ' ' + y),
    ('element', 'math', ('elem',), DEFAULT_PRECEDENCE - 5, lambda x : x),
    ('infix', 'math', ('inf',), DEFAULT_PRECEDENCE - 5, lambda x : x),
    ('prefix', 'math', ('pref',), DEFAULT_PRECEDENCE - 5, lambda x : x),
    ('posfix', 'math', ('pos',), DEFAULT_PRECEDENCE - 5, lambda x : x),
    ('delimiter', 'math', ('delim',), DEFAULT_PRECEDENCE - 5, lambda x : x),
    ('name', 'math', ('name',), DEFAULT_PRECEDENCE - 5, lambda x : x)
]
