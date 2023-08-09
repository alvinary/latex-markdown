from constants import *

# Handle generic latex macros

def squareArgs(squares):
    if squares:
        return f'{LEFT_SQUARE}{", ".join(squares)}{RIGHT_SQUARE}'
    else:
        return ''
        
def curlyArgs(curly):
    if curly:
        return LEFT_CURLY + ', '.join([c for c in curly]) + RIGHT_CURLY
    else:
        return ''

def indent(text, depth=2):
    lines = text.split(NEWLINE)
    lines = [' ' * depth + line for line in lines]
    return NEWLINE.join(lines)

def singleMacro(name):
    return f"{BACKSLASH}{name}"

def macro(name, curly, squares=[]):
    first =  f'{BACKSLASH}{name}' + squareArgs(squares)
    last = curlyArgs(curly)
    return first + last
    
def begin(name):
    return f'{BEGIN}{LEFT_CURLY}{name}{RIGHT_CURLY}'
    
def end(name):
    return f'{END}{LEFT_CURLY}{name}{RIGHT_CURLY}'

def beginEnd(name, content, squares=[], curly=[]):
    _begin = begin(name) + BREAK
    _args = squareArgs(squares) + curlyArgs(curly)
    _content = indent(content) + BREAK
    _end = end(name)
    listing = [_begin, _args, _content, _end]
    if '' in listing:
        listing.remove('')
    return NEWLINE.join(listing)

# Common beamer macros

def frame(content):
    return beginEnd('frame', content)

def theme(_theme):
    return macro('usetheme', [_theme])

def colors(_colorTheme):
    return macro('usecolortheme', [_colorTheme])
    
def titleFrame():
    return macro('frame', [BACKSLASH + 'titlepage'])

def frameTitle(_title):
    return macro('frametitle', [_title])

def beamerDocument(_titleframe, content):
    _class = macro('documentclass', ['beamer'])
    _author = author(_author)
    _date = date(_date)
    _titleFrame = titleFrame()
    content = beginEnd('document', [content])
    return BREAK.join([_class, _titleFrame, titleFrame(), content])

def box(subtitle, text):
    return beginEnd('block', text, curly=[subtitle])

# Common latex macros

def document(documentClass, content):
    _documentClass = macro('documentclass', [documentClass])
    _packages = macro('usepackage', ['amsmath'])
    _documentContent = beginEnd('document', content)
    return f"{_documentClass}{BREAK}{_documentContent}"
    
def article(content):
    return document('article', content)

def title(titleText):
    return macro('title', [titleText])
    
def author(_author):
    return macro('author', [_author])
    
def date(_date):
    return macro('date', [_date])

def section(sectionTitle):
    return macro('section', [sectionTitle])
    
def subsection(subsectionTitle):
    return macro('section', [subsectionTitle])

def item(text, bullet=''):
    return f'{BACKSLASH}item{bullet} {text}'

def itemize(items, bullet=''):
    bulletPoints = indent(BREAK.join(items))
    return beginEnd('itemize', [bulletPoints])

def bold(text):
    return macro('textbf', [text])

def italics(text):
    return macro('textit', [text])

def typewriter(text):
    return macro('texttt', [text])
    
# bibtex

def citation(reference):
    return macro('citation', [reference])

# Auxiliary functions

big_version = {
    '\\cup' : '\\bigcup',
    '\\sum' : '\\sum',
    '\\prod' : '\\prod',
    '\\int' : '\\int',
    '\\cap' : '\\bigcap',
    '\\wedge' : '\\bigwedge',
    '\\vee' : '\\bigvee'
}

def big_operator(operator_name):
    return big_version[operator_name]
