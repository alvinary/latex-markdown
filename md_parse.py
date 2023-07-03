from contants import *

class Parse:

    def __init__(self, tokens, parser):
        self.parser = parser
        self.tokens = tokens
        self.unvisited = set()
        self.end_at = INVENTORY()
        self.begin_at = INVENTORY()
        self.spans = INVENTORY()
        self.readable = set()
        self.values = {}
        self.parts = {}

    def execute(self):

        for index, tagged_token in enumerate(self.tokens):
            token, token_label = tagged_token
            span_data = token_label, index, index, TAGGED
            self.values[span_data] = token
            self.add_span(*span_data)
            self.unvisited.add(span_data)

        while self.unvisited:
            current = self.unvisited.pop()
            _, begin, end, _ = current
            self.trigger(current)

            left_candidates = set(self.end_at[begin - 1])
            for other in left_candidates:
                self.trigger_pair(other, current)

            right_candidates = set(self.begin_at[end + 1])
            for other in right_candidates:
                self.trigger_pair(current, other)

        self.prune()

        return self
        
    def evaluate(self):
        values = []
        for begin, end in self.spans:
            if begin == 0 and end == len(self.tokens) + 1:
                finish = int(end)
        spans = self.spans[0, finish]
        for s in spans:
            self.set_value[s]
            new_value = self.values[s]
        values.append(new_value)
    
    def set_value(self, span):
        if span in self.values:
            return self.values[span]
        _, _, _, name = span
        parts = self.parts[span]
        for s in parts:
            self.set_value(s)
        argument_values = [self.values[s] for s in parts]
        semantics = self.parser.actions_map[name]
        self.values[span] = semantics(*argument_values)

    def trigger(self, branch):
        branch_label, begin, end, _ = branch
        same_as = self.parser.same_as[branch_label]
        for grammar_rule in same_as:
            name, label, _, _, _ = grammar_rule
            head = (label, begin, end, name)
            self.add_span(label, begin, end, name)
            self.spans[begin, end].add((head, branch))
            self.parts[head] = [branch]

    def trigger_pair(self, left_part, right_part):
        left_label, begin, _, _ = left_part
        right_label, _, end, _ = right_part
        begin_with = self.parser.begin_with[left_label]
        end_with = self.parser.end_with[right_label]
        for grammar_rule in begin_with & end_with:
            name, label, _, _, _ = grammar_rule
            new_span = (label, begin, end, name)
            self.add_span(label, begin, end, name)
            self.spans[begin, end].add((new_span, left_part, right_part))
            self.parts[new_span] = [left_part, right_part]

    def add_span(self, label, begin, end, name):
        span_data = (label, begin, end, name)
        self.end_at[end].add(span_data)
        self.begin_at[begin].add(span_data)
        self.unvisited.add(span_data)
        # These are used in self.show()
        span_content = tuple([token for token, tag in self.tokens[begin:end + 1]])
        self.readable.add((begin, end, label, span_content))

    def compare(self, left, right):
        left_label, i, j, left_name = left
        right_label, k, l, right_name = right
        
        if i == j or k == l:
            return False
        
        left_precedence = self.parser.precedence_map[left_name]
        right_precedence = self.parser.precedence_map[right_name]
        spans_overlap = left_label == right_label and i == k and j == l

        if spans_overlap and left_precedence < right_precedence:
            return left
        elif spans_overlap and right_precedence < left_precedence:
            return right
        else:
            return False

    def prune(self):

        remove = set()
        nodes = set()

        for indices in self.spans:
            for span in self.spans[indices]:
                nodes |= set(span)

        nodes = list(nodes)

        for n, m in self.pairs(nodes):
            comparison = self.compare(n, m)
            if comparison:
                remove.add(comparison)

        for indices in self.spans:
            spanItems = list(self.spans[indices])
            self.spans[indices] = [i for i in spanItems if not set(i) & remove]

    def pairs(self, sequence):
        for i in range(len(sequence)):
            for j in range(i):
                yield (sequence[i], sequence[j])
            
    def show(self):
        for span in sorted(self.readable):
            begin, end, label, tokens = span
            begin = str(begin)
            end = str(end)
            print(f"{label} : {' '.join(tokens) } [{begin} : {end}]\n")

