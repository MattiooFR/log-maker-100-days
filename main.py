import datetime
from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument("date", nargs='?', default="",
                    help="Set your own starting date here, format : yyyy-mm-dd")
args = parser.parse_args()

if args.date:
    start_day = datetime.date.fromisoformat(args.date)
else:
    start_day = datetime.date.today()

with open("log.md", "x") as f:
    f.write(f"""# 100 Days Of Code - Log

*Main Commitment*:

I will code in **Python** programming language for at least an hour every day for the next 100 days.

Start Date:
{start_day.strftime("%B %d, %Y")}.
End Date:

----
## Days:
|+|00                                    |10                                   |20                                 |30                                  |40                                  |50                                  |60                                  |70                                  |80                                  |90                                    |
|--|-------------------------------------|-------------------------------------|-----------------------------------|------------------------------------|------------------------------------|------------------------------------|------------------------------------|------------------------------------|------------------------------------|--------------------------------------|
""")

    for i in range(10):
        f.write(f"|{i:02d}|")
        for j in range(1, 100, 10):
            day_format = start_day.strftime("%B-%d-%Y")
            f.write(f"[Day {i+j}](#day-{i+j}-{day_format.lower()}) | ")
            start_day += datetime.timedelta(10)
        if i+j == 99:
            f.write(f"[Day 100](#day-100-{day_format.lower()}) | ")
        f.write("\n")
        start_day -= datetime.timedelta(99)

    f.write(f"\n[Or Jump Right To Conclusion!](#Conclusion)\n")

    if args.date:
        start_day = datetime.date.fromisoformat(args.date)
    else:
        start_day = datetime.date.today()

    for i in range(1, 101):
        day_format = start_day.strftime("%B, %d, %Y")
        f.write(f"""
### Day {i}: {day_format}

**Today's Progress**:

**Thoughts:**

**Link(s) to work**
[Example](http://www.example.com)

[Back Top](#days)

----""")
        start_day += datetime.timedelta(1)

    f.write(f"\n\n\n# Conclusion\n\n")
