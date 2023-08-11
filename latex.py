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
        tagged_tokens = self.preprocess(markdown)
        parse = self.parser.get_parse(tagged_tokens)
        values = list(parse.evaluate())
        return values

    def preprocess(self, text):
        text = self.preprocessor(text)
        tokens = text.split()
        tags = [self.tag(t) for t in tokens]
        tagged_tokens = list(zip(tokens, tags))
        return tagged_tokens
        
    def postprocess(self, text):
        while '  ' in text:
            text = text.replace('  ', ' ')
        for s in RIGHT:
            text = text.replace(" {s}" ,"{s}")
        for s in LEFT:
            text = text.replace("{s} " ,"{s}")
        return text
        

class Latex(LatexMarkdown):

    def __init__(self):
        self.parser = Rules(latex_dsl + math_dsl)
        self.special_tokens = latex_tokens
        self.default_token = "text"
        self.math_parser = Math()
        self.parse = False
    
    def tag(self, token):
        if token in self.special_tokens:
            return token
        else:
            return self.default_token

    def get_latex(self, markdown):
        tagged_tokens = self.preprocess(markdown)
        self.parse = self.parser.get_parse(tagged_tokens)
        values = list(self.parse.evaluate())
        values = [self.postprocess(v) for v in values]
        return values

    def preprocess(self, text):
        text = f"{BEGIN_DOCUMENT} {text.strip()}\n\n{END_DOCUMENT}"
        text = text.replace(NEWLINE, f" {EXPLICIT_NEWLINE} ")
        text = text.replace(BEGIN_MATH, f" {BEGIN_MATH} ")
        while '  ' in text:
            text = text.replace('  ', ' ')
        pretokens = [t.strip() for t in text.split()]
        tokens = []
        text_tokens = []
        newline_tokens = []
        formula_tokens = []
        math_mode = False
        tagged_tokens = []
        for token in pretokens:
            
            is_newline = token == EXPLICIT_NEWLINE
            is_special = token  in self.special_tokens
            text_empty = not text_tokens
            is_break = len(newline_tokens) > 1
            one_newline = len(newline_tokens) == 1
            
            if not is_newline and is_break:
                tokens.append(EXPLICIT_BREAK)
                newline_tokens = []
            elif not is_newline and one_newline:
                tokens.append(EXPLICIT_NEWLINE)
                newline_tokens = []
            
            # Begin math
            if token == BEGIN_MATH and not formula_tokens:
                math_mode = not math_mode
                tokens.append(" ".join(text_tokens))
                tokens.append(BEGIN_MATH)
                text_tokens = []
            # Adding math
            elif math_mode and not is_newline and token != END_MATH:
                formula_tokens.append(token)
            # Finish math
            elif token == END_MATH and formula_tokens:
                math_mode = not math_mode
                math_text = " ".join(formula_tokens)
                tagged_formula_tokens = self.math_parser.preprocess(math_text)
                tokens += tagged_formula_tokens
                tokens.append(BEGIN_MATH)
                formula_tokens = []
            # Special token, having no text tokens stored
            elif is_special and not is_newline and text_empty:
                tokens.append(token)
            # Special token, having text tokens stored
            elif is_special and not is_newline and text_tokens:
                tokens.append(" ".join(text_tokens))
                tokens.append(token)
                text_tokens = []
            elif is_newline and text_tokens:
                tokens.append(" ".join(text_tokens))
                newline_tokens.append(token)
                text_tokens = []
            elif is_newline and text_empty:
                newline_tokens.append(token)                
            else:   
                text_tokens.append(token)
                
        if text_tokens:
            tokens.append(" ".join(text_tokens))
            
        if tokens[-1] != END_DOCUMENT:
            tokens.append(END_DOCUMENT)
            
        tokens = [t for t in tokens if t]
        # Alternate between latex and math tags using the
        # same delimiter-based criterion
        tagged_tokens = []
        for token in tokens:
            if isinstance(token, tuple):
                tagged_tokens.append(token)
            else:
                tagged_tokens.append((token, self.tag(token)))
        # print('TAGGED TOKENS:', '\n'.join([str(s) for s in tagged_tokens]))
        return tagged_tokens
        
    def postprocess(self, text):
        while '  ' in text:
            text = text.replace('  ', ' ')
        for s in RIGHT:
            text = text.replace(" {s}" ,"{s}")
        for s in LEFT:
            text = text.replace("{s} " ,"{s}")
        return text


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
        self.special_characters = list(SPECIAL_CHARACTERS)
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
        
        for k in with_special:
            text = text.replace(k, with_special[k])         
        
        # Put whitespace around special characters
        
        for d in self.special_characters:
            text = text.replace(d, f' {d} ')
            
        # Recover tokens
        
        for k in without_special:
            text = text.replace(k, without_special[k])
        
        # Remove double spaces
            
        while '  ' in text:
            text = text.replace('  ', ' ')
            
        # Split at whitespace

        tokens = text.split()
        tokens = [t for t in tokens if t]
        tags = [self.tag(t) for t in tokens]

        return list(zip(tokens, tags))
    
    def postprocess(self, text):
        while '  ' in text:
            text = text.replace('  ', ' ')
        for s in RIGHT:
            text = text.replace(" {s}" ,"{s}")
        for s in LEFT:
            text = text.replace("{s} " ,"{s}")
        return text
