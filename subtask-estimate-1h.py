#!/bin/python3
"""Set original estimate of every subtask to 1 day

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
    jira = JIRA('https://jira.coreos.com', basic_auth=(args["--user"], passwd))
    unprioritized = jira.search_issues('((type=Task and issueFunction not in hasSubtasks()) or type=Sub-task) and project=CNV and component="CNV SSP" and originalEstimate is empty and status in (New, "In Progress")')
    for issue in unprioritized:
        print(issue, issue.fields.summary)
        if not args.get("-d", False):
            issue.update(fields={"timetracking": [{"edit": {"originalEstimate": "1d"}}]})

