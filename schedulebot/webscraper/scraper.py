#!/usr/bin/env python3


def login(browser, site):
    browser.visit(site + 'wp-admin')
    login = 'friendlybot'
    password = 'friendlyBot'
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


def add_day(browser):
    browser.find_by_css('a.button[data-event="add-row"]').last.click()


def add_program(browser):
    browser.find_by_css('a.button[data-event="add-row"]')[-3].click()


def commit(browser):
    browser.find_by_id('publish').first.click()
