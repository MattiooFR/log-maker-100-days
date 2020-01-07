from os import path
import datetime

class LogParser():

    def __init__(self, filename):
        if not path.isfile(filename):
            raise ValueError(f"Log file {filename} does not exist")
        else:
            self.log_file = filename
        self.intro, self.table, self.diary = self.parse_log()

    def parse_log(self):
        with open(self.log_file, 'r') as log:
            log_text = log.read()
            intro, table, diary = log_text.split("----")
            diary = diary.split("---")
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
        pass
    def is_empty(self, entry):
        pass

