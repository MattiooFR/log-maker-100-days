import datetime
import os.path
from argparse import ArgumentParser


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

with open(filename, create) as f:
    f.write(f"""# 100 Days Of Code - Log

*Main Commitment*:

I will code in **YOUR LANGUAGE** programming language for at least an hour every day for the next 100 days.

Start Date: **{start_day.strftime("%B %d, %Y")}**\n
End Date (without any breaks): **{(start_day + datetime.timedelta(100)).strftime("%B %d, %Y")}**

----
## Days:

""")

    header = "|+|"
    header += "".join([f"{i:02d}|" for i in range(0, duration, 10)])
    header += "\n|--|"
    header += "".join(["--|" for i in range(0, duration, 10)])
    header += "\n"
    f.write(header)

    time_var = start_day
    for i in range(10):
        f.write(f"|{i:02d}|")
        for j in range(1, duration, 10):
            day_format = time_var.strftime("%B-%d-%Y")
            f.write(f"[Day {i+j}](#day-{i+j}-{day_format.lower()}) | ")
            time_var += datetime.timedelta(10)
        if i+j == duration-1:
            f.write(
                f"[Day {duration}](#day-{duration}-{day_format.lower()}) | ")
        f.write("\n")
        time_var -= datetime.timedelta(duration-1)

    f.write(f"\n[Or Jump Right To Conclusion!](#Conclusion)\n")

    time_var = start_day
    for i in range(1, duration+1):
        day_format = time_var.strftime("%B, %d, %Y")
        f.write(f"""
### Day {i}: {day_format}

**Today's Progress**:

**Thoughts:**

**Link(s) to work**
[Example](http://www.example.com)

[Back Top](#days)

----""")
        time_var += datetime.timedelta(1)

    f.write(f"\n\n\n# Conclusion\n\n")

print(args)
