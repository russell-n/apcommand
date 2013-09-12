
# this package
from argumentparser import Arguments
from log_setter import set_logger


def enable_debugger(args):
    """
    Enables interactive debugger (pudb takes precedence over pdb)

    :param:

     - `args`: namespace with pudb and pdb attributes
    """
    if args.pudb:
        import pudb
        pudb.set_trace()
        return
    elif args.pdb:
        import pdb
        pdb.set_trace()
    return


def main():
    """
    Runs the command-line interface
    """    
    command_line = Arguments()
    args = command_line.arguments
    set_logger(args)
    if any((args.pudb, args.pdb)):
        enable_debugger(args)
    args.function(args)
    return


if __name__ == "__main__":
    main()
