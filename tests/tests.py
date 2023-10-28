import logging
from latex import Beamer, Math, Latex
from rules import Rules
from parse import Parse
from constants import NEWLINE
from examples import *

class Tests:
    
    def test_beamer(self):
        logging.info("Testing Beamer class")
        toBeamer().get_latex()

    def test_latex(self):
        logging.info("Testing Latex class")
        latex_markdown = Latex()
        for example in latex_examples:
            tagged_tokens = latex_markdown.preprocess(example)
            tokens = [t for (t, s) in tagged_tokens]
            parse = latex_markdown.parser.get_parse(tagged_tokens)
            #print('Tokens:')
            #print(" :: ".join([str(t) for t in parse.tokens]))
            #print()
            results = latex_markdown.get_latex(example)
            parse.show()
            #print()
            print('\nsource:\n')
            print(example)
            print('\nresults:\n')
            for result in results:
                print(result)
                print('')
            print()

    def test_math(self):
        logging.info("Testing Math class")
        math_markdown = Math()

        for example, expected_result in math_examples:
            tagged_tokens = math_markdown.preprocess(example)
            parse = math_markdown.parser.get_parse(tagged_tokens)
            results = parse.evaluate()
            print('\nsource:\n')
            print(example)
            print('\nresults:\n')
            for result in results:
                print(result)
                print('')
            assert expected_result in results

class TestRules:

    def test_binarize(self):
        logging.info("Testing Rules.binarize_line()")
        rules = Rules()
        result_lines = []
        for line in test_grammar:
            result_lines += rules.binarize_line(line)
        result_lines = set([(n, h, tuple(p), o) for (n, h, p, o, _) in result_lines])
        assert ('sum', 'number', ('number', 'sum[1]'), 10) in result_lines
        assert ('sum[1]', 'sum[1]', ('plus', 'number'), 10) in result_lines
        assert ('product[1]', 'product[1]', ('times', 'number'), 10) in result_lines

    def test_build(self):
        logging.info("Testing Rules.build()")
        rules = Rules(test_grammar)
        begins_with = rules.begin_with['number']
        begins_with = set([n for (n, _, _, _, _) in begins_with])
        assert 'product' in begins_with
        assert 'substraction' in begins_with
        assert 'sum' in begins_with
        assert 'negative' not in begins_with
        assert 'sum[1]' not in begins_with
        begins_with = rules.begin_with['plus']
        begins_with = set([n for (n, _, _, _, _) in begins_with])
        assert 'product' not in begins_with
        assert 'substraction' not in begins_with
        assert 'sum[1]' in begins_with
        end_with = rules.end_with['number']
        end_with = set([n for (n, _, _, _, _) in end_with])
        assert 'negative' in end_with
        assert 'product' not in end_with
        assert 'substraction' not in end_with
        assert 'product[1]' in end_with
        assert 'substraction[1]' in end_with
        assert 'sum' not in end_with
        assert 'sum[1]' in end_with

class TestParse:

    def test_parse(self):
        parser = Rules(test_grammar)
        result_lines = []
        tokens = "( 3 * 3 ) + ( 2 * ( 3 + 1 ) )".split()
        tags = "lparen digits times digits rparen plus lparen digits times lparen digits plus digits rparen rparen".split()
        parse = parser.get_parse(list(zip(tokens, tags)))
        values = parse.evaluate()
        for v in values:
            print(v)
        assert 17 in values
        tokens = "- ( - ( ( 1 + 3 ) * 5 ) + 17 )".split()
        tags = "minus lparen minus lparen lparen digits plus digits rparen times digits rparen plus digits rparen".split()
        parse = parser.get_parse(list(zip(tokens, tags)))
        values = parse.evaluate()
        for v in values:
            print(v)
        assert 3 in values

if __name__ == "__main__":
    # Tests.test_beamer()
    # Tests.test_math()
    tests = TestRules()
    tests.test_binarize()
    tests.test_build()
    test_parse = TestParse()
    test_parse.test_parse()
    test_markdown = Tests()
    test_markdown.test_latex()
    test_markdown.test_math()
    
