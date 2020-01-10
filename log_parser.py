from os import path
import datetime
import dateparser

class LogParser():

    def __init__(self, filename):
        if not path.isfile(filename):
            raise ValueError(f"Log file {filename} does not exist")
        else:
            self.log_file = filename
        self.intro, self.table, self.diary = self.parse_log()
        self.days = 100 # TODO: Parse

    def parse_log(self):
        with open(self.log_file, 'r') as log:
            log_text = log.read()
            intro, table, diary = log_text.split("-----")
            diary = diary.split("----")
            formatted_diary = [self.process_diary_entry(e) for e in diary]
            formatted_diary = [x for x in formatted_diary if x]
            return intro, table, formatted_diary
    
    def process_diary_entry(self, entry):
        entry = entry.strip()
        reduced_entry = entry.split("\n\n")[:-1]
        try:
            dict_entry = {key: value.strip() for key, value in [x.split(": ") for x in reduced_entry]}
            for key in list(dict_entry.keys()):
                if "Day" in key:
                    dict_entry["Day"] = dict_entry[key]
                    del dict_entry[key]
            return dict_entry
        except ValueError:
            print(f"Failed for entry: \n{reduced_entry}")
            return {}

    def update_log(self):
        non_empty = [entry for entry in self.diary if not self.is_empty(entry)]
        print(f"Non-empty length = {len(non_empty)}")
        last_day = dateparser.parse(non_empty[-1]["Day"]) if non_empty else None
        print(last_day)
        if last_day:
            while len(non_empty) < self.days:
                last_day += datetime.timedelta(1)
                non_empty.append({
                    "**Today's Progress**": '', 
                    '**Thoughts**': '', 
                    '**Link(s) to work**': '[Example](https://www.example.com)',
                    'Day': last_day.strftime("%B %d, %Y"),
                })
            for entry in non_empty:
                print(entry)
            new_diary = [self.get_string_entry(i, entry['Day'], progress=entry["**Today's Progress**"],
                            thoughts=entry["**Thoughts**"], work=entry['**Link(s) to work**']) 
                        for i, entry in enumerate(non_empty)]
            self.diary = new_diary
            with open(self.log_file, 'w') as write_file:
                write_file.write(self.intro + "-----")
                write_file.write(self.table + "-----")
                write_file.write("".join(self.diary))


    def get_string_entry(self, day_count, day_format, progress="", thoughts="", work="[Example](https://www.example.com)" ):
        return f"""
### Day {day_count}: {day_format}

**Today's Progress**: {progress}

**Thoughts**: {thoughts}

**Link(s) to work**: {work}

| |
| :--: |
| [Back to Top](#{self.days}-days-of-code---log) |

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



