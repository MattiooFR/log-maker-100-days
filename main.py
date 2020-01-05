import datetime
import os.path
import string
from argparse import ArgumentParser
from log_table import LogTable

# TODO :
# I would suggest to change the name of your main.py, that could be confusing.
# I would also put all the text parameters in another file (help customisation and later internationnalization).
# You could also exit at the very begining it all the lib are not available (os.exit(1) or something close)...


VERBOSE = False

class ErrorFormatDate(Exception):
    pass


def get_date_parser_loaded():
    try:
        import dateparser
    except ImportError as e:
        print("# INFO : Module dateparser is not installed, run : 'pip install dateparser', \
    or pipenv|conda install dateparser if this is what you are using. \
    A log.md with the date of today will still be created in case this is what you are looking for.")
        return False
    return True


def get_args():
    parser = ArgumentParser()
    parser.add_argument("date", nargs='?', default="",
                        help='Set your own starting date : 22/12/2019, yesterday, or\
                            "20 of december 2019" in any language. Default is today')
    parser.add_argument("-o", "--overwrite", help='overwrite the existing log.md file',
                        action="store_true")
    parser.add_argument("-f", "--filename", help='choose your own filename output',
                        type=str, default="log.md")
    parser.add_argument("-l", "--list", help='append this log to an existing list of logs',
                        action="store_true")
    parser.add_argument("-d", "--duration", help='set a custom duration for your challenge',
                        default=100, type=int)
    parser.add_argument("-v", "--verbose", help='print process infos',
                        action="store_true")
    args = parser.parse_args()
    return args


def get_start_day(args, isDateparserLoaded):
    if args.date and isDateparserLoaded:
        start_day = dateparser.parse(args.date)
        if not start_day:
            raise(ErrorFormatDate("Date format not recognized..."))
    else:
        start_day = datetime.date.today()
    return start_day


def get_create(args, filename):
    if os.path.isfile(filename) and args.overwrite:
        create = "w"
    else:
        create = "x"
    return create


def get_filename(args):
    if len(args.filename) > 3 and args.filename[-3:] == ".md":
        filename = args.filename
    else:
        filename = args.filename + ".md"
    while not args.overwrite and args.list and os.path.isfile(filename):
        if filename[-4] not in string.digits:
            filename = filename[:-3] + "1" + filename[-3:]
        else:
            i = -5
            while i > (-1 * len(filename)) and filename[i] in string.digits:
                i -= 1
            filename = filename[:i + 1] + str(int(filename[i + 1 : -3]) + 1) + filename[-3:]
    
    return filename


def get_verbosity(args):
    return args.verbose

def print_message(args, start_day, duration, filename, create):
    print(f"main.py called with args: {args}")
    print(f"Writing log with start_day: {start_day} and duration: {duration} days "\
        + f"to filename '{filename}' with file writing options '{create}''")

def main():
    args = get_args()
    VERBOSE = get_verbosity(args)
    DPLoaded = get_date_parser_loaded()
    start_day = get_start_day(args, DPLoaded)
    duration = args.duration
    filename = get_filename(args)
    create = get_create(args, filename)

    if VERBOSE:
        print_message(args, start_day, duration, filename, create)

    with open(filename, create) as f:
        log_table = LogTable(start_day, days=duration)
        f.write(log_table.get_intro())
        f.write(log_table.get_string_table())
        f.write(log_table.get_diary())
        f.write(f"\n\n\n# Conclusion\n\n")


if __name__ == '__main__':
    main()
