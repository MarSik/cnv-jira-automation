#!/bin/python3
"""Sync Epic priorities to tasks

Usage:
  $0 [-d] -u <user>

Options:
  -d            Dry run, do not change anything
  -u --user	JIRA username
"""


from docopt import docopt
import getpass
from jira import JIRA
import requests


if __name__ == "__main__":
    args = docopt(__doc__)
    passwd = getpass.getpass("Password for {}: ".format(args["--user"]))
    jira = JIRA('https://jira.coreos.com', basic_auth=(args["--user"], passwd))
    unprioritized = jira.search_issues('type IN (story, task) and project=CNV and component="CNV SSP" and priority = unprioritized and status in (New, "In Progress")')
    for issue in unprioritized:
        epicId = issue.fields.customfield_10006 # Epic link field for CNV
        if epicId is None:
            continue

        epic = jira.issue(epicId, fields=["priority"])
        print(issue, epic, epic.fields.priority.name)
        prio = epic.fields.priority.name
        if not args.get("-d", False):
            issue.update(priority={"name": prio})

