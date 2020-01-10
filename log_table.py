import datetime


class LogTable():

    def __init__(self, start_day, columns=10, days=100):
        self.columns = columns
        self.days = days
        self.start_day = start_day
        self.table = self.gen_table()

    def get_intro(self):
        intro = f"""# {self.days} Days Of Code - Log
*Main Commitment*:

I will code in **YOUR LANGUAGE** programming language for at least an hour every day for the next 100 days.

Start Date: **{self.start_day.strftime("%B %d, %Y")}**\n
End Date (without any breaks): **{(self.start_day + datetime.timedelta(self.days)).strftime("%B %d, %Y")}**

-----
"""
        return intro

    def get_header(self):
        header = [["| Days |"]]
        header[-1].extend([f" {str(i)} |" for i in range(1, self.columns + 1)])
        header.append([f"| -- " for i in range(self.columns + 1)])
        header[-1].extend("|")
        return header

    def gen_table(self):
        day_count = 1
        table = []
        table.extend(self.get_header())
        while day_count <= self.days:
            row_counter = 0
            table.append([])
            table[-1].append(f"| {day_count - 1:02d} |")
            while row_counter < self.columns:
                day = self.start_day + datetime.timedelta(day_count - 1)
                day_format = day.strftime("%B-%d-%Y")
                table[-1].append(
                    f"[Day {day_count}](#day-{day_count}-{day_format.lower()}) | ")
                row_counter += 1
                day_count += 1
                if day_count > self.days:
                    break
        return table

    def get_diary(self):
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

| |
| :--: |
| [Back to Top](#{self.days}-days-of-code---log) |

----
""")
            day_count += 1
        return "".join(diary)

    def get_string_table(self):
        string_table = ""
        for row in self.table:
            string_table += "".join(row)
            string_table += "\n"
        string_table += "\n"
        return string_table + "-----"

    def write_table(self, filename):
        with open("test.md", "w") as write_file:
            write_file.write(self.get_string_table())


if __name__ == '__main__':
    lt = LogTable(datetime.date.today(), columns=13, days=144)
    lt.write_table("test.md")
