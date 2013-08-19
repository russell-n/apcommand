
# Python Libraries
import logging
import logging.handlers
import os


logger = logging.getLogger(__package__)
SMALL_TIMESTAMP = "%H:%M:%S"
SCREEN_FORMAT = "%(levelname)s: %(name)s.%(funcName)s, Line: %(lineno)d [%(asctime)s] -- %(message)s"
SCREEN_FORMAT_QUIET = "%(levelname)s: [%(asctime)s] -- %(message)s"
DATA_FRIENDLY_FORMAT = "%(levelname)s,%(asctime)s,%(message)s"
LOG_FORMAT = "%(levelname)s,%(module)s,%(threadName)s,%(funcName)s,Line: %(lineno)d,%(asctime)s,%(message)s" 
LOG_TIMESTAMP = "%Y-%m-%d %H:%M:%S"

GIGABYTE = 1073741824
BACKUP_LOGS = 5

LOGNAME = "{0}.log".format(__package__)


def cleanup(log_directory="last_log", log_name=LOGNAME):
    """
    Saves the last log to log-directory

    :param:

     - `log_directory`: sub-directory to save old file to
     - `log_name`: the name of the log-file (default is log_setter.LOGNAME)

    :postconditions:

     - `log_directory` is a sub-directory of the current directory (if log exists)
     - log-file is moved to the log-directory (if log existed)
    """
    if not os.path.isfile(log_name):
        return
    if not os.path.isdir(log_directory):
        os.makedirs(log_directory)
    os.rename(log_name, os.path.join(log_directory, log_name))
    return


def set_logger(args):
    """
    Creates a logger and sets the level based on args.

    :param:

     - `args`: args with debug and silent attributes
    """
    cleanup()
    stderr = logging.StreamHandler()
    if args.debug:
        screen_format = SCREEN_FORMAT
    else:
        screen_format = SCREEN_FORMAT_QUIET
        
    screen_format = logging.Formatter(screen_format, datefmt=SMALL_TIMESTAMP)
    stderr.setFormatter(screen_format)

    log_file = logging.handlers.RotatingFileHandler(LOGNAME,
                                           maxBytes=GIGABYTE, backupCount=BACKUP_LOGS)
    file_format = logging.Formatter(LOG_FORMAT, datefmt=LOG_TIMESTAMP)
    log_file.setFormatter(file_format)
    
    logger.setLevel(logging.DEBUG)
    log_file.setLevel(logging.DEBUG)

    if args.debug:
        stderr.setLevel(logging.DEBUG)
    elif args.silent:
        stderr.setLevel(logging.ERROR)
    else:
        stderr.setLevel(logging.INFO)

    logger.addHandler(stderr)
    logger.addHandler(log_file)
    

    return 
