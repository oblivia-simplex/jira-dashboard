import sys
import datetime
import re
import os

ATTRIBUTES = ["name", "total", "frequency", "average"]
COLOUR_ON = True
RAINBOW = ["yellow","green","blue","cyan","magenta","red"]


def colour(hue, shade="dark"):
  global COLOUR_ON
  if (not COLOUR_ON):
      return ""
  hues = {
      "reset":"0"
      ,"black":"30"
      ,"red":"31"
      ,"green":"32"
      ,"yellow":"33"
      ,"blue":"34"
      ,"magenta":"35"
      ,"cyan":"36"
      ,"white":"37"
  }
  shades = {
      "dark":"0"
      ,"light":"1"
  }
  if hue == 'grey' and shade == 'dark':
    hue, shade = 'black', 'light'
  elif hue == 'grey' and shade == 'light':
    hue, shade = 'white', 'dark'
  return "\x1b["+shades[shade]+";"+hues[hue]+"m"

DEBUG = 1
DBGLOG = []

def dbgprint(*args, **kwargs): #bullet='+', errprint=True):
  if not (DEBUG
          or ('stream' in kwargs)
          or ('override' in kwargs and kwargs['override'] == True)
          or (args[0][0]=='!')):
    return ''
  bullet = '+'
  errprint = True
  stream = sys.stderr
  if 'bullet' in kwargs:
    bullet = kwargs['bullet']
  if 'stream' in kwargs:
    stream = kwargs['stream']
  s = ' '.join(['{}'.format(x) for x in list(args)])
  if s[0] == '!' and len(s) >= 2:
    s = s[1:]
  m = re.match('^\[(.)\]',s)
  if not m:
    if 'WARNING' in s:
      bullet = 'X'
    b = '[{}]'.format(bullet)
    s = b+' '+s
  else:
    bullet = m.group(1)
  DBGLOG.append(s)
  col_s = s
  if bullet == 'X':
    col_s = colourize(s, "red", "light")
  elif bullet == '*':
    col_s = colourize(s, "green", "dark")
  if stream:
      print(col_s, file=stream)
  return col_s

def colourize(string, hue, shade="dark"):
  if not COLOUR_ON and shade=="light":
    return '*'+string+'*'
  return colour(hue, shade) + string + colour("reset")

def timestamp ():
  return "{:%Y-%m-%d_%H-%M}".format(datetime.datetime.now())

def compress_report(rows):

  rep = {}
  for row in rows:
    if row not in rep.keys():
      rep[row] = 1
    else:
      rep[row] += 1

  report = []
  for k in rep.keys():
    if rep[k] > 1:
      report.append(k + ' (x{})'.format(rep[k]))
    else:
      report.append(k)

  return report
