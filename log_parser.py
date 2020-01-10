from os import path
import datetime
import dateparser
from log_table import LogTable
import string


class LogParser():

    def __init__(self, filename):
        if not path.isfile(filename):
            raise ValueError(f"Log file {filename} does not exist")
        else:
            self.log_file = filename
        self.intro, self.table, self.diary = self.parse_log()
        self.days = self.get_days()
        self.diary_object_form = None

    def get_days(self):
        first_line = self.intro.split("\n")[0]
        days_string = "".join([char for char in first_line if char in string.digits])
        return int(days_string)

    def parse_log(self):
        with open(self.log_file, 'r') as log:
            log_text = log.read()
            intro, table, diary = log_text.split("-----\n")
            diary = diary.split("----")
            formatted_diary = [self.process_diary_entry(e) for e in diary]
            formatted_diary = [x for x in formatted_diary if x]
            return intro, table, formatted_diary

    def process_diary_entry(self, entry):
        entry = entry.strip()
        reduced_entry = entry.split("\n\n")[:-1]
        try:
            dict_entry = {
                key: value.strip() for key, value in [
                    x.split(":", 1) for x in reduced_entry]}
            for key in list(dict_entry.keys()):
                if "Day" in key:
                    dict_entry["Day"] = dict_entry[key]
                    del dict_entry[key]
            return dict_entry
        except ValueError:
            print(f"Failed for entry: \n{reduced_entry}")
            return {}

    def update_log(self):
        self.update_diary()
        self.update_table()
        self.update_intro()
        with open(self.log_file, 'w') as write_file:
            write_file.write(self.intro)
            write_file.write(self.table + "-----\n")
            write_file.write("".join(self.diary))
    
    def get_header(self, columns):
        header = [["| Days |"]]
        header[-1].extend([f" {str(i)} |" for i in range(1, columns + 1)])
        header.append([f"| -- " for i in range(columns + 1)])
        header[-1].extend("|")
        return header

    def update_table(self):
        if not self.diary_object_form:
            raise ValueError("Update diary before updating table")
        columns = len(self.table.split("\n")[0].strip("|").split("|")) - 1
        table_generator = LogTable(columns=columns, days=self.days)
        table_generator.day_iter = iter([dateparser.parse(entry['Day']) for entry in self.diary_object_form])
        table = table_generator.get_string_table()
        self.table = table
    
    def update_intro(self):
        table_generator = LogTable()
        days = [dateparser.parse(entry['Day']) for entry in self.diary_object_form]
        self.intro = table_generator.get_intro(start_day=days[0], end_day=days[-1], days=self.days)

    def update_diary(self):
        non_empty = [entry for entry in self.diary if not self.is_empty(entry)]
        last_day = dateparser.parse(
            non_empty[-1]["Day"]) if non_empty else None
        if last_day:
            while len(non_empty) < self.days:
                last_day += datetime.timedelta(1)
                non_empty.append({
                    "**Today's Progress**": '',
                    '**Thoughts**': '',
                    '**Link(s) to work**': '[Example](https://www.example.com)',
                    'Day': last_day.strftime("%B %d, %Y"),
                })
            new_diary = [
                self.get_string_entry(
                    i + 1,
                    entry['Day'],
                    progress=entry["**Today's Progress**"],
                    thoughts=entry["**Thoughts**"],
                    work=entry['**Link(s) to work**']) for i,
                entry in enumerate(non_empty)]
            self.diary = new_diary
            self.diary_object_form = non_empty

    def get_string_entry(
            self,
            day_count,
            day_format,
            progress="",
            thoughts="",
            work="[Example](https://www.example.com)"):
        return f"""
### Day {day_count}:{" " + day_format if day_format else ""}

**Today's Progress**:{" " + progress if progress else ""}

**Thoughts**:{" " + thoughts if thoughts else ""}

**Link(s) to work**:\n{work}

[Back to Top](#{self.days}-days-of-code---log)

----
"""

    def is_empty(self, entry):
        empty_entry_params = {
            "**Today's Progress**": '',
            '**Thoughts**': '',
            '**Link(s) to work**': '[Example](https://www.example.com)',
        }
        for key in empty_entry_params:
            if entry[key] != empty_entry_params[key]:
                return False
        return True


if __name__ == "__main__":
    lp = LogParser("log.md")
    lp.update_log()
    # print(lp.diary)
