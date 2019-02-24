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
    days = xlparser.getDates(table)

    for day, value in days.items():
        days[day]["programs"] = xlparser.getProgram(table, value["id"])

    with open("schedule.json", "w") as file_json:
        json.dump(days, file_json, indent=4, ensure_ascii=False)

    with Browser("firefox") as browser:
        site = "http://0.0.0.0:8080/"
        scraper.login(browser, site)
        scraper.open_schedule(browser, site)
        scraper.add_day(browser)
        scraper.add_program(browser)
        scraper.commit(browser)
