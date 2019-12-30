import datetime

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
        f.write(f"[{i:02d}]")
        for j in range(1, 10):
            day_format = start_day.strftime("%B-%d-%Y")
            f.write(f"[Day {i*10+j}](#day-{i*10+j}-{day_format.lower()})")
            start_day += datetime.timedelta(1)
        f.write("\n")
    f.write(f"[Day 100](#day-100-{day_format.lower()})")
