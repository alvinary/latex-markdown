import argparse
from latex import Latex

DESCRIPTION = '''
Compile markdown to LaTeX
'''

EPILOG = '''
Verbosity levels show: 1- rules, 2- grounded rules, and \n 3- dimacs ground clauses.\n
'''

class CLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description=DESCRIPTION, epilog=EPILOG)
        self.parser.add_argument(
            dest='markdown',
            default="",
            type=str,
            help='The input markdown text, which should be a text file.')
        self.parser.add_argument(
            '-o',
            dest='latex',
            default="no file",
            type=str,
            help='Name of the output file'
        )
        '''
        self.parser.add_argument(
        '-f',
        dest='flags',
        nargs="+",
        type=str,
        help=
        'Choose one of the flags { beamer, article } to decide how to process the input files.'
        )
        '''
        self.latex_parser = Latex()
        # self.beamer_parser = Beamer()
        
def textfile_input(input_file):
    text = ""
    with open(input_file) as current_file:
            for line in current_file:
                text = f"{text}{line}"
    return text
        
if __name__ == '__main__':
    
    cli = CLI()
    arguments = vars(cli.parser.parse_args())
    
    markdown_file = arguments['markdown']
    output_file = arguments['latex']
    
    if markdown_file:
        markdown = textfile_input(markdown_file)
    else:
        markdown = ""
        
    results, reports = cli.latex_parser.get_latex(markdown)
    
    if not results:
        print("The contents of the file could not be parsed, please check for errors in the input file!")
        print()
        print(f"This is the longest initial segment that was parsed successfully:")
        print()
        for r in reports[0:1]:
            r, s = r.split('<< SEGMENT END <<')
            r = r.replace("@BREAK@", "\n\n")
            r = r.replace("@_BEGIN_@", "")
            r = r.replace("@_END_@", "")
            r = r + '\n<< SEGMENT END <<\n' + s
            print(r)
            print('')
    else:
        for r in results:
           print(r, "\n")
        
        
