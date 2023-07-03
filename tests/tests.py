import logging
from md_latex import toBeamer, toMath
from md_rules import Rules
from md_parse import Parse
from examples import *

class Tests:
    def test_beamer(self):
        logging.info("Testing toBeamer")
        toBeamer().get_latex()

    def test_math(self):
        logging.info("Testing toMath")
        toMath().get_latex()

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
        
        rules = Rules()
        result_lines = []
        for line in test_grammar:
            result_lines += rules.binarize_line(line)
        rules.build(result_lines)

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
        parser = Rules()
        result_lines = []
        for line in test_grammar:
            result_lines += parser.binarize_line(line)
        parser.build(result_lines)
        tokens = "- ( - ( 1 + 3 ) * 5 + 17 )".split()
        tags = "minus lparen minus lparen digits plus digits rparen times digits plus digits rparen".split()
        tagged_tokens = list(zip(tokens, tags))
        parse = Parse(tagged_tokens, parser)
        parse.execute()
        parse.show()
        whole_span = ('number', 0, 12, 'negative')
        parse.set_value(whole_span)
        value = parse.values[whole_span]
        print(value)
        assert value == 3

if __name__ == "__main__":
    # Tests.test_beamer()
    # Tests.test_math()
    tests = TestRules()
    tests.test_binarize()
    tests.test_build()
    test_parse = TestParse()
    test_parse.test_parse()
