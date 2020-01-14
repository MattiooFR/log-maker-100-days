from os import path
import datetime
import dateparser
from log_table import LogTable
import string


class LogParser():

    MAPPINGS = {
        'Progress': "**Today's Progress**",
        'Thoughts': "**Thoughts**",
        'Link': '**Link(s) to work**',
    }

    def __init__(self, filename):
        if not path.isfile(filename):
            raise ValueError(f"Log file {filename} does not exist")
        else:
            self.log_file = filename
        self.intro, self.table, self.diary = self.parse_log()
        self.days = self.get_days()
        self.day_list, self.new_day_log = self.get_new_day_log()
        self.table_generator = LogTable(columns=self.get_columns(), days=self.days)

    #
    # Getting the new diary and log
    # --------------------------------
    #

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
        dict_entry = {
            key: value.strip() for key, value in [
                x.split(":", 1) for x in reduced_entry]}
        for key in list(dict_entry.keys()):
            if "Day" in key:
                dict_entry["Day"] = dict_entry[key]
                del dict_entry[key]
        return dict_entry

    def get_days(self):
        first_line = self.intro.split("\n")[0]
        days_string = "".join([char for char in first_line if char in string.digits])
        return int(days_string)

    def get_new_day_log(self):
        non_empty = [entry for entry in self.diary if not self.is_empty(entry)]

        for entry in non_empty:
            entry['Day'] = dateparser.parse(entry['Day'])
            for key, value in LogParser.MAPPINGS.items():
                entry[key] = entry[value]

        last_day = non_empty[-1]['Day'] if non_empty else None
        if last_day:
            while len(non_empty) < self.days:
                last_day += datetime.timedelta(1)
                non_empty.append(self.get_blank_entry(last_day))

        day_list = [entry['Day'] for entry in non_empty]

        return day_list, non_empty

    def get_columns(self):
        columns = len(self.table.split("\n")[0].strip("|").split("|")) - 1
        return columns

    def get_blank_entry(self, day=None):
        new_entry = {
            "Progress": '',
            'Thoughts': '',
            'Link': '[Example](https://www.example.com)',
        }
        if day:
            new_entry['Day'] = day
        return new_entry

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

    #
    # Updating logs
    # ---------------------------
    #

    def update_log(self):
        self.update_diary()
        self.update_table()
        self.update_intro()
        with open(self.log_file, 'w') as write_file:
            write_file.write(self.intro)
            write_file.write(self.table + "-----\n")
            write_file.write("".join(self.diary))

    def update_table(self):
        table = self.table_generator.get_string_table(iterator=iter(self.day_list))
        self.table = table

    def update_intro(self):
        days = self.day_list
        self.intro = self.table_generator.get_intro(start_day=days[0], end_day=days[-1], days=self.days)

    def update_diary(self):
        new_diary = self.table_generator.diary_from_entry_list(self.new_day_log)
        self.diary = new_diary


if __name__ == "__main__":
    lp = LogParser("log.md")
    lp.update_log()
    # print(lp.diary)
