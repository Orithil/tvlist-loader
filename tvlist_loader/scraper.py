#!/usr/bin/env python3

from time import sleep


def login(browser, site, login, password):
    browser.visit(site + 'wp-admin')
    browser.find_by_id('user_login').fill(login)
    browser.find_by_id('user_pass').fill(password)
    browser.find_by_id('wp-submit').first.click()


def open_schedule(browser, site):
    browser.visit(site + 'wp-admin/edit.php?post_type=tv_program')
    try:
        browser.find_link_by_partial_text(
            'Программа передач').first.click()
    except splinter.exceptions.ElementDoesNotExist:
        print('Не удалось обнаружить ссылку на программу передач')


def add_day(browser, day, date):
    browser.find_by_css('a.button[data-event="add-row"]').last.click()
    field_day = browser.find_by_css(
        'div[data-name="tv_program_item_title"] input')
    field_date = browser.find_by_css(
        'div[data-name="tv_program_item_date"] input')
    field_day[-2].fill(day)
    field_date[-3].fill(date)


def add_program(browser, name, time, age, project, project_name):
    browser.find_by_css('a.button[data-event="add-row"]')[-3].click()
    field_name = browser.find_by_css(
        'div[data-name="tv_program_item_program_title"] input')
    field_time = browser.find_by_css(
        'div[data-name="tv_program_item_program_date"] input')
    field_age = browser.find_by_css(
        'div[data-name="tv_program_item_program_age"] input')
    field_name[-3].fill(name)
    if project:
        field_link = browser.find_by_css(
            'div[data-name="tv_program_item_program_link"] .select2')
        add_link(browser, field_link.last, project_name)
    field_time[-5].fill(time)
    field_age[-3].fill(age)

def add_link(browser, field, project_name):
    field.click()
    field_input = browser.find_by_css(".select2-search__field")
    field_input.fill(project_name)
    sleep(5)
    results = browser.find_by_css(".select2-results > ul > li")
    for li in results:
        if li.html.upper() == project_name:
            li.click()
            break

def commit(browser):
    browser.find_by_id('publish').first.click()
    sleep(60)
