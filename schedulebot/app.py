#!/usr/bin/env python3

import argparse
import json
import sys
from splinter import Browser
import schedulebot.xlparser.parser as xlparser
import schedulebot.webscraper.scraper as scraper


def main():

    # Parse cli arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("FILE", help="Файл программы передач в формате Excel")
    parser.add_argument(
        "-s", "--sheet", help="Имя листа с программой передач. По умолчанию 'Лист1'")
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

    with Browser("firefox") as browser:
        site = "http://0.0.0.0:8080/"
        scraper.login(browser, site)
        scraper.open_schedule(browser, site)

        # for days in week.values():
        #    scraper.add_day(browser, days["day"], days["date"])
        testday = week["day1"]
        scraper.add_day(browser, testday["day"], testday["date"])
        for programs in testday["programs"].values():
            scraper.add_program(
                browser, programs["name"], programs["time"], programs["age"])
        scraper.commit(browser)
