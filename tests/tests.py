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
        
        for line in result_lines:
            print(*line)


if __name__ == "__main__":
    # Tests.test_beamer()
    # Tests.test_math()
    tests = Tests()
    tests.test_binarize()
    