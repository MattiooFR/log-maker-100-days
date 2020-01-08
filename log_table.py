import datetime


class LogTable():

    def __init__(self, start_day, columns=10, days=100, filetype="md"):
        self.columns = columns
        self.days = days
        self.start_day = start_day
        self.filetype = filetype
        self.table = self.gen_table()

    def get_intro(self):
        if self.filetype == "md":
            intro = f"""# {self.days} Days Of Code - Log
*Main Commitment*:

I will code in **YOUR LANGUAGE** programming language for at least an hour every day for the next {self.days} days.

Start Date: **{self.start_day.strftime("%B %d, %Y")}**\n
End Date (without any breaks): **{(self.start_day + datetime.timedelta(self.days)).strftime("%B %d, %Y")}**

----
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

    def get_header(self):
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

    def gen_table(self):
        day_count = 1
        table = []
        table.extend(self.get_header())

        if self.filetype == "md":
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

    def get_diary(self):
        diary = []
        day_count = 1

        while day_count <= self.days:
            day = self.start_day + datetime.timedelta(day_count - 1)
            day_format = day.strftime("%B %d, %Y")

            if self.filetype == "md":
                diary.append(f"""
### Day {day_count}: {day_format}

**Today's Progress**:

**Thoughts:**

**Link(s) to work**: [Example](http://www.example.com)

[Back to Top](#{self.days}-days-of-code---log)

----""")
            elif self.filetype == "html":
                day_format_href = day.strftime("%B-%d-%Y")
                diary.append(
                    f"""    <h3 id="day-{day_count}-{day_format_href.lower()}">Day {day_count}: {day_format}</h3>
    <p><strong>Today's Progress</strong>:</p>
    <p><strong>Thoughts:</strong></p>
    <p>
      <strong>Link(s) to work</strong>:
      <a href="http://www.example.com">Example</a>
    </p>
    <p><a href="#{self.days}-days-of-code---log">Back to Top</a></p>
    <hr />

""")
            day_count += 1
        return "".join(diary)

    def get_string_table(self):
        string_table = ""
        for row in self.table:
            string_table += "".join(row)
            string_table += "\n"
        string_table += "\n"
        return string_table

    def write_table(self, filename):
        with open(f"test.{self.filetype}", "w") as write_file:
            write_file.write(self.get_string_table())


if __name__ == '__main__':
    lt = LogTable(datetime.date.today(), columns=10, days=100, filetype="html")
    lt.write_table("test.md")
