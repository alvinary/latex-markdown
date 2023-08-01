import logging
from constants import *
from dsls import *
from collections import defaultdict
from rules import Rules

class LatexMarkdown:

    def __init__(self, dsl, tokens, default, prepreocessor):
        self.parser = Rules(dsl)
        self.special_tokens = tokens
        self.default_token = default
        self.preprocessor = preprocessor
    
    def tag(self, token):
        if token in self.special_tokens:
            return token
        else:
            return self.default_token

    def get_latex(self, markdown):
        tagged_tokens = self.preprocess(text)
        parse = self.parser.get_parse(tagged_tokens)
        values = list(parse.evaluate())
        return values

    def preprocess(self, text):
        text = self.preprocessor(text)
        tokens = text.split()
        tags = [self.tag(t) for t in tokens]
        tagged_tokens = list(zip(tokens, tags))
        return tagged_tokens

class Latex(LatexMarkdown):

    def __init__(self):
        self.parser = Rules(latex_dsl)
        self.special_tokens = latex_tokens
        self.default_token = "text"
    
    def tag(self, token):
        if token in self.special_tokens:
            return token
        else:
            return self.default_token

    def get_latex(self, markdown):
        tagged_tokens = self.preprocess(text)
        parse = self.parser.get_parse(tagged_tokens)
        values = list(parse.evaluate())
        return values

    def preprocess(self, text):
        text = text.replace(NEWLINE, EXPLICIT_NEWLINE)
        double_newline = EXPLICIT_NEWLINE * 2
        double_break = EXPLICIT_BREAK * 2
        text = text.replace(double_newline, EXPLICIT_BREAK)
        while double_break in text:
            text = text.replace(double_break, EXPLICIT_BREAK)
        text = text.replace(EXPLICIT_BREAK + EXPLICIT_NEWLINE, EXPLICIT_BREAK)
        text = text.replace(EXPLICIT_NEWLINE + EXPLICIT_BREAK, EXPLICIT_BREAK)
        while "  " in text:
            text = text.replace("  ", " ")
        pretokens = text.split()
        tokens = []
        text = []
        for token in pretokens:
            if token in self.special_tokens and not text:
                tokens.append(token)
            elif token in self.special_tokens and text:
                tokens.append(" ".join(text))
                tokens.append(token)
                text = text
            else:
                text.append(token)
        tags = [self.tag(t) for t in tokens]
        tagged_tokens = list(zip(tokens, tags))
        return tagged_tokens

class Beamer(LatexMarkdown):

    def get_latex(self, markdown = "2 + 5"):
        grammar = Rules().parser_from_grammar(BeamerDSL)
        tokens = self.preprocess(markdown)
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


class Math(LatexMarkdown):

    def __init__(self):
        self.delimiters = list(delimiters)
        self.special_tokens = list(math_tokens)
        self.parser = Rules(math_dsl)

    def tag(self, token):
        if token in self.special_tokens:
            return token
        else:
            return 'name'

    def get_latex(self, markdown):
        parse = self.parser.get_parse(self.preprocess(markdown))
        values = parse.evaluate()
        return list(values)

    def preprocess(self, text):
    
        # Hide tokens with delimiters
        
        for k in with_delimiters:
            text = text.replace(k, with_delimiters[k])         
        
        # Put whitespace around delimiters
        
        for d in self.delimiters:
            text = text.replace(d, f' {d} ')
            
        # Recover tokens
        
        for k in without_delimiters:
            text = text.replace(k, without_delimiters[k])
        
        # Remove double spaces
            
        while '  ' in text:
            text = text.replace('  ', ' ')
            
        # Split at whitespace

        tokens = text.split()
        tags = [self.tag(t) for t in tokens]

        return list(zip(tokens, tags))
