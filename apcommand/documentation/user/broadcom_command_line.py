
# python standard library
import subprocess
# this package
from apcommand.broadcom.argumentparser import Arguments


arguments = Arguments()
arguments.add_arguments()
arguments.add_subparsers()
parser = arguments.parser

# this is so that it doesn't say 'Pweave' as the name
parser.prog = 'broadcom'
parser.print_help()


print subprocess.check_output('broadcom status --help'.split())


print subprocess.check_output('broadcom channel --help'.split())


print subprocess.check_output('broadcom enable --help'.split())
