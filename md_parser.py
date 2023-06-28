from md_parse import Parse
from contants import TOKEN
from collections import defaultdict

justToken = lambda x: TOKEN

class Parser:

    def __init__(self, grammar, actions, order, tag=justToken):
        self.grammar = grammar
        self.actions = actions
        self.precedence = order
        self.tag = tag
        self.values = {}

    def get_parse(self, tokens):
        return Parse(tokens, self).execute()

    def setValue(self, span):

        if span[0] in self.values:  # Value is already stored
            return

        isLeaf = len(span) == 1
        isUnary = len(span) == 2
        isBinary = len(span) == 3

        if isLeaf:
            leaf = span[0]
            check = True  # Because leaves already have a value

        if isUnary:
            head, branch = span
            check = branch in self.values

        if isBinary:
            head, left, right = span
            checkLeft = left in self.values
            checkRight = right in self.values
            check = checkLeft and checkRight

        if check and isLeaf:
            self.values[leaf] = leaf[3]  # The token

        if check and isUnary:
            _, action, arg = self.actions[head[3]]  # Magic number 3
            argument = self.values[branch]
            arg = list(reversed(arg(argument).collect()))
            self.values[head] = action(*arg)

        if check and isBinary:
            _, action, args = self.actions[
                head[3]]  # These should all be objects, not tuples
            left = self.values[left]
            right = self.values[right]
            args = args(left, right)
            args = list(reversed(args.collect()))
            self.values[head] = action(*args)

    def value(self, tokens):

        self.values = {}

        parse = self.get_parse(tokens)

        distances = set()

        leaves = defaultdict(lambda: [])
        binary = defaultdict(lambda: [])
        unary = defaultdict(lambda: [])

        for span in parse.spans.keys():
            distance = span[1] - span[0]
            data = parse.spans[span]
            for d in data:
                if len(d) == 1:
                    leaves[distance].append(d)
                if len(d) == 2:
                    unary[distance].append(d)
                if len(d) == 3:
                    binary[distance].append(d)
            distances.add(distance)

        for span in leaves[0]:
            self.setValue(span)

        for k in sorted(distances):

            for s in binary[k]:
                for t in binary[k]:
                    self.setValue(t)

            for s in unary[k]:
                for t in unary[k]:
                    self.setValue(t)

        begin = 0
        end = max(distances)

        fullSpans = [
            span for span in self.values if span[1] == begin and span[2] == end
        ]

        results = [self.values[k] for k in fullSpans]

        return results
