#!/bin/python3
"""Set QE owner of all tasks to the QE owner of the epic

Usage:
  $0 [-d] -u <user>

Options:
  -u --user	JIRA username
  -d            Dry run, do not change anything
"""


from docopt import docopt
import getpass
from jira import JIRA
import requests


if __name__ == "__main__":
    args = docopt(__doc__)
    print(args)
    passwd = getpass.getpass("Password for {}: ".format(args["--user"]))
    jira = JIRA('https://issues.redhat.com', basic_auth=(args["--user"], passwd))
    no_qe_owner = jira.search_issues("""project=cnf and "QA Contact" is not empty and "QE Assignee" is empty""")
    for issue in no_qe_owner:
        print(issue, issue.fields.customfield_12315948.name)
        if not args.get("-d", False):
            issue.update(fields={"customfield_12316243": {"name": issue.fields.customfield_12315948.name}})

