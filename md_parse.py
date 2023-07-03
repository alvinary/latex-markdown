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

    def execute(self):

        for index, tagged_token in enumerate(self.tokens):
            token, token_label = tagged_token
            span_data = token_label, index, index, TAGGED
            self.values[span_data] = token
            self.add_span(span_data)

        while self.unvisited:
            current = self.unvisited.pop()
            _, begin, end, _ = current
            self.trigger(current)

            left_candidates = set(self.end_at[begin - 1])
            for other in left_candidates:
                self.triggerPair(other, current)

            right_candidates = set(self.begin_at[end + 1])
            for other in right_candidates:
                self.triggerPair(current, other)

        self.prune()

        return self
    
    def evaluate(self):
        pass
        
    def set_value(self, spans):
 
        if spans[0] in self.values:  # Value is already stored
            return

        is_leaf = len(spans) == 1
        is_unary = len(spans) == 2
        is_binary = len(spans) == 3
        
        # Check if all dependencies already have a value

        if is_leaf:
            leaf = spans[0]
            check = True  # Because leaves already have a value

        if is_unary:
            span, branch = spans
            check = branch in self.values

        if is_binary:
            span, left_part, right_part = spans
            check_left = left in self.values
            check_right = right in self.values
            check = check_left and check_right
            
        # This method does nothing if 'check' is False,
        # because that means the values for the 'part'
        # spans on which the current span depends have
        # not yet been evaluated
        
        # In Parser.evaluate(), spans are evaluated bottom-up,
        # and since unary rules might yield new spans that
        # can be used by further rules, every tree level
        # is checked []

        if check and is_leaf:
            pass  # Leaves are assigned a value in the first lines of 'execute()'

        if check and is_unary:
            name, begin, end, precedence, semantics = span  # Magic number 3
            argument = self.values[branch]
            self.values[span] = semantics(argument)

        # WRAPPEND = lambda x, y : [x] + y
        # WRAP = lambda x, y : [x, y]
        if check and is_binary:
            name, begin, end, precedence, semantics = span
            left_value = self.values[left_part]
            right_value = self.values[right_part]
            right_is_auxiliary = is_auxiliary(right_part) # TODO: define is_auxiliary
            if right_is_auxiliary:
                arguments = [left_value]
                arguments += right_value                  # TODO: have this make sense for auxiliary rules
            else:
                arguments = [left_value, right_value]
            self.values[head] = action(*arguments) # just return

    def trigger(self, branch):
        branch_label, begin, end, _ = branch
        same_as = self.parser.grammar.same_as[branch_label]
        for grammar_rule in same_as:
            name, label, _, _, _ = grammar_rule
            head = (label, begin, end, name)
            self.add_span(label, begin, end, name)
            self.spans[begin, end].add((head, branch))

    def triggerPair(self, left_part, right_part):
        left_label, begin, _, _ = left_part
        right_label, _, end, _ = right_part
        begin_with = self.parser.begin_with[left_label]
        end_with = self.parser.end_with[right_label]
        for grammar_rule in begin_with & end_with:
            name, label, _, _, _ = grammar_rule
            new_span = (label, begin, end, name)
            self.add_span(label, begin, end, name)
            self.spans[begin, end].add((new_span, left_part, right_part))

    def add_span(self, label, begin, end, name):
        spanData = (label, begin, end, name)
        self.end_at[end].add(spanData)
        self.begin_at[begin].add(spanData)
        self.unvisited.add(spanData)
        # These are used in self.show()
        spanContent = tuple(self.tokens[begin:end + 1])
        self.readable.add((begin, end, label, spanContent))

    def compare(self, left, right):
        left_label, i, j, left_name = left
        right_label, k, l, right_name = right
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
            print(f"[{begin} : {end}] {label} : {' '.join(tokens) }")

