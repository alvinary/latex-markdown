import logging
from contants import *
from dsls import *
from collections import defaultdict
from md_rules import Rules

class LatexMarkdown:

    def get_latex(self):
        raise NotImplemented

    def preprocess(self, text):
        raise NotImplemented

    def get_tokenized_tokens(self, token):
        if token in SPECIAL_TOKENS:
            return token 
        else:
            return TEXT_TOKEN
        

class toBeamer(LatexMarkdown):

    def get_latex(self, markdown):
        rules = Rules()
        tokens = self.preprocess(markdown)
        grammar = rules.parser_from_grammar(BeamerDSL)
        parse = grammar.parse(tokens)
        tokenized_tokens = self.get_tokenized_tokens(tokens)
        values = grammar.value(tokenized_tokens)
        if values:
            return values.pop(0)
        else:
            for span in parse.readable:
                print(span)

    def preprocess(self, text):
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
                if currentText:
                    currentText += ' '
                currentText += pretoken
        
        return tokens


class toMath(LatexMarkdown):

    def __init__(self):
        self.delimiters = {'(', ')', '{', '}', '[', ']', '<', '>'}

    def get_latex(self, markdown):
        rules = Rules()
        tokens = self.preprocess(markdown)
        grammar = rules.parser_from_grammar(mathDSL)
        parse = grammar.parse(tokens)
        tokenized_tokens = self.get_tokenized_tokens(tokens)
        values = grammar.value(tokenized_tokens)
        if values:
            return values.pop(0)
        else:
            for span in parse.readable:
                print(span)

    def preprocess(self, text):
    
        for d in self.delimiters:
            text = text.replace(d, f' {d} ')
            
        while '  ' in text:
            text = text.replace('  ', ' ')
            
        # Recover empty set
        text = text.replace('{ }', '{}')
        
        # Recover binary relations
        text = text.replace('> =', '>=')
        text = text.replace('< =', '<=')
        
        return text.split()
        

class Node:

    def __init__(self):
        self.items = list()
        self.ignore_items = set()


def tokensToRules(tokens, name):
    '''
       Input a sequence of tokens and a rule
       name and return the corresponding rule.
    '''

    if tokens[1] == LBRACE and tokens[-1] == RBRACE:
        rules = []
        head = tokens[0]
        members = tokens[2:-1]  # ignore '{' and '}'
        members = [s.strip()
                   for s in ''.join(members).split(',')]  # Remove commas
        for leaf in members[1:]:
            rules += unaryRule(head, leaf, name)
        return rules

    if len(tokens) == 2:
        head, branch = tuple(tokens)
        return unaryRule(head, branch, name)

    if len(tokens) == 3:
        head, left, right = tuple(tokens)
        return binaryRule(head, left, right, name)

    if len(tokens) > 3:
        return naryRule(tokens, name)


def binaryRule(head, left, right, name):
    return [((left, right), (head, name))]


def unaryRule(head, branch, name):
    return [(branch, (head, name))]


def naryRule(tokens, name):

    rules = []

    head = tokens.pop(0)
    left = tokens.pop(0)
    size = len(tokens)

    while tokens:

        auxiliaryRight = f"{name}[{size - len(tokens)}]"

        if len(tokens) == 1:

            right = tokens.pop(0)
            newRules = binaryRule(head, left, right, auxiliaryRight)
            rules += newRules

        else:
            newRules = binaryRule(head, left, auxiliaryRight, auxiliaryRight)
            rules += newRules
            head = auxiliaryRight
            left = tokens.pop(0)

    return rules




def checkSilent(token):
    if token[0] == "[" and token[-1] == "]":
        return token[1:-1], True
    else:
        return token, False


def isUnary(rhs):
    return not isinstance(rhs, tuple)


def isBinary(rhs):
    return isinstance(rhs, tuple) and len(rhs) == 2

'''
Argument accumulators

We pass these instead of Python sequences because
when working with collections f(*a) could be applied
to what is intended to be single argument, but happens
to be a Python sequence
'''

def semantics(grammar, triggers):

    actions = {}

    triggers['tab'] = lambda x: x
    triggers['space'] = lambda x: x
    triggers['newline'] = lambda x: x

    for rule in grammar:

        rhs, lhs = rule
        head, actionName = lhs

        if isBinary(rhs):

            left, right = rhs
            left, leftIsMute = checkSilent(left)
            right, rightIsMute = checkSilent(right)

            if actionName in triggers.keys():
                semanticAction = triggers[actionName]

            elif '[0]' in actionName:
                name = actionName.replace('[0]', '')
                semanticAction = triggers[name]

            else:
                semanticAction = variadicIdentity

            if leftIsMute and rightIsMute:
                argumentAction = ignoreBoth
            if leftIsMute and not rightIsMute:
                argumentAction = ignoreLeft

            if not leftIsMute and rightIsMute:
                argumentAction = ignoreRight
            if not leftIsMute and not rightIsMute:
                argumentAction = includeBoth

            actions[actionName] = (head, semanticAction, argumentAction)

        if isUnary(rhs):

            production, mute = checkSilent(rhs)
            semanticAction = triggers[actionName]

            if mute:
                argumentAction = emptyArgument
            else:
                argumentAction = encapsulate

            actions[actionName] = (head, semanticAction, argumentAction)

    return actions


justToken = lambda x: TOKEN




def getHead(span):
    return span[0]




# These are most special characters visible in a QWERTY keyboard
defaultSpecial = (
    '" ' +
    "< > ( ) { } [] / \\ ' ! = + - * & | % $ ^ ? @ # ~ ; : , . ").split()


def defaultTokenizer(string, specialCharacters=defaultSpecial):
    for p in defaultSpecial:
        string = string.replace(p, f' {p} ')
    return string.split()


def whitespaceTokenizer(string, specialCharacters=defaultSpecial):
    for p in defaultSpecial:
        string = string.replace(p, f' {p} ')
    string = " NEWLINE ".join(string.split(NEWLINE))
    string = " TAB ".join(string.split(TAB))
    string = " SPACE ".join(string.split(SPACE))
    return string.split()


inventory = lambda: defaultdict(lambda: set())

whitespaceRules = tokensToRules(['TAB', TAB], 'tab') + tokensToRules(
    ['NEWLINE', NEWLINE], 'newline') + tokensToRules(['SPACE', SPACE], 'space')


# Handle generic latex macros

def squareArgs(square):
    if square:
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
    content = beginEnd('document', content)
    return BREAK.join([_class, _titleFrame, titleFrame(), content])

def box(subtitle, text):
    return beginEnd('block', text, curly=[subtitle])

# Common latex macros

def document(documentClass, content):
    _documentClass = macro('documentclass', [documentClass])
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

# Math

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

    

    

            

            

        
