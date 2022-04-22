import os
import re
from webapp.models import TestLine, TestRun, TestCase


def insert_logs():
    folder_to_view = "webapp/logs"
    keywords = ["| PASS |", "| FAIL |"]
    keyword = [" -v CONFIGURATION"]

    for file_name in os.listdir(folder_to_view):
        # if file_name.endswith(".txt"): # extra, daca o sa am nevoie
        id_notepad = file_name.rpartition('.')[0]
        # print("id_notepad:")
        # print(id_notepad)

        with open("webapp/logs/" + file_name, encoding="utf8") as fin:
            line_date = []
            line_name = []
            line_status = []

            for line in fin:
                if any(i in line for i in keyword):
                    config_id = line.split("UTESRANCLOUD")[1].strip()
                    print("config_id:")
                    print(config_id)

                if any(i in line for i in keywords):
                    line_date.append(re.search("\[(.*?)\,", line).group(1))
                    line_name.append(re.search("\](.*?)\|", line).group(1))
                    line_status.append(re.search("\|(.*?)\|", line).group(1))

        TestLine_insert = TestLine(
            id = config_id
        )
        TestLine_insert.save()

        TestRun_insert = TestRun(
            id = id_notepad,
            test_line = TestLine.objects.get(id = config_id)
        )
        TestRun_insert.save()

        for i in range(len(line_status)):
            TestCase_insert = TestCase(
                status = line_status[i],
                case_name = line_name[i],
                execution_time = line_date[i],
                test_run = TestRun.objects.get(id = id_notepad)
            )
            TestCase_insert.save()
