import datetime
from argparse import ArgumentParser

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
                         "20 of december 2019" in any language. Default is today.')
args = parser.parse_args()

if args.date and isDateparserLoaded:
    start_day = dateparser.parse(args.date)
else:
    start_day = datetime.date.today()

with open("log.md", "x") as f:
    f.write(f"""# 100 Days Of Code - Log

*Main Commitment*:

I will code in **YOUR LANGUAGE** programming language for at least an hour every day for the next 100 days.

Start Date: {start_day.strftime("%B %d, %Y")}
End Date (without any breaks): {(start_day + datetime.timedelta(100)).strftime("%B %d, %Y")}

----
## Days:
|+|00                                    |10                                   |20                                 |30                                  |40                                  |50                                  |60                                  |70                                  |80                                  |90                                    |
|--|-------------------------------------|-------------------------------------|-----------------------------------|------------------------------------|------------------------------------|------------------------------------|------------------------------------|------------------------------------|------------------------------------|--------------------------------------|
""")
    time_var = start_day
    for i in range(10):
        f.write(f"|{i:02d}|")
        for j in range(1, 100, 10):
            day_format = time_var.strftime("%B-%d-%Y")
            f.write(f"[Day {i+j}](#day-{i+j}-{day_format.lower()}) | ")
            time_var += datetime.timedelta(10)
        if i+j == 99:
            f.write(f"[Day 100](#day-100-{day_format.lower()}) | ")
        f.write("\n")
        time_var -= datetime.timedelta(99)

    f.write(f"\n[Or Jump Right To Conclusion!](#Conclusion)\n")

    time_var = start_day
    for i in range(1, 101):
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
