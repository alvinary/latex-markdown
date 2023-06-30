from md_parser import Parser
from contants import *
from collections import defaultdict

INVENTORY = lambda: defaultdict(lambda: set())

class Rule:
    def __init__(self, name, label, parts, semantics, precedence):
        self.name = name
        self.label = label
        self.parts = parts
        self.semantics = semantics
        self.precedence = precedence
        self.text = self.as_string()
        self.evaluation_symbol = ""
        self.precedence_symbol = ""

    def as_string(self):
        return f"{self.precedence} : {self.label} {RULE_ARROW} {' '.join(self.parts)} {self.parser.evaluation_symbol {self.semantics}"

    def from_line(name, line):

        marker = self.evaluation_symbol

        # Get precedence

        if marker in line:
            parts = line.split()
            precedence = [p for p in parts if p.startsWith(marker)]
            assert len(precedence) == 1

            precedence = precedence.pop()
            precedence = precedence.replace(marker, "")
            precedence = float(precedence)

        else:
            precedence = self.parser.default_precedence

        # Get syntax

        assert self.parser.evaluation_symbol in line

        syntax = line.split(self.evaluation_symbol).pop(0)
        syntax = [t for t in syntax.split() if not t.startsWith(marker) and t != RULE_ARROW]
        
        label = syntax.pop(0)
        parts = syntax

        # Get semantics


        semantics = line.split(self.evaluation_symbol).pop(1)

        return Rule(name, parser, label, parts, semantics, precedence)

class Rules:

    def __init__(self):
        self.semantics = None
        self.syntax = None
        self.precedence = None

    def parser_from_grammar(self, grammar):
        lines = self.get_lines(grammar)
        rules = [self.get_rule_from_line(l) for l in lines]
        return Parser(rules)

    def get_rule_from_line(self, line):
        # To Fix
        return
        rules = self.lines_to_rules(lines, separator, precedence)
        actions = self.lines_to_actions(lines, separator, precedence)
        sem = semantics(rules, actions)
        syn = grammarFromRules(rules)
        

    def get_lines(self, text):
        # The first line should be '<separator> <precedence>'
        # This simply takes the first line, splits it at whitespace,
        # and returns whatever it finds after the first token
        firstLine = [l for l in text.split('\n') if l][0]
        lines = text.split('\n')
        lines = [line for line in lines if line and self.notComment(line)]
        lines = lines[1:]

        evaluate = firstLine.split()[0].strip()
        precedence = firstLine.split()[1].strip()

        return evaluate, precedence, lines
    
    def not_comment(self, line):
        return COMMENT != line[:len(COMMENT)]

    def lines_to_precedence(self, lines, separator, precedence):
        order = defaultdict(lambda: UNORDERED)
        for index, line in enumerate(lines):
            if precedence in line:
                orderValues = [t for t in line.split() if t.startswith(precedence)]
                orderValue = float(orderValues[0].replace(precedence, ""))
                order[str(index)] = orderValue
                # In case a rule is n-ary and the actual rule used during parsing is n[0]
                order[str(index) + '[0]'] = orderValue
        return order
    
    def lines_to_rules(self, lines, separator, precedence):
        # The first line should be separator <separator>
        rules = []
        lines = [
            self.remove_precedence(l, precedence).split(separator)[0].strip()
            for l in lines
        ]
        lines = [l + f' ({i})' for i, l in enumerate(lines)]
        for line in lines:
            newRules = self.lineToRules(line)
            rules += newRules

        rules += whitespaceRules

        return rules

    whitespaceRules = tokensToRules(['TAB', TAB], 'tab') + tokensToRules(
    ['NEWLINE', NEWLINE], 'newline') + tokensToRules(['SPACE', SPACE], 'space')
    
    def remove_precedence(self, line, precedence):
        if precedence not in line:
            return line
        return " ".join([t for t in line.split() if not t.startswith(precedence)])

    def line_to_rules(self, line):
        tokens, name = self.line_to_parts(line)
        return tokensToRules(tokens, name)
    
    def line_to_parts(self, line):
        assert "->" in line and ')' in line and '(' in line  # to be sure

        rparenIndex = -1  # Index of the last )
        lparenIndex = line.rfind("(")
        line = line[:rparenIndex]  # String up to the last (

        tokens = [t.strip() for t in line[:lparenIndex].split()]
        tokens = tokens[0:1] + tokens[2:]  # Ignore '->'

        name = line[lparenIndex + 1:]
        # Handle punctuation here

        return tokens, name

    def lines_to_actions(self, lines, separator, precedence):
        actions = {}
        lines = [l.split(separator)[1].strip() for l in lines]
        for index, line in enumerate(lines):
            actions[str(index)] = eval('lambda ' + line)

        actions['NEWLINE'] = lambda x: NEWLINE
        actions['SPACE'] = lambda x: SPACE
        actions['TAB'] = lambda x: TAB

        return actions

    def grammar_from_rules(rules):
        grammar = defaultdict(lambda: [])
        for rule in rules:
            rhs, lhs = rule
            if isUnary(rhs):
                rhs, _ = checkSilent(rhs)
                grammar[rhs].append(lhs)
            if isBinary(rhs):
                left, right = rhs
                left, _ = checkSilent(left)
                right, _ = checkSilent(right)
                rhs = left, right
                grammar[rhs].append(lhs)
        return grammar
