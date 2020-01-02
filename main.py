import datetime
import os.path
from argparse import ArgumentParser
from log_table import LogTable


class ErrorFormatDate(Exception):
    pass


isDateparserLoaded = True
try:
    import dateparser
except ImportError as e:
    print("# INFO : Module dateparser is not installed, run : 'pip install dateparser', \
or pipenv|conda install dateparser if this is what you are using. \
A log.md with the date of today will still be created in case this is what you are looking for.")
    isDateparserLoaded = False


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

if args.date and isDateparserLoaded:
    start_day = dateparser.parse(args.date)
    if not start_day:
        raise(ErrorFormatDate("Date format not recognized..."))
else:
    start_day = datetime.date.today()

duration = args.duration
if args.filename[-3:] == ".md":
    filename = args.filename
else:
    filename = args.filename + ".md"


if os.path.isfile(filename) and args.overwrite:
    create = "w"
else:
    create = "x"

with open(args.filename, create) as f:
        log_table = LogTable(start_day, days=args.duration)
        f.write(log_table.get_intro())
        f.write(log_table.get_string_table())
        f.write(log_table.get_diary())
        f.write(f"\n\n\n# Conclusion\n\n")

