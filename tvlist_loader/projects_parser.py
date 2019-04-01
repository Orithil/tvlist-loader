#!/usr/bin/env python3

def get_projects(browser, site):
    browser.visit(site)
    projects_list = []
    sitemenu = browser.find_by_css('.block_pop')[1].find_by_css('.themes_row > ul > li > a')
    for item in sitemenu:
        projects_list.append(item.html.upper())
    return projects_list
