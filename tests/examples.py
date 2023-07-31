basicExample = '''

# A super long example

## Anatomy of a Serial Procrastinator

Pee poo pee pee poo. Ala ala momola
soco choco me eme asasaa lllaaa aaaa
ssldsdl . asdad. asdasdadasd.

asaskasaksdasdasd

## asmakdjasdlkajsdla

asdasd sadasdas vksjadlkq dkqjdc asdkj KAJ DS
sadasd as dad asdadad.

adasda ddasd a.

adasdadasd. asdasfasf.af fafafaf.
afsfaf. fafafafa.

aaaa.
'''        
        
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

testText = '''# Common Words for Kitchen Items

____________

## Kitchen Items

If you are standing in a kitchen, you may find one or several of these items:

* A big plastic box that humms and has a door

* A small plastic box with a round door or
a lid that can be opened from above, with a strange cylinder with holes

== Note ======

The plastic things are all connected to a power supply, do not fiddle with them haphazardly

=======

_____________________

* The first item is called A FRIDGE
* The second item is a WASHING MACHINE

Both items are types of appliances


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
    ('sum over i in A of f sub i (x sub i sup 2)', '\\sum_{i \\in A} f_i(x_i^2)'),
    ('sum over i in A of f sup i (x sup i sub 2)', '\\sum_{i \\in A} f^i(x^i_2)'),
    ('a not in A', 'a \\\\notin A'),
    # ('f : a -> b', ),
    # ('A included in B'),
    # ('A subset of B'),
    # ('A includes B')

]
