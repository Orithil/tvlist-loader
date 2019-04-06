#!/usr/bin/env python3

def get_projects(browser, site):
    """ Gets projects list from site and returns it as a list
    """
    browser.visit(site)
    projects_list = []
    sitemenu = browser.find_by_css('.block_pop')[1].find_by_css('.themes_row > ul > li > a')
    for item in sitemenu:
        projects_list.append(item.html.upper())
    return projects_list

def check_project(name, projects_list):
    """ Checks if entry in tv list is a project instance.
        If entry name is identical to project name returns entry name.
        If some part of entry name matches project name or vice versa
        returns '1' to mark partial matching.
        If entry name does not match project name at all returns '2'
        to mark error.
    """
    if name in projects_list:
        return name
    else:
        for project in projects_list:
            if name in project or project in name:
                return project
        return '2'
