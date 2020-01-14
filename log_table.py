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
        
        if self.filetype == "md":
          intro = f"""# {days} Days Of Code - Log
*Main Commitment*:

I will code in **YOUR LANGUAGE** programming language for at least an hour every day for the next {days} days.

Start Date: **{start_day.strftime("%B %d, %Y")}**\n
End Date (without any breaks): **{end_day.strftime("%B %d, %Y")}**

-----
"""
        elif self.filetype == "html":
            intro = f"""<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <title>{self.days} Days Of Code - Log</title>

    <link
      rel="stylesheet"
      href="https://cdn.jsdelivr.net/gh/Microsoft/vscode/extensions/markdown-language-features/media/markdown.css"
    />
    <link
      rel="stylesheet"
      href="https://cdn.jsdelivr.net/gh/Microsoft/vscode/extensions/markdown-language-features/media/highlight.css"
    />

    <style>
      .task-list-item {{
        list-style-type: none;
      }}
      .task-list-item-checkbox {{
        margin-left: -20px;
        vertical-align: middle;
      }}
    </style>
    <style>
      body {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe WPC", "Segoe UI",
          "Ubuntu", "Droid Sans", sans-serif;
        font-size: 14px;
        line-height: 1.6;
      }}
    </style>
  </head>
  <body class="vscode-light">
    <h1 id="{self.days}-days-of-code---log">{self.days} Days Of Code - Log</h1>
    <p><em>Main Commitment</em>:</p>
    <p>
      I will code in <strong>YOUR LANGUAGE</strong> programming language for at
      least an hour every day for the next {self.days} days.
    </p>
    <p>Start Date: <strong>{self.start_day.strftime("%B %d, %Y")}</strong></p>
    <p>End Date (without any breaks): <strong>{(self.start_day + datetime.timedelta(self.days)).strftime("%B %d, %Y")}</strong></p>
    <hr />"""
        return intro

    def get_table_header(self):
        if self.filetype == "md":
            header = [["| Days |"]]
            header[-1].extend([f" {str(i)} |" for i in range(1,
                                                             self.columns + 1)])
            header.append([f"| -- " for i in range(self.columns + 1)])
            header[-1].extend("|")
        elif self.filetype == "html":
            header = [["""
    <table>
      <thead>
        <tr>
          <th>Days</th>"""]]
            header[-1].extend([f"\n          <th>{day}</th>"
                               for day in range(1, self.columns + 1)])
            header.append(["""        </tr>
      </thead>"""])

        return header

    def gen_table(self, iterator):
        day_count = 1
        table = []
        
        table.extend(self.get_table_header())

        if self.filetype == "md":
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
        elif self.filetype == "html":
            table.append(["      <tbody>"])
            while day_count <= self.days:
                row_counter = 0
                table.append(["        <tr>"])
                table.append([f"          <td>{day_count - 1:02d}</td>"])
                while row_counter < self.columns:
                    day = self.start_day + datetime.timedelta(day_count - 1)
                    day_format = day.strftime("%B-%d-%Y")
                    table.append(
                        [f'          <td><a href="#day-{day_count}-{day_format.lower()}">Day {day_count}</a></td>'])
                    row_counter += 1
                    day_count += 1
                    if day_count > self.days:
                        break
                table.append([f"        </tr>"])
            table.append(["""      </tbody>
    </table>"""])
        return table

    def get_blank_diary(self):
        diary = []
        day_count = 1

        while day_count <= self.days:
            day = self.start_day + datetime.timedelta(day_count - 1)
            day_format = day.strftime("%B %d, %Y")

            diary.append(self.get_string_entry(day_count, day_format))
            day_count += 1
        return "".join(diary)


    def get_string_entry(
            self,
            day_count,
            day_format,
            progress="",
            thoughts="",
            work="[Example](https://www.example.com)"):
        if self.filetype == "md":
            return f"""
### Day {day_count}:{" " + day_format if day_format else ""}

**Today's Progress**:{" " + progress if progress else ""}

**Thoughts**:{" " + thoughts if thoughts else ""}

**Link(s) to work**:\n{work}

[Back to Top](#{self.days}-days-of-code---log)

----""")
        elif self.filetype == "html":
            return f"""    <h3 id="day-{day_count}-{day_format_href.lower()}">Day {day_count}: {day_format}</h3>
    <p><strong>Today's Progress</strong>:</p>
    <p><strong>Thoughts:</strong></p>
    <p>
      <strong>Link(s) to work</strong>:
      <a href="http://www.example.com">Example</a>
    </p>
    <p><a href="#{self.days}-days-of-code---log">Back to Top</a></p>
    <hr />

""")

    def diary_from_entry_list(self, entry_list):
        '''
        Takes in a list of diary entries with keys
        Day -> datetime
        Progress -> Progress made str
        Thoughts -> Thoughts from the day str
        Work -> Links to work str
        '''
        return [self.get_string_entry(
                i + 1,
                entry['Day'].strftime("%B %d, %Y"),
                progress=entry["Progress"],
                thoughts=entry["Thoughts"],
                work=entry["Link"]) for i,
            entry in enumerate(entry_list)]

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


    def write_table(self, filename):
        with open(f"test.{self.filetype}", "w") as write_file:
            write_file.write(self.get_string_table())

if __name__ == '__main__':
    lt = LogTable(datetime.date.today(), columns=10, days=100, filetype="html")
    lt.write_table("test.md")
