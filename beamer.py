import re

from tale.cyk import *

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

SPECIAL_TOKENS = [STAR, TITLE, SECTION, SUBSECTION, THICK_BAR, SHORT_THICK_BAR, UNDERSCORE, THIN_BAR, EXPLICIT_NEWLINE, EXPLICIT_TAB]

underscores = re.compile('_____[_]+')
thickBar = re.compile('=====[=]+')

TEXT_TOKEN = 'text'
SPECIAL_TOKEN = 'special'

# Handle generic latex macros

def squareArgs(square):
    if square:
        return f'{LEFT_SQUARE}{", ".join(squares)}{RIGHT_SQUARE}'
    else:
        return ''
        
def curlyArgs(curly):
    if curly:
        return ''.join(['{' + c + '}' for c in curly])
    else:
        return ''

def indent(text, depth=2):
    lines = text.split(NEWLINE)
    lines = [' ' * depth + line for line in lines]
    return NEWLINE.join(lines)

def singleMacro(name):
    return f"{BACKSLASH}{name}"

def macro(name, curly, squares=[]):
    first =  f'{BACKSLASH}{NAME}' + squareArgs(squares)
    last = curlyArgs(curly)
    return first + last
    
def begin(name):
    return f'{BEGIN}{LEFT_CURLY}{name}{RIGHT_CURLY}'
    
def end(name):
    return f'{END}{LEFT_CURLY}{name}{RIGHT_CURLY}'

def beginEnd(name, content, squares=[], curly=[]):
    _begin = begin(name)
    _args = squareArgs(squares) + curlyArgs(curly)
    _content = indent(content)
    _end = end(name)
    listing = [_begin, _args, _content, _end]
    if '' in listing:
        listing.remove('')
    return NEWLINE.join(listing)

# Common beamer macros

def frame(content):
    return beginEnd('frame', content)

def theme(_theme):
    return macro('usetheme', _theme)

def colors(_colorTheme):
    return macro('usecolortheme', _colorTheme)

def title(_title):
    return macro('title', _title)
    
def author(_author):
    return macro('author', _author)
    
def date(_date):
    return macro('date', _date)
    
def titleFrame():
    return macro('frame', BACKSLASH + 'titlepage')

def frameTitle(_title):
    return macro('frametitle', _title)

def beamerDocument(_titleframe, content):
    _class = macro('documentclass', 'beamer')
    _author = author(_author)
    _date = date(_date)
    _titleFrame = titleFrame()
    content = beginEnd('document', content)
    return BREAK.join([_class, _titleFrame, titleFrame(), content])

def box(subtitle, text):
    return beginEnd('block', text, curly=[subtitle])

# Common latex macros

def item(text, bullet=''):
    return f'{BACKSLASH}item{bullet} {text}'

def itemize(items, bullet=''):
    bulletPoints = indent(BREAK.join(items))
    return beginEnd('itemize', bulletPoints)

def bold(text):
    return macro('textbf', text)

def italics(text):
    return macro('textit', text)

def typewriter(text):
    return macro('texttt', text)

# Small tests

testTitle = '\\title'

testItems = '''\\begin{itemize}
  \\item This is item 1
  \\item This is item 2
  \\item This is item 3
\\end{itemize}'''

resultTitle = singleMacro('title')

resultItems = beginEnd('itemize', '\n'.join([item(f'This is item {str(i)}') for i in [1, 2, 3]]))

assert resultTitle == testTitle
assert resultItems == testItems

# DSL

dslGrammar = '''
:= @

'''

# Images
# Setting titles for frames

'''for i in range(6):
    n itemize -> (n + 1) items

    n item -> nIndent bullet text
    n item -> nIndent bullet text (n+1)subitems

Y a la remil poronga
'''

# Text preprocessing

'''
* Replace ______+ with BAR and ====+ with THICK_BAR
* Replace tabs and newlines with EXPLICIT_TAB and EXPLICIT_NEWLINE
* Group all non-punctuation spans as 'text'
* Remove empty lines
'''

def preprocess(text):
    
    text = text.replace('\n', f' {EXPLICIT_NEWLINE} ')
    text = text.replace('\t', f' {EXPLICIT_TAB} ')
    
    pretokens = text.split()
    tokens = []
    currentText = ''
    
    for pretoken in pretokens:
        
        if underscores.match(pretoken):
            pretoken = THIN_BAR
        
        if thickBar.match(pretoken):
            pretoken = THICK_BAR
            
        if pretoken in SPECIAL_TOKENS:
            if currentText:
                tokens.append(currentText)
            tokens.append(pretoken)
            currentText = ''
        else:
            currentText += ' '
            currentText += pretoken
    
    return tokens

testText = '''# Common Words for Kitchen Items

____________

## Kitchen Items

If you are standing in a kitchen, you may find one or several of these items:

* A big plastic box that humms and has a door

* A small plastic box with a round door or
a lid that can be opened from above, with a strange cylinder with holes

== Note ======

The plastic things are all connected to a power supply, do not fiddle with them haphazardly

=======

_____________________

* The first item is called A FRIDGE
* The second item is a WASHING MACHINE

Both items are types of appliances


'''

# Math

'''
#inline
- does this thing inline any math looking stuff? Yes, it does
- it also inlines anythin between tildes ~mn~
- m hat is m hat, m tilde is m tilde, m tick es m tick
- what is the precedence of hat? the highest highest highest

- subindex i
- arrow over letter (like vectors)
- sums, integrals, etc
- matrices
- matrices with dots in the given direction

 1  ...  i  ...  n 
...             ...
 i      ...      i
...             ...
 n  ... i   ...  n
 
 
 
 | a b c | d
 | d e f | e
 | g h i | f
 
 ( a b c ) ( x_1 )
 ( d e f ) ( x_2 )
 ( g h i ) ( x_3 )

block

Math

  n
 Sum   f (i)
i = 1

<v, v>

<v-, v->

x _i '
x - (x arrow)

sum
    from i = 1
    to n
    of x_i hat <x-, y_i->
    
    
{ g (x) : x in S and f(x) = a }


'''

'''
integral from () to () of ()

~ n = m ~ 
~ RR ~

~ Letras bold, letras blackboard, letras blackboard no mistico~

:contents - table of contents -
:author
:institution

'''
    
def tagTokens(token):

    if token in SPECIAL_TOKENS:
        return SPECIAL_TOKEN 

    else:
        return TEXT_TOKEN
    
def toBeamer(markdown):
    tokens = preprocess(markdown)
    values = parserFromGrammar(dslGrammar, tag=tagTokens).value(tokens)
    if values:
        return values.pop(0)
        
example = '''
BEAMER MARKDOWN

Write Beamer Slides With A Clean DSL

____________________________________

What Is Beamer Markdown?

* Markdown is a plain text format that makes it
  easy to write human-readable rich text

* Markdown is a (WYASJHASJH) format, and not a (WSIWG)
  format

_____________________________________

* Markdown documents can be written easily on any
  editor, and are not visually messy, which has
  many advantages:
  
  * It's hard to miss spelling mistakes and text reads closer
    to the 'printed' / compiled version, which makes it
    easy to think of corrections

  * The number of lines in a markdown document bears  a direct
    relationship to the space taken by a certain part of a
    given text -- it's easier to know when something is too
    long when length can be determined visually or by comparing
    a couple of integers

  * The number of lines in a markdown document bear a direct
    relationship to the space taken by a certain part of a
    given text -- it's easier to get the right idea of size
    at a glance

____________________________________

Since everyone has so much to do, and their energy is better
spent doing something more useful than scratching their heads
before `pdflatex` error messages

==============================================

Why Not Just Have A Nice Markdown For Beamer?

==============================================

________________________________________

Now, latex has lots of features

Easily extensible

== Remark ====================================
You can always do stuff wrong
==============================================

_________________________________________
'''

basic = '''

leftTitle -> ~#
rightTitle -> #~

leftSection -> ~-
rightSection -> -~

leftSubsection -> ~+
rightSubsection -> +~

leftInline -> -[ 
rightInline -> ]- 

leftBlock -> =[
rightBlock -> ]=

line -> text newline

title -> [leftTitle] text [rightTitle]
title -> [] []
section -> [] []
subsection -> [] []
paragraph -> 

'''
    
print(toBeamer(example))
