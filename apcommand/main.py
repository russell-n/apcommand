
# this package
from argumentparser import Arguments
from log_setter import set_logger


def main():
    """
    Runs the command-line interface
    """    
    command_line = Arguments()
    args = command_line.args
    set_logger(args)
    if any((arg.pudb, args.pdb)):
        enable_debugger(args)
    args.function(args)
    return


if __name__ == "__main__":
    main()
