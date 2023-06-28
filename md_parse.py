
from collections import defaultdict

INVENTORY = lambda: defaultdict(lambda: set())

class Parse:

    def __init__(self, tokens, parser):
        self.parser = parser
        self.tokens = tokens
        self.unvisited = set()
        self.endAt = INVENTORY()
        self.beginAt = INVENTORY()
        self.spans = INVENTORY()
        self.readable = set()

    def execute(self):

        for index, token in enumerate(self.tokens):
            tokenLabel = self.parser.tag(token)
            self.addToken(index, token, tokenLabel)
            self.spans[index, index].add(
                ((tokenLabel, index, index, token), ))

        while self.unvisited:
            current = self.unvisited.pop()
            label, begin, end, action = current
            self.trigger(current)

            left = set(self.endAt[begin - 1])
            for other in left:
                self.triggerPair(other, current)

            right = set(self.beginAt[end + 1])
            for other in right:
                self.triggerPair(current, other)

        self.prune()

        return self

    def trigger(self, branch):
        branchLabel, begin, end, _ = branch
        if branchLabel in self.parser.grammar.keys():
            for pair in self.parser.grammar[branchLabel]:
                label, action = pair
                head = (label, begin, end, action)
                self.addSpan(label, begin, end, action)
                self.spans[begin, end].add((head, branch))

    def triggerPair(self, left, right):
        lLabel = left[0]
        rLabel = right[0]
        begin = left[1]
        end = right[2]
        if (lLabel, rLabel) in self.parser.grammar.keys():
            for pair in self.parser.grammar[(lLabel, rLabel)]:
                label, action = pair
                head = label, begin, end, action
                self.addSpan(*head)
                self.spans[begin, end].add((head, left, right))

    def addSpan(self, label, begin, end, action):
        spanData = (label, begin, end, action)
        self.endAt[end].add(spanData)
        self.beginAt[begin].add(spanData)
        self.unvisited.add(spanData)
        spanContent = tuple(self.tokens[begin:end + 1])
        self.readable.add((label, spanContent))

    def addToken(self, index, token, tokenLabel):
        self.addSpan(tokenLabel, index, index, token)

    def compare(self, left, right):
        leftLabel, i, j, leftName = left
        rightLabel, k, l, rightName = right
        leftPrecedence = self.parser.precedence[leftName]
        rightPrecedence = self.parser.precedence[rightName]

        if leftLabel == rightLabel and i == k and j == l and leftPrecedence != rightPrecedence:
            if leftPrecedence < rightPrecedence:
                return left
            if rightPrecedence < leftPrecedence:
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
            
    def showSpans(self):
        for span in self.readable:
            print(span)
