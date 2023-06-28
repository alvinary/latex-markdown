import logging
from md_latex import toBeamer, toMath
from examples import *

class Tests:

    def test_beamer(self):
        logging.info("Testing toBeamer")
        toBeamer().get_latex()

    def test_math(self):
        logging.info("Testing toMath")
        toMath().get_latex()


if __name__ == "__main__":
    Tests.test_beamer()
    Tests.test_math()


mathTests = ['( a b over b a ) equals 1',
    'all x : x not in ø',
    'sum from a to n of f(x)',
    'sum over { x : g(x) in S } of h(x, g(x))',
]
    
print(toBeamer(basicExample))

for t in mathTests[1:]:
    print(toMath(t))