#!/usr/bin/env python3

import pandas as pd
import xlrd
import re
from datetime import datetime


def getTable(file, sheet):
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


def getDates(table):
    # Gets first header with dates and trims empty cells
    days = {}
    i = 0
    for cell in table.ix[0]:
        if cell == cell:
            i += 1
            date = cell.strip().split("_")
            days["day" + str(i)] = {"day": date[1], "date": date[0], "id": i}
    return days


def getProgram(table, id):
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
        name = row.iat[1]
        time = datetime.strptime(row.iat[0], "%H:%M") if isinstance(
            row.iat[0], str) else row.iat[0].strftime("%H:%M")
        age = str(int(row.iat[2].strip("+"))
                  ) if row.iat[2] == row.iat[2] else "0"
        program["program" + str(program_index)
                ] = {"name": name, "time": time, "age": age}
    return program
