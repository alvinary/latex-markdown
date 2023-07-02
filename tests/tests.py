import logging
from md_latex import toBeamer, toMath
from md_rules import Rules
from examples import *

class Tests:

    def test_beamer(self):
        logging.info("Testing toBeamer")
        toBeamer().get_latex()

    def test_math(self):
        logging.info("Testing toMath")
        toMath().get_latex()

    def test_binarize(self):
        logging.info("Testing Rules.binarize_line()")
        rules = Rules()
        result_lines = []
        for line in sample_lines:
            result_lines += rules.binarize_line(line)
        result_lines = set([(n, h, tuple(p), o) for (n, h, p, o, _) in result_lines])
        print(result_lines)
        assert ('sum', 'number', ('number', 'sum[1]'), 10) in result_lines
        assert ('sum[1]', 'sum[1]', ('plus', 'number'), 10) in result_lines
        assert ('product[1]', 'product[1]', ('times', 'number'), 10) in result_lines


if __name__ == "__main__":
    # Tests.test_beamer()
    # Tests.test_math()
    tests = Tests()
    tests.test_binarize()
