example = '''

# BEAMER MARKDOWN

Write Beamer Slides With A Clean DSL

____________________________________

## What Is Beamer Markdown?

* Markdown is a plain text format that makes it
  easy to write human-readable rich text

* Markdown is a (WYASJHASJH) format, and not a (WSIWG)
  format

_____________________________________

* Markdown documents can be written easily on any
  editor, and are not visually messy, which has
  many advantages:
  
  * It's hard to miss spelling mistakes and text reads closer
    to the 'printed' / compiled version, which makes it
    easy to think of corrections

  * The number of lines in a markdown document bears  a direct
    relationship to the space taken by a certain part of a
    given text -- it's easier to know when something is too
    long when length can be determined visually or by comparing
    a couple of integers

  * The number of lines in a markdown document bear a direct
    relationship to the space taken by a certain part of a
    given text -- it's easier to get the right idea of size
    at a glance

____________________________________

Since everyone has so much to do, and their energy is better
spent doing something more useful than scratching their heads
before `pdflatex` error messages

==============================================

Why Not Just Have A Nice Markdown For Beamer?

==============================================

________________________________________

Now, latex has lots of features

Easily extensible

== Remark ====================================
You can always do stuff wrong
==============================================

_________________________________________
'''

test_grammar = [
            ('integer', 'number', ('digits',), 10, lambda x : int(x)),
            ('grouping', 'number', ('lparen', 'number', 'rparen'), 25, lambda _, x, __ : x),
            ('product', 'number', ('number', 'times', 'number'), 15, lambda x, _, z: x * z),
            ('sum', 'number', ('number', 'plus', 'number'), 10, lambda x, _, z: x + z),
            ('negative', 'number', ('minus', 'number'), 20, lambda _, y : -y),
            ('substraction', 'number', ('number', 'minus', 'number'), 10, lambda x, _, z : x - z),
            ('five aguments', 'foo', ('bar', 'barfoo', 'foobar', 'barbar', 'foofoo'), 10, lambda x, y, z, w, u : [x, y, z, w, u])
        ]

latex_examples = [
        '''
        # Why sections are better suited for a single numeral

        There are many sections, and a single title. So titles can have a less
        typable syntax without interferring too much.

        ## How about subsections?

        Subsections are written with double hashes/ double numerals.

        ## Some other subsection

        This is some other subsection.
        '''
]

math_tests = ['( a b over b a ) equals 1',
    'all x : x not in ø',
    'sum from a to n of f(x)',
    'sum over { x : g(x) in S } of h(x, g(x))',
]

math_examples = [
    ('a = b', 'a = b'),
    ('a != b', 'a \\\\neq b'),
    ('a in A', 'a \\in A'),
    ('for all x : exists y : x in A => r(x, y)', '\\forall x : \\exists y : x \\in A \\Rightarrow r ( x, y )'),
    ('sum from i = 1 to n of i', '\\sum_{i = 1}^{n} i'),
    ('sum over t in T of f (t)', '\\sum_{t \\in T} f ( t )'),
    ('sum over i in A of f sub i (x)', '\\sum_{i \\in A} f_{i} ( x )'),
    ('sum over i in A of f sub i (x sub i sup 2)', '\\sum_{i \\in A} f_{i} ( x_{i}^{2} )'),
    ('sum over i in A of f sup i (x sup i sub 2)', '\\sum_{i \\in A} f^{i} ( x^{i}_{2} )'),
    ('a [: not in :] A', 'a \\\\notin A'),
    ('a not in A', 'a \\\\notin A'),
    ('for all x in R . exists y in R . xy = 1', '\\forall x \\in \\R. \\exists y \\in \\R . xy = 1'), 
    # ('f : a -> b', ),
    # ('A included in B'),
    # ('A subset of B'),
    # ('A includes B')

]
