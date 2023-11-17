from parse import Parse
from constants import *

class Rules:

    def __init__(self, rules=list()):
        self.rules_map = {}
        self.begin_with = INVENTORY()
        self.end_with = INVENTORY()
        self.same_as = INVENTORY()
        self.precedence_map = {}
        self.actions_map = {}
        binary_rules = []
        for line in rules:
            binary_rules += self.binarize_line(line)
        self.build(binary_rules)

    def build(self, grammar):
        
        for line in grammar:
            name, _, parts, precedence, semantics = line
            self.rules_map[name] = line
            self.precedence_map[name] = precedence
            self.actions_map[name] = semantics

            is_unary = len(parts) == 1
            is_binary = len(parts) == 2

            if is_binary:
                left, right = parts
                self.begin_with[left].add(line)
                self.end_with[right].add(line)

            if is_unary:
                single_part = parts[0]
                self.same_as[single_part].add(line)

    def get_parse(self, tagged_tokens):
        new_parse = Parse(tagged_tokens, self)
        new_parse.execute()
        return new_parse

    def binarize_line(self, grammar_line):

        binary_lines = []
        name, label, parts, precedence, semantics = grammar_line
        remaining_parts = list(parts)
        size = int(len(remaining_parts))

        if len(parts) <= 2: # The input grammar line is already binary
            binary_lines.append(grammar_line)

        else:
            current_label = label
            current_name = name
            current_semantics = lambda x, y : semantics(*WRAPPEND(x, y))
            current_semantics = get_try(current_semantics, current_label)
            current_precedence = precedence

            while remaining_parts:

                if len(remaining_parts) > 2:

                    left_part = remaining_parts.pop(0)
                    right_part = f"{name}[{size - len(remaining_parts)}]"

                    new_line = (current_name, current_label, (left_part, right_part), current_precedence, current_semantics)
                    binary_lines.append(new_line)

                    current_name = str(right_part)
                    current_label = str(right_part)
                    current_precedence = DEFAULT_PRECEDENCE                    
                    current_semantics = get_try(WRAPPEND, current_name)

                if len(remaining_parts) == 2:
                    current_semantics = get_try(WRAP, current_name)
                    left_part = remaining_parts.pop(0)
                    right_part = remaining_parts.pop(0)
                    new_line = (current_name, current_label, (left_part, right_part), current_precedence, current_semantics)
                    binary_lines.append(new_line)

        return binary_lines
