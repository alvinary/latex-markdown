from constants import *
import bisect

# TODO: use named tuples for spans

class Parse:

    def __init__(self, tokens, parser):
        self.parser = parser
        self.tokens = tokens
        self.unvisited = []
        self.end_at = INVENTORY()
        self.begin_at = INVENTORY()
        self.spans = INVENTORY()
        self.readable = set()
        self.values = {}
        self.parts = {}
        self.uncovered_spans = []
        self.considered = set()

    def execute(self):

        for index, tagged_token in enumerate(self.tokens):
            token, token_label = tagged_token
            span_data = token_label, index, index, TAGGED
            self.values[span_data] = token
            self.add_span(*span_data)
            bisect.insort(self.unvisited, span_data)

        while self.unvisited:
            current = self.unvisited.pop()
            _, begin, end, _ = current
            
            # Check unary rule parses
            self.trigger(current)

            # Check for left matches
            left_candidates = set(self.end_at[begin - 1])
            for other in left_candidates:
                self.trigger_pair(other, current)

            # Check for right matches
            right_candidates = set(self.begin_at[end + 1])
            for other in right_candidates:
                self.trigger_pair(current, other)

        # self.prune()

        return self
        
    def evaluate(self):
        values = []
        begin = 0
        finish = len(self.tokens) - 1
        complete_spans = self.spans[begin, finish]
        for s in complete_spans:
            head_span = s[0]
            self.set_value(head_span)
            new_value = self.values[head_span]
            values.append(new_value)
        return values
    
    def set_value(self, span):
        if span in self.values:
            return self.values[span]
        _, _, _, name = span
        parts = self.parts[span]
        for s in parts:
            _, i, j, _ = s
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
        if span_data not in self.considered:
            self.considered.add(span_data)
            bisect.insort(self.unvisited, span_data)
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

    def get_dependencies(self, span):
        queue = [span]
        in_dependencies = set()
        dependencies = []
        visited = set()
        while queue:
            current = queue.pop(0)
            if current in self.parts:
                parts = set(self.parts[current])
                unvisited_parts = parts - visited
                in_dependencies |= parts
                new_parts = parts - in_dependencies
                for new in new_parts:
                    bisect.insort(dependencies, new)
                queue += [p for p in unvisited_parts]
                visited |= parts
        return list(dependencies)

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

    def unfold_parse(self, span):
        head_span = [span]
        parts = self.parts[span]
        is_unary = len(parts) == 1
        is_binary = len(parts) == 2
        if is_binary:
            left = parts[0]
            right = parts[1]
            left_spans = self.unfold_parse(left)
            right_spans = self.unfold_parse(right)
            return head_span + left_spans + right_spans
        if is_unary:
            branch = parts[0]
            branch_spans = self.unfold_parse(branch)
            return head_span + branch_spans

    def n_initial_segments(self, n=5, cutoff=100):
        initial_segments = [span for span in self.begin_at[1]]
        segment_length = lambda span: span[2] - span[1]
        initial_segments.sort(key=segment_length)
        initial_segments = list(reversed(initial_segments))
        return initial_segments[:n]

    def report(self, n=1, cutoff=200):
        reports = []
        for _, begin, end, _ in self.n_initial_segments():
            tokens = [t[0] for t in self.tokens[:end]]
            tip = min(len(self.tokens), end + 30)
            next_tokens = [t[0] + f' ({t[1]}) ' for t in self.tokens[end:tip]]
            tokens_text = " ".join(tokens)
            if len(tokens_text) > cutoff:
                tokens_text = tokens_text[-cutoff:]
            next_text = " ".join(next_tokens)
            reports.append(tokens_text + " << SEGMENT END << " + next_text)
        return reports

