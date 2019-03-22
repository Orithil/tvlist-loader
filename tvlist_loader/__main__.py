#!/usr/bin/env python3

import argparse
import json
import sys
from splinter import Browser
from tvlist_loader import xlparser
from tvlist_loader import scraper


def main():

    # Parse cli arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("FILE", help="Файл программы передач в формате Excel")
    parser.add_argument(
        "-s", "--sheet", help="Имя листа с программой передач. По умолчанию 'Лист1'")
    parser.add_argument("-a", "--auth", help="Файл с адресом сайта, логином и паролем в формате JSON")
    args = vars(parser.parse_args())

    # Set sheet to read
    if args["sheet"]:
        sheet = args["sheet"]
    else:
        sheet = "Лист1"

    table = xlparser.getTable(args["FILE"], sheet)
    week = xlparser.getDates(table)

    for day, value in week.items():
        week[day]["programs"] = xlparser.getProgram(table, value["id"])

    with open("schedule.json", "w") as file_json:
        json.dump(week, file_json, indent=4, ensure_ascii=False)

    if args["auth"]:
        file_client = args["auth"]
    else:
        file_client = "client_id.json"
    try:
        with open(file_client, "r") as file_json:
            client = json.load(file_json)
    except FileNotFoundError:
        print(f"Не удалось открыть {file_client}. Поместите файл 'client_id.json' в папку запуска программы или укажите другой файл с помощью параметра -a")
        sys.exit(1)
    except json.decoder.JSONDecodeError:
        print(f"Файл {file_client} не является корректным JSON.") 
        sys.exit(1)

    with Browser("firefox") as browser:
        site = client['site']
        scraper.login(browser, site, client['login'], client['password'])
        scraper.open_schedule(browser, site)

        for days in week.values():
            scraper.add_day(browser, days["day"], days["date"])
            for programs in days["programs"].values():
                scraper.add_program(
                    browser, programs["name"], programs["time"], programs["age"])
        scraper.commit(browser)


if __name__ == '__main__':
    main()
