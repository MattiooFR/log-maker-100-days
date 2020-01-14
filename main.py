import datetime
import os.path
from argparse import ArgumentParser
from log_table import LogTable
from log_parser import LogParser

# TODO Put all the text parameters in another file (help customisation and
# later internationnalization).

class ErrorFormatDate(Exception):
    pass


def get_date_parser_loaded():
    try:
        import dateparser
        global dateparser
    except ImportError:
        print(
            "# INFO : Module dateparser is not installed, run : 'pip install dateparser', "
            "or pipenv|conda install dateparser if this is what you are using. \n"
            f"A log.{get_args().type} with the date of today ({datetime.date.today()}) "
            "will still be created in case this is what you are looking for.")
        return False
    return True


def get_args():
    parser = ArgumentParser()
    parser.add_argument(
        "date",
        nargs='?',
        default="",
        help='Set your own starting date : 22/12/2019, yesterday, or\
             "20 of december 2019" in any language. Default is today')
    parser.add_argument(
        "-o",
        "--overwrite",
        help='overwrite the existing log.md file',
        action="store_true")
    parser.add_argument(
        "-f",
        "--filename",
        help='choose your own filename output',
        type=str,
        default="log")
    parser.add_argument(
        "-l",
        "--list",
        help='append this log to an existing list of logs',
        action="store_true")
    parser.add_argument(
        "-d",
        "--duration",
        help='set a custom duration for your challenge',
        default=100,
        type=int)
    parser.add_argument(
        "-t",
        "--type",
        help='generate your log in html format',
        default="md",
        type=str)
    parser.add_argument("-v", "--verbose", help='print process infos',
                        action="store_true")
    parser.add_argument("-u", "--update", help='update an existing log file',
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


def get_create_string(args, filename):
    if os.path.isfile(filename) and args.overwrite:
        create_string = "w"
    else:
        create_string = "x"
    return create_string


def get_filename(args):
    if len(args.filename) > 3 and args.filename[-3:] == args.type:
        filename = args.filename
    else:
        filename = args.filename + "." + args.type
    return filename


def get_verbosity(args):
    return args.verbose

def print_message(args, start_day, duration, filename, create_string):
    print(f"main.py called with args: {args}")
    print(f"Writing log with start_day: {start_day} and duration: {duration} days "\
        + f"to filename '{filename}' with file writing options '{create_string}''")

def write_log_table(filename, create_string, start_day, duration):
    with open(filename, create_string) as f:
        log_table = LogTable(start_day, days=duration)
        f.write(log_table.get_intro())
        f.write(log_table.get_string_table())
        f.write(log_table.get_blank_diary())
        f.write(f"\n\n\n# Conclusion\n\n")
    if VERBOSE:
        print(f"Successfully wrote log file to {filename}")

def main():
    args = get_args()
    DPLoaded = get_date_parser_loaded()
    start_day = get_start_day(args, DPLoaded)
    duration = args.duration
    filename = get_filename(args)
    create_string = get_create_string(args, filename)

    if VERBOSE:
        print_message(args, start_day, duration, filename, create_string)

    if args.update:
        parser = LogParser(filename)
        parser.update_log()
    else:
        write_log_table(filename, create_string, start_day, duration)

if __name__ == '__main__':
    main()
