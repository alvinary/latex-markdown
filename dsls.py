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
    "--",
    "```",
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
    ('inline text right', 'text', ('inline_text', 'text'), DEFAULT_PRECEDENCE - 5, lambda x, y : x + SPACE + y),
    ('text and text', 'text', ('text', 'text'), DEFAULT_PRECEDENCE, lambda x, y : x + ' ' + SPACE + y),
    ('blank', 'block', ('--', 'break'), DEFAULT_PRECEDENCE, lambda _, __ : r'\bigbreak'),
    # Special symbols for titles, sections, and subsections
    ('section mark', 'section_mark', ("#",), DEFAULT_PRECEDENCE, IDENTITY),
    ('subsection mark', 'subsection_mark', ("##",), DEFAULT_PRECEDENCE, IDENTITY),
    ('subsubsection', 'subsubsection_mark', ("###",), DEFAULT_PRECEDENCE, IDENTITY),
    # Document hierarchy
    ('section', 'block', ('section_mark', 'text', 'break'), DEFAULT_PRECEDENCE, lambda _, x, __  : section(x)),
    ('subsection', 'block', ('subsection_mark', 'text', 'break'), DEFAULT_PRECEDENCE, lambda _, x, __  : subsection(x)),
    ('subsubsection', 'block', ('subsubsection_mark', 'text', 'break'), DEFAULT_PRECEDENCE, lambda _, x, __  : subsubsection(x)),
    # Listings
    ('itemize', 'block', ('items',), DEFAULT_PRECEDENCE, lambda x : itemize(x)),
    ('items', 'items', ('single_item', 'break', 'items'), DEFAULT_PRECEDENCE + 10, lambda x, y, z : x + y + z),
    ('single item', 'single_item', ('*', 'text',), DEFAULT_PRECEDENCE, lambda _, x : item(x)),
    ('items', 'items', ('single_item', 'break'), DEFAULT_PRECEDENCE, lambda x, _ : x),
    # Code blocks
    ('code', 'block', ('```', 'break', 'blocks', '```'), DEFAULT_PRECEDENCE, lambda _1, _2, x, _3, _4 : beginEnd('verbatim*', x)),
    ('code', 'block', ('```', 'break', 'block', '```'), DEFAULT_PRECEDENCE, lambda _1, _2, x, _3, _4 : beginEnd('verbatim*', x)),
    # TODO: do this with iterator concatenation to avoid copying and pasting a thousand times the same list
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
    ('default math block', 'block', ('begin_math', 'math', 'end_math', 'break'), DEFAULT_PRECEDENCE, lambda ___, x, _, __ : '\[ ' + x + ' \]'),
    ('latex math', 'latex_math', ('begin_math', 'math', 'end_math'), DEFAULT_PRECEDENCE, lambda _, x, __ : x),
    ('inline math', 'inline_text', ('latex_math',), DEFAULT_PRECEDENCE, lambda x : '$' + x + '$'),
    ('dummy math test', 'inline_text', ('$$$$',), DEFAULT_PRECEDENCE, lambda x : x)
]

math_tokens = [
    '(', ')', '{', '}', '<', '>', '(|', '|)', '[:', ':]', '(-', '-)',
    '=', '!=',
    '>=','<=',
    '=>', 'and','or','not','iff','<=>','<==>',
    'in', 'to', 'maps', '->', 'notin',
    '|=', '|-',
    '|',
    'empty', 'for', 'all', 'exists',
    'from', 'over', 'of',
    'sum', 'product', 'integral', 'fraction', 'gradient',
    'infinity',
    'sup',
    'sub',
    '_]',
    '[_',
    '^]',
    '[^',
    '|C', '|R', '|Q', '|Z', '|N',
    '+', 'dot', 'times',
    'vector', 'hat', 'check', 'bar', 'ring', 'tilde',
    'subset', 'superset', 'strict, square, root', '-h-',
    'raise', 'lower', 'partial'
]

greek_letters = '''
Alpha	Beta	Gamma	Delta
Epsilon	Zeta	Eta	Theta
Iota	Kappa	Lambda	Mu
Nu	Xi	Omicron	Pi
Rho	Sigma	Tau	Upsilon
Phi	Chi	Psi	Omega
varGamma	varDelta	varTheta	 varLambda
varXi	varPi	varSigma	varUpsilon
varPhi	varPsi	varOmega	
alpha	beta	gamma	delta
epsilon	zeta	eta	theta
iota	kappa	lambda	mu
nu xi	omicron	pi
rho	sigma	tau	upsilon
phi	chi	psi	omega
varepsilon	varkappa	vartheta	thetasym
varpi	varrho	varsigma	varphi
digamma
'''.split()

math_tokens = math_tokens + greek_letters

clash_tokens = {'(|', '|)', '[:', ':]', '>=','<=', '-h-',
    '=>', '<=>','<==>', '->', '|=', '|-',
    '_]', '[_', '^]', '[^', '|C', '|R', '|Q', '|Z', '|N', '(-', '-)'}

with_special = {t : f"@@token@@{i}" for (i, t) in enumerate(math_tokens) if t in clash_tokens}
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
    # Grouping 
    ('paren', 'math', ('(', 'math', ')'), DEFAULT_PRECEDENCE + 5, lambda x, y, w : x + y + w),
    ('bars', 'math', ('(|', 'math', '|)'), DEFAULT_PRECEDENCE + 5, lambda x, y, ww : r'\lvert ' + y + r' \rvert'),
    ('square brackets', 'math', ('[', 'math', ']'), DEFAULT_PRECEDENCE + 5, lambda x, y, www : x + y + www),
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
    ('maps to', 'inf', ('->',), DEFAULT_PRECEDENCE + 5, lambda _ : r'\rightarrow'),
    # maps to via
    # Set inclusions
    ('subset', 'inf', ('subset', 'of'), DEFAULT_PRECEDENCE + 2, lambda _, __ : r'\subseteq'),
    ('superset', 'inf', ('superset', 'of'), DEFAULT_PRECEDENCE + 2, lambda _, __ : r'\supseteq'),
    ('strict subset', 'inf', ('strict', 'subset', 'of'), DEFAULT_PRECEDENCE + 5, lambda _, __, ___ : r'\subseteq'),
    ('strict superset', 'inf', ('strict', 'superset', 'of'), DEFAULT_PRECEDENCE + 5, lambda _, __, ___ : r'\supseteq'),
    ('not subset', 'inf', ('not', 'subset', 'of'), DEFAULT_PRECEDENCE + 10, lambda _, __, ___ : r'\nsubseteq'),
    ('not superset', 'inf', ('not', 'superset', 'of'), DEFAULT_PRECEDENCE + 10, lambda _, __, ___ : r'\nsupseteq'),
    ('not strict subset', 'inf', ('not','strict',  'subset', 'of'), DEFAULT_PRECEDENCE + 15, lambda _, __, ___, ____ : r'\nsubset'),
    ('not strict superset', 'inf', ('not','strict',  'superset', 'of'), DEFAULT_PRECEDENCE + 15, lambda _, __, ___, ____ : r'\nsupset'),
    # Quantifiers, empty set and cardinal
    ('empty', 'elem', ('empty',), DEFAULT_PRECEDENCE, lambda x : r'\emptyset'),
    ('empty', 'elem', ('ø',), DEFAULT_PRECEDENCE, lambda x : r'\emptyset'),
    ('for all', 'math', ('for', 'all',), DEFAULT_PRECEDENCE + 5, lambda _, __ : r'\forall'),
    ('exists', 'pref', ('exists',), DEFAULT_PRECEDENCE, lambda x : r'\exists'),
    ('vert', 'delim', ('|',), DEFAULT_PRECEDENCE, lambda x : r'\vert'),
    # Subindices and superindices
    ('sub', 'math', ('math', 'sub', 'marked_math'), DEFAULT_PRECEDENCE + 10, lambda x, _, y : x + '_{' + y + '}'),
    ('super', 'math', ('math', 'sup', 'marked_math'), DEFAULT_PRECEDENCE + 10, lambda x, _, y : x + '^{' + y + '}'),
    ('short sub', 'math', ('math', 'sub', 'name'), DEFAULT_PRECEDENCE + 5, lambda x, _, y : x + '_{' + y + '}'),
    ('short super', 'math', ('math', 'sup', 'name'), DEFAULT_PRECEDENCE + 5, lambda x, _, y : x + '^{' + y + '}'),
    # Diactritics: ', ^, bar, hat, tilde, vector
    ('vector', 'name', ('name', 'vector'), DEFAULT_PRECEDENCE, lambda x, _ : r'\vec{' + x + '}'),
    ('hat', 'name', ('name', 'hat'), DEFAULT_PRECEDENCE, lambda x, _ : r'\hat{' + x + '}'),
    ('check', 'name', ('name', 'check'), DEFAULT_PRECEDENCE, lambda x, _ : r'\check{' + x + '}'),
    ('bar', 'name', ('name', 'bar'), DEFAULT_PRECEDENCE, lambda x, _ : r'\bar{' + x + '}'),
    ('ring', 'name', ('name', 'ring'), DEFAULT_PRECEDENCE, lambda x, _ : r'\mathring{' + x + '}'),
    ('tilde', 'name', ('name', 'tilde'), DEFAULT_PRECEDENCE, lambda x, _ : r'\tilde{' + x + '}'),
    # Common 'big operator' operations
    ('gradient', 'op', ('gradient',), DEFAULT_PRECEDENCE, lambda x : r'\nabla'),
    ('partial', 'name', ('partial',), DEFAULT_PRECEDENCE, lambda x : r'\partial'),
    ('sum', 'op', ('sum',), DEFAULT_PRECEDENCE, lambda x : r'\sum'),
    ('product', 'op', ('product',), DEFAULT_PRECEDENCE, lambda x : r'\prod'),
    ('integral', 'op', ('integral',), DEFAULT_PRECEDENCE, lambda x : r'\int'),
    ('op from to', 'math', ('op', 'from', 'marked_math', 'to', 'marked_math', 'of', 'marked_math',), DEFAULT_PRECEDENCE + 10, lambda o, _, s, __, b, ___, f : big_operator(o) + '_{' + s + '}^{' + b + '}' + f' {f}'),
    ('inf from to', 'math', ('op', 'from', 'marked_math', 'to', 'marked_math', 'of', 'marked_math',), DEFAULT_PRECEDENCE + 10, lambda o, _, s, __, b, ___, f : big_operator(o) + '_{' + s + '}^{' + b + '}' + f' {f}'),
    ('op over', 'math', ('op', 'over', 'marked_math', 'of', 'marked_math',), DEFAULT_PRECEDENCE + 10, lambda o, _, s, __, f : big_operator(o) + '_{' + s + '} ' + f),
    ('op of', 'math', ('op', 'of', 'marked_math',), DEFAULT_PRECEDENCE + 10, lambda o, _, f : big_operator(o) + '{' + f + '} '),
    # Greek letters
    ("Alpha", "name", ("Alpha",), DEFAULT_PRECEDENCE, lambda x: "\\Alpha"),
    ("Beta", "name", ("Beta",), DEFAULT_PRECEDENCE, lambda x: "\\Beta"),
    ("Gamma", "name", ("Gamma",), DEFAULT_PRECEDENCE, lambda x: "\\Gamma"),
    ("Delta", "name", ("Delta",), DEFAULT_PRECEDENCE, lambda x: "\\Delta"),
    ("Epsilon", "name", ("Epsilon",), DEFAULT_PRECEDENCE, lambda x: "\\Epsilon"),
    ("Zeta", "name", ("Zeta",), DEFAULT_PRECEDENCE, lambda x: "\\Zeta"),
    ("Eta", "name", ("Eta",), DEFAULT_PRECEDENCE, lambda x: "\\Eta"),
    ("Theta", "name", ("Theta",), DEFAULT_PRECEDENCE, lambda x: "\\Theta"),
    ("Iota", "name", ("Iota",), DEFAULT_PRECEDENCE, lambda x: "\\Iota"),
    ("Kappa", "name", ("Kappa",), DEFAULT_PRECEDENCE, lambda x: "\\Kappa"),
    ("Lambda", "name", ("Lambda",), DEFAULT_PRECEDENCE, lambda x: "\\Lambda"),
    ("Mu", "name", ("Mu",), DEFAULT_PRECEDENCE, lambda x: "\\Mu"),
    ("Nu", "name", ("Nu",), DEFAULT_PRECEDENCE, lambda x: "\\Nu"),
    ("Xi", "name", ("Xi",), DEFAULT_PRECEDENCE, lambda x: "\\Xi"),
    ("Omicron", "name", ("Omicron",), DEFAULT_PRECEDENCE, lambda x: "\\Omicron"),
    ("Pi", "name", ("Pi",), DEFAULT_PRECEDENCE, lambda x: "\\Pi"),
    ("Rho", "name", ("Rho",), DEFAULT_PRECEDENCE, lambda x: "\\Rho"),
    ("Sigma", "name", ("Sigma",), DEFAULT_PRECEDENCE, lambda x: "\\Sigma"),
    ("Tau", "name", ("Tau",), DEFAULT_PRECEDENCE, lambda x: "\\Tau"),
    ("Upsilon", "name", ("Upsilon",), DEFAULT_PRECEDENCE, lambda x: "\\Upsilon"),
    ("Phi", "name", ("Phi",), DEFAULT_PRECEDENCE, lambda x: "\\Phi"),
    ("Chi", "name", ("Chi",), DEFAULT_PRECEDENCE, lambda x: "\\Chi"),
    ("Psi", "name", ("Psi",), DEFAULT_PRECEDENCE, lambda x: "\\Psi"),
    ("Omega", "name", ("Omega",), DEFAULT_PRECEDENCE, lambda x: "\\Omega"),
    ("varGamma", "name", ("varGamma",), DEFAULT_PRECEDENCE, lambda x: "\\varGamma"),
    ("varDelta", "name", ("varDelta",), DEFAULT_PRECEDENCE, lambda x: "\\varDelta"),
    ("varTheta", "name", ("varTheta",), DEFAULT_PRECEDENCE, lambda x: "\\varTheta"),
    ("varLambda", "name", ("varLambda",), DEFAULT_PRECEDENCE, lambda x: "\\varLambda"),
    ("varXi", "name", ("varXi",), DEFAULT_PRECEDENCE, lambda x: "\\varXi"),
    ("varPi", "name", ("varPi",), DEFAULT_PRECEDENCE, lambda x: "\\varPi"),
    ("varSigma", "name", ("varSigma",), DEFAULT_PRECEDENCE, lambda x: "\\varSigma"),
    ("varUpsilon", "name", ("varUpsilon",), DEFAULT_PRECEDENCE, lambda x: "\\varUpsilon"),
    ("varPhi", "name", ("varPhi",), DEFAULT_PRECEDENCE, lambda x: "\\varPhi"),
    ("varPsi", "name", ("varPsi",), DEFAULT_PRECEDENCE, lambda x: "\\varPsi"),
    ("varOmega", "name", ("varOmega",), DEFAULT_PRECEDENCE, lambda x: "\\varOmega"),
    ("alpha", "name", ("alpha",), DEFAULT_PRECEDENCE, lambda x: "\\alpha"),
    ("beta", "name", ("beta",), DEFAULT_PRECEDENCE, lambda x: "\\beta"),
    ("gamma", "name", ("gamma",), DEFAULT_PRECEDENCE, lambda x: "\\gamma"),
    ("delta", "name", ("delta",), DEFAULT_PRECEDENCE, lambda x: "\\delta"),
    ("epsilon", "name", ("epsilon",), DEFAULT_PRECEDENCE, lambda x: "\\epsilon"),
    ("zeta", "name", ("zeta",), DEFAULT_PRECEDENCE, lambda x: "\\zeta"),
    ("eta", "name", ("eta",), DEFAULT_PRECEDENCE, lambda x: "\\eta"),
    ("theta", "name", ("theta",), DEFAULT_PRECEDENCE, lambda x: "\\theta"),
    ("iota", "name", ("iota",), DEFAULT_PRECEDENCE, lambda x: "\\iota"),
    ("kappa", "name", ("kappa",), DEFAULT_PRECEDENCE, lambda x: "\\kappa"),
    ("lambda", "name", ("lambda",), DEFAULT_PRECEDENCE, lambda x: "\\lambda"),
    ("mu", "name", ("mu",), DEFAULT_PRECEDENCE, lambda x: "\\mu"),
    ("nu", "name", ("nu",), DEFAULT_PRECEDENCE, lambda x: "\\nu"),
    ("xi", "name", ("xi",), DEFAULT_PRECEDENCE, lambda x: "\\xi"),
    ("omicron", "name", ("omicron",), DEFAULT_PRECEDENCE, lambda x: "\\omicron"),
    ("pi", "name", ("pi",), DEFAULT_PRECEDENCE, lambda x: "\\pi"),
    ("rho", "name", ("rho",), DEFAULT_PRECEDENCE, lambda x: "\\rho"),
    ("sigma", "name", ("sigma",), DEFAULT_PRECEDENCE, lambda x: "\\sigma"),
    ("tau", "name", ("tau",), DEFAULT_PRECEDENCE, lambda x: "\\tau"),
    ("upsilon", "name", ("upsilon",), DEFAULT_PRECEDENCE, lambda x: "\\upsilon"),
    ("phi", "name", ("phi",), DEFAULT_PRECEDENCE, lambda x: "\\phi"),
    ("chi", "name", ("chi",), DEFAULT_PRECEDENCE, lambda x: "\\chi"),
    ("psi", "name", ("psi",), DEFAULT_PRECEDENCE, lambda x: "\\psi"),
    ("omega", "name", ("omega",), DEFAULT_PRECEDENCE, lambda x: "\\omega"),
    ("varepsilon", "name", ("varepsilon",), DEFAULT_PRECEDENCE, lambda x: "\\varepsilon"),
    ("varkappa", "name", ("varkappa",), DEFAULT_PRECEDENCE, lambda x: "\\varkappa"),
    ("vartheta", "name", ("vartheta",), DEFAULT_PRECEDENCE, lambda x: "\\vartheta"),
    ("thetasym", "name", ("thetasym",), DEFAULT_PRECEDENCE, lambda x: "\\thetasym"),
    ("varpi", "name", ("varpi",), DEFAULT_PRECEDENCE, lambda x: "\\varpi"),
    ("varrho", "name", ("varrho",), DEFAULT_PRECEDENCE, lambda x: "\\varrho"),
    ("varsigma", "name", ("varsigma",), DEFAULT_PRECEDENCE, lambda x: "\\varsigma"),
    ("varphi", "name", ("varphi",), DEFAULT_PRECEDENCE, lambda x: "\\varphi"),
    ("digamma", "name", ("digamma",), DEFAULT_PRECEDENCE, lambda x: "\\digamma"),    
    # Commonly used sets
    ('reals', 'name', ('|R',), DEFAULT_PRECEDENCE, lambda x : r'\mathbb{R' + '}'),
    ('complex', 'name', ('|C',), DEFAULT_PRECEDENCE, lambda x : r'\mathbb{Complex' + '}'),
    ('rationals', 'name', ('|Q',), DEFAULT_PRECEDENCE, lambda x : r'\mathbb{Q' + '}'),
    ('integers', 'name', ('|Z',), DEFAULT_PRECEDENCE, lambda x : r'\mathbb{Z' + '}'),
    ('naturals', 'name', ('|N',), DEFAULT_PRECEDENCE, lambda x : r'\mathbb{N' + '}'),
    # Commonly used operations
    ('plus', 'inf', ('+',), DEFAULT_PRECEDENCE, IDENTITY),
    ('dot', 'inf', ('dot',), DEFAULT_PRECEDENCE, lambda x : r'\cdot'),
    ('times', 'inf', ('times',), DEFAULT_PRECEDENCE, lambda x : r'\times'),
    ('large fraction', 'math', ('marked_math', 'over', 'marked_math'), DEFAULT_PRECEDENCE, lambda x, _, y : r'\frac{ ' + x + ' }{ ' + y + ' }'),
    ('small fraction', 'math', ('name', 'over', 'name'), DEFAULT_PRECEDENCE, lambda x, _, y : r'\frac{ ' + x + ' }{ ' + y + ' }'),
    ('square root', 'math', ('square', 'root', 'marked_math'), DEFAULT_PRECEDENCE, lambda __, _, x : r'\sqrt{ ' + x + ' }'),
    ('nth root', 'math', ('name', 'root', 'marked_math'), DEFAULT_PRECEDENCE, lambda y, _, x : r'\sqrt[' + y + ']{ ' + x + ' }'),
    # Commonly used symbols and constants
    ('infinity', 'name', ('infinity'), DEFAULT_PRECEDENCE, lambda x : r'\infty'),
    # Logic
    ('derives', 'inf', ('|-',), DEFAULT_PRECEDENCE, lambda x : r'\vdash'),
    ('consequence', 'inf', ('|=',), DEFAULT_PRECEDENCE, lambda x : r'\vDash'),
    # Quantum Mechanics
    ('reduced plank constant', 'name', ('-h-', ), DEFAULT_PRECEDENCE, lambda x : r'\hbar'),
    #('bra', 'name', ('<', 'math', '|'), DEFAULT_PRECEDENCE, lambda _, x, __ : r'\Bra{' + x  + '|}'),
    #('ket', 'name', ('|', 'math', '>' ), DEFAULT_PRECEDENCE, lambda _, x, __ : r'\Ket{|' + x  + '}'),
    #('braket', 'name', ('<', 'math', '|', 'math', '>' ), DEFAULT_PRECEDENCE, lambda _, x, __, y, ___ : r'\Braket{' + x + ' | ' + y + '}'),
    # Assorted
    ('up arrow', 'name', ('raise',), DEFAULT_PRECEDENCE, lambda x: r'\upnarrow'),
    ('down arrow', 'name', ('lower',), DEFAULT_PRECEDENCE, lambda x: r'\downarrow'),
    # Math elements
    ('math', 'math', ('math', 'math'), DEFAULT_PRECEDENCE - 5, lambda x, y : x + ' ' + y),
    ('element', 'math', ('elem',), DEFAULT_PRECEDENCE - 5, lambda x : x),
    ('infix', 'math', ('inf',), DEFAULT_PRECEDENCE - 5, lambda x : x),
    ('prefix', 'math', ('pref',), DEFAULT_PRECEDENCE - 5, lambda x : x),
    ('posfix', 'math', ('pos',), DEFAULT_PRECEDENCE - 5, lambda x : x),
    ('delimiter', 'math', ('delim',), DEFAULT_PRECEDENCE - 5, lambda x : x),
    ('name', 'math', ('name',), DEFAULT_PRECEDENCE - 5, lambda x : x),
    ('marked math', 'marked_math', ('(-', 'math', '-)'), DEFAULT_PRECEDENCE, lambda _, x, __ : x),
    ('short marked math', 'marked_math', ('name', ), DEFAULT_PRECEDENCE, lambda x : x)
]

