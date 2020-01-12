import datetime


class LogTable():

    def __init__(self, start_day=datetime.date.today(), columns=10, days=100):
        self.columns = columns
        self.days = days
        self.start_day = start_day
        self.table = None
        self.day_iter = iter([self.start_day + datetime.timedelta(day_count - 1) for day_count in range(1, self.days + 1)])

    def get_intro(self, start_day=None, end_day=None, days=None):
        start_day = start_day if start_day else self.start_day
        end_day = end_day if end_day else start_day + datetime.timedelta(self.days - 1)
        days = days if days else self.days
        intro = f"""# {days} Days Of Code - Log
*Main Commitment*:

I will code in **YOUR LANGUAGE** programming language for at least an hour every day for the next {days} days.

Start Date: **{start_day.strftime("%B %d, %Y")}**\n
End Date (without any breaks): **{end_day.strftime("%B %d, %Y")}**

-----
"""
        return intro

    def get_table_header(self):
        header = [["| Days |"]]
        header[-1].extend([f" {str(i)} |" for i in range(1, self.columns + 1)])
        header.append([f"| -- " for i in range(self.columns + 1)])
        header[-1].extend("|")
        return header

    def gen_table(self, iterator):
        day_count = 1
        table = []
        table.extend(self.get_table_header())
        while day_count <= self.days:
            row_counter = 0
            table.append([])
            table[-1].append(f"| {day_count - 1:02d} |")
            while row_counter < self.columns:
                day = iterator.__next__()
                day_format = day.strftime("%B-%d-%Y")
                table[-1].append(
                    f"[Day {day_count}](#day-{day_count}-{day_format.lower()}) | ")
                row_counter += 1
                day_count += 1
                if day_count > self.days:
                    break
        return table

    def get_blank_diary(self):
        diary = []
        day_count = 1
        while day_count <= self.days:
            day = self.start_day + datetime.timedelta(day_count - 1)
            day_format = day.strftime("%B %d, %Y")
            diary.append(f"""
### Day {day_count}: {day_format}

**Today's Progress**: 

**Thoughts**: 

**Link(s) to work**: [Example](https://www.example.com)

[Back to Top](#{self.days}-days-of-code---log)

----
""")
            day_count += 1
        return "".join(diary)

    def get_string_table(self, iterator=None):
        iterator = iterator if iterator else self.day_iter
        if not self.table:
            self.table = self.gen_table(iterator)
        string_table = ""
        for row in self.table:
            string_table += "".join(row)
            string_table += "\n"
        string_table += "\n"
        return string_table + "-----"

if __name__ == '__main__':
    lt = LogTable(datetime.date.today(), columns=13, days=144)
    lt.write_table("test.md")
