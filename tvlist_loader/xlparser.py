#!/usr/bin/env python3

import pandas as pd
import xlrd
import re
from tvlist_loader import projects_parser as pp
from datetime import datetime


def get_table(file, sheet):
    # Read file
    try:
        df = pd.read_excel(file, sheet_name=sheet, header=None, skiprows=[0])
    except IOError:
        sys.exit(f"Не удалось открыть файл {file}")
    except xlrd.biffh.XLRDError:
        sys.exit(f"Не удалось найти лист \"{sheet}\"")

    # Replace empty strings that might oocure in some cells with Nan values
    df.replace(r"^ +", pd.np.nan, regex=True, inplace=True)
    # Trim rows and columns that consist of Nan values only
    df.dropna(axis=0, how="all", inplace=True)
    df.dropna(axis=1, how="all", inplace=True)

    return df


def get_dates(table):
    # Gets first header with dates and trims empty cells
    days = {}
    i = 0
    for cell in table.ix[0]:
        if cell == cell:
            i += 1
            date = cell.strip().split("_")
            days["day" + str(i)] = {"day": date[1], "date": date[0], "id": i}
    return days


def get_program(table, id, projects):
    program = {}
    # Program table has three columns: 'time', 'name', and 'age'
    TABLE_WIDTH = 3
    # Set start and stop indexes for table slice of three columns
    start_index = id * TABLE_WIDTH - TABLE_WIDTH
    stop_index = start_index + TABLE_WIDTH
    # Rows with programs list start from index 2
    table = table.iloc[2:, start_index:stop_index]
    table.dropna(axis=0, how="all", inplace=True)
    program_index = 0

    for row_index in range(table.index[0], table.index[-1] + 1):
        row = table.ix[row_index]
        program_index += 1
        name = fix_quotes(row.iat[1])
        project = pp.check_project(name, projects)
        if project == "2":
            bproject = False
            project_name = ""
        else:
            bproject = True
            project_name = project
        time = datetime.strptime(row.iat[0], "%H:%M") if isinstance(
            row.iat[0], str) else row.iat[0].strftime("%H:%M")
        age = str(row.iat[2]).strip("+") if row.iat[2] == row.iat[2] else "0"
        program["program" + str(program_index)
                ] = {"name": name, "time": time, "project": bproject, "project_name": project_name, "age": age}
    return program


def fix_quotes(name):
    name = name.strip()
    name = re.sub(r"""\s+""", ' ', name)
    name = re.sub(r"""\s["]""", ' «', name)
    name = re.sub(r"""["]$""", '»', name)
    name = re.sub(r"""(^[хдмт]/[фс]\s)(.*)([А-Я0-9]$)""", r"""\1«\2\3»""", name)
    return name
