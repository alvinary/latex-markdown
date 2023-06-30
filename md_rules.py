from md_parser import Parser
from contants import *
from collections import defaultdict
from dsls import BeamerDSL

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
        return f"{self.precedence} : {self.label} {RULE_ARROW} {' '.join(self.parts)} {self.parser.evaluation_symbol} {self.semantics}"

    def from_line(self, line):

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

        self.rules_map = {}
        self.begins_with = INVENTORY()
        self.ends_with = INVENTORY()
        self.same_as = INVENTORY()

    def build(self, grammar):
        
        for index, line in enumerate(grammar):
            self.rules_map[index] = line

        for line in grammar:

            label, parts, semantics, precedence = line

            is_unary = len(parts) == 1
            is_binary = len(parts) == 2

            if is_binary:
                left, right = parts
                self.begins_with[left].add(line)
                self.ends_with[right].add(line)

            if is_unary:
                single_part = parts[0]
                self.same_as[single_part].add(line)


    '''
    The first line should be '<separator> <precedence>'
    This simply takes the first line, splits it at whitespace,
    and returns whatever it finds after the first token
    '''
    def grammar_from_rules(self, rules):
        grammar = defaultdict(lambda: [])
        for rule in rules:
            rhs, lhs = rule
            if self.isUnary(rhs):
                rhs, _ = self.checkSilent(rhs)
                grammar[rhs].append(lhs)
            if self.isBinary(rhs):
                left, right = rhs
                left, _ = self.checkSilent(left)
                right, _ = self.checkSilent(right)
                rhs = left, right
                grammar[rhs].append(lhs)
        return grammar

    def binaryRule(self, head, left, right, name):
        return [((left, right), (head, name))]


    def unaryRule(self, head, branch, name):
        return [(branch, (head, name))]

    def naryRule(self, tokens, name):

        rules = []

        head = tokens.pop(0)
        left = tokens.pop(0)
        size = len(tokens)

        while tokens:

            auxiliaryRight = f"{name}[{size - len(tokens)}]"

            if len(tokens) == 1:

                right = tokens.pop(0)
                newRules = self.binaryRule(head, left, right, auxiliaryRight)
                rules += newRules

            else:
                newRules = self.binaryRule(head, left, auxiliaryRight, auxiliaryRight)
                rules += newRules
                head = auxiliaryRight
                left = tokens.pop(0)

        return rules
    
    def checkSilent(self, token):
        if token[0] == "[" and token[-1] == "]":
            return token[1:-1], True
        else:
            return token, False

    def isUnary(self, rhs):
        return not isinstance(rhs, tuple)


    def isBinary(self, rhs):
        return isinstance(rhs, tuple) and len(rhs) == 2
