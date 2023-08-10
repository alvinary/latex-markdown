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

math_placeholders_testcase = '''
It is easy to prove that eigenspaces are disjoint.
We say $$$$ is an eigenvector of $$$$ if

	$$$$

for some $$$$ in $$$$.

So if $$$$ and $$$$, $$$$ and $$$$ are distinct,
and $$$$, then $$$$ and $$$$ cannot be equal, and
the two vectors cannot be elements of the same
eigenspace.

Note if $$$$ then $$$$, and in that case the two
vectors belong to the same eigenspace.
'''

# Usa un testcase de verdad

math_testcase = '''
It is easy to prove that eigenspaces are disjoint.
We said ~v~ is an eigenvector of ~T~ if

~ Tx = kx ~ 

for some ~k~ in ~K~.

So if ~Tx = kx~ and ~Ty = k'y~, ~x~ and ~y~ are distinct,
and ~y != qx~, then ~k'~ and ~k~ cannot be equal, and the
two vectors cannot be elements of the same eigenspace.

Note if ~y + qx~ then ~T(y) = T(qx) = k(qx) = ky~, and the
two vectors do belong to the same eigenspace and have
the same eigenvalue. So 'scaled versions' of the same
vector belong to the same eigenspace.
'''

stats_testcase = '''
This is the conceptual diagram with the generalization
of Bayes theorem from last class: ~pi(theta/X) alpha l(theta) dot pi(theta)~
'''

syntactically_demanding = '''

The absolute value of both sides gives 

~ (| epsilon sub [: n + 1 :] |) = fraction ( (| f'' (xi sub n) |) ) over ( 2 (| f' ( x sub n ) |) ) dot epsilon sub n sup 2 ~

and this shows something.

'''

beamer_testcase = '''
## The typed abstract machine

* A JVM state consists of a heap and a stack frame. Each
  frame contains a program counter, an operand stack and
  a register map.
* A typed state contains a stack type ~st~ and a register
  type ~rt~
* The typed abstract machine is defined by rules of the form

	from
		P[i] = instr
		constraints
	infer
		i |- st, rt => st', rt'

_________________________________________________

## Sample rules

     from 
_______________________________________
i |- int :: int st, rt => int :: st, rt

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
        ''',
        math_placeholders_testcase,
        math_testcase,
        stats_testcase,
        syntactically_demanding
]

math_tests = ['( a b over b a ) equals 1',
    'all x : x not in ø',
    'sum from a to n of f(x)',
    'sum over { x : g(x) in S } of h(x, g(x))',
]

math_examples = [
    ('a = b', 'a = b'),
    ('a != b', r'a \neq b'),
    ('a in A', r'a \in A'),
    ('for all x : exists y : x in A => r(x, y)', r'\forall x : \exists y : x \in A \Rightarrow r ( x , y )'),
    ('sum from i = 1 to n of i', r'\sum_{i = 1}^{n} i'),
    ('sum over t in T of f (t)', r'\sum_{t \in T} f ( t )'),
    ('sum over i in A of f sub i (x)', r'\sum_{i \in A} f_{i} ( x )'),
    ('sum over i in A of f sub i (x sub i sup 2)', r'\sum_{i \in A} f_{i} ( x_{i}^{2} )'),
    ('sum over i in A of f sup i (x sup i sub 2)', r'\sum_{i \in A} f^{i} ( x^{i}_{2} )'),
    ('a [: not in :] A', r'a \notin A'),
    ('a not in A', r'a \notin A'),
    ('for all x in R . exists y in R . xy = 1', r'\forall x \in \R . \exists y \in \R . xy = 1'), 
    # ('f : a -> b', ),
    # ('A included in B'),
    # ('A subset of B'),
    # ('A includes B')

]
