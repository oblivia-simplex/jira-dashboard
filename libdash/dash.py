import jira
from libdash.displayfuncs import *
import math
import curses
from libdash.creds import *
import sys
import datetime

# convenience functions for issues
def updated(issue):
  return issue.fields.updated.split('T')[0]

def assignee(issue):
  try:
    return issue.fields.assignee.name
  except AttributeError:
    return "UNASSIGNED"

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

def format_issue(issue, hide_assigned=False, colour=False):
  s = ""
  if not hide_assigned:
    s += "{}:{}".format(assignee(issue), gap("xxxxxxxxxxxxxxx", assignee(issue)))
    
  stat = status(issue)
  s += "{}{}{}  {}{}{}".format(key(issue),
                               gap('VULN-XXXXX', key(issue)),
                               updated(issue),
                               stat,
                               gap('Integration Review', stat),
                               summary(issue))
  if colour:
    if stat == "In Progress":
      s = colourize(s, "green")
  return s



class Board (object):

  def __init__(self, only_mine=True, colour=False):
    self.only_mine = only_mine
    self.query_prefix = "assignee = currentUser() AND" if only_mine else ""
    end_words = ["Resolved", "Closed", "Done"]
    self.my_unresolved_issues_query = "NOT (" + ' OR '.join("status = "+w for w in end_words) + ")"
    self.order_results = "ORDER BY updated"
    self.url = URL
    self.auth = (USERNAME, PASSWORD)
    self.jira = jira.JIRA(self.url, basic_auth=self.auth)
    self.issues = []
    self.colour = colour

  def search_issues(self, query=None):
    if query is None:
      query = self.my_unresolved_issues_query
    query = self.compose_query(query)
    dbgprint("query:",query)
    issues = self.jira.search_issues(query, maxResults=None)
    return issues

  def compose_query(self, query):
    return ' '.join((self.query_prefix, query, self.order_results))
  
  def print_issues_from_query(self, query):
    issues = self.search_issues(query)
    r = self.print_issues(issues)
    return r
  
  def print_issues(self, issues):
    report = []
    for issue in issues:
      report.append(format_issue(issue, self.only_mine, self.colour))
    if not report:
      return []  
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

def main(query=None, only_mine=True, colour=False):
  board = Board(only_mine=only_mine, colour=colour)
  board.print_issues_from_query(query)

