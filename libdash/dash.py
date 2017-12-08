import jira
import math
import curses
from libdash.creds import *
import sys
import datetime

# convenience functions for issues
def updated(issue):
  return issue.fields.updated.split('T')[0]

def status(issue):
  try:
    return issue.fields.status.name
  except AttributeError as e:
    return "UNKNOWN: {}".format(e)

def key(issue):
  return issue.key

def summary(issue):
  return issue.fields.summary


def gap(sample, string, plus=2):
  return ' '*((len(sample) - len(string)) + plus)

def format_issue(issue):
  s = "{}{}{}  {}{}{}".format(key(issue),
                              gap('VULN-XXXXX', key(issue)),
                              updated(issue),
                              status(issue),
                              gap('In Code Review', status(issue)),
                              summary(issue))
  return s



class Board (object):

  def __init__(self, only_mine=True):
    self.query_prefix = "assignee = currentUser() AND" if only_mine else ""
    self.my_unresolved_issues_query = """
    NOT (status = "Resolved" OR status = "Closed") 
    """
    self.order_results = "ORDER BY updated"
    self.url = URL
    self.auth = (USERNAME, PASSWORD)
    self.jira = jira.JIRA(self.url, basic_auth=self.auth)
    self.issues = []

  def search_issues(self, query):
    issues = self.jira.search_issues(query, maxResults=None)
    return issues

  def compose_query(self, query):
    return ' '.join((self.query_prefix, query, self.order_results))
  
  def print_issues_from_query(self, query):
    if query is None:
      query = self.my_unresolved_issues_query
    query = self.compose_query(query)
    dbgprint("query:",query)
    exit(1)
    issues = self.search_issues(query)
    r = self.print_issues(issues)
    return r
  
  def print_issues(self, issues):
    report = []
    for issue in issues:
      report.append(format_issue(issue))
    maxwidth = max(len(row) for row in report)
    border = '-=' * math.ceil(maxwidth/2)
    print(border)
    for row in report:
      print(row)
    print(border)
    return report
  
  
    


class Display (object):

  def __init__(self, board):
    self.screen = curses.initscr()
    self.screen.keypad(True)
    self.board = board
    
  def refresh(self):
    curses.cbreak()

  def exit(self):
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    sys.exit(0)
    

    # TODO

def main(query=None, only_mine=True):
  board = Board(only_mine=only_mine)
  board.print_issues_from_query(query)

