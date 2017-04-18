#!/usr/bin/env python
import csv
import argparse

from datetime import datetime

isodatef = '%Y-%m-%d %H:%M:%S'

def org_date(date):
    return date.strftime('%Y-%m-%d %a %H:%M')
    #return '2016-11-24 Thu 11:10'

def org_state_change(state, time):
    return '- %s [%s]' % (state, org_date(time))

def org_headline(title, content, created, todo='', state_changes=[]):
    tpl = '''* %s %s
:PROPERTIES:
:CREATED:  [%s]
:END:

'''
    s = tpl % (todo, title, org_date(created))
    s += content
    if state_changes:
        s += '\n\n:LOGBOOK:\n'
        s += '\n'.join([org_state_change(s, t) for s, t in state_changes])
        s += '\n:END:'

    return s

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('inputfile', type=argparse.FileType('r'))

    args = ap.parse_args()

    inputfile = args.inputfile

    r = csv.reader(inputfile)

    for note in r:
        created, modified, content = note
        if created == 'created':
            continue

        created = datetime.strptime(created, isodatef)
        modified = datetime.strptime(modified, isodatef)

        content = content.split('\n')
        title = content[0]
        if len(content) > 1:
            content = '\n'.join(content[1:])
        else:
            content = ''
        s = org_headline(title, content, created, state_changes=[('modified', modified)])
        print(s)
        print('\n')
            

if __name__ == '__main__':
    main()
