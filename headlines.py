import urllib
import json
import xml.etree.ElementTree as ET
from argparse import ArgumentParser

URL_DEFAULT = 'http://feeds.bbci.co.uk/news/rss.xml'

def get(url):
    u = urllib.urlopen(url)
    data = u.read()
    return data

def parse(xml):
    root = ET.fromstring(xml)
    return root

def execute(url):
    data = get(url)
    root = parse(data)
    channel = root[0]
    # build up list of headline items
    items = []
    for child in channel:
        if child.tag == 'item':
            items.append(child)

    myDict = {}
    i = 0
    for item in items:
        f = lambda tag: item.find(tag)
        # store each item as dict
        myDict[i] = {
            'title': f('title').text,
            'description': f('description').text,
            'link': f('link').text,
            'guid': f('guid').text,
            'isPermaLink': bool(f('guid').get('isPermaLink')),
            'pubDate': f('pubDate').text
        }
        i += 1

    return myDict

def output(myDict):
    i = 0
    for key in myDict.keys():
        print 'headline', i
        for x in myDict[key].keys():
            print x, myDict[key][x]
        print ""
        i += 1

def main():
    ap = ArgumentParser()
    ap.add_argument('-u', '--url',
        type=str, default=URL_DEFAULT,
        help='URL to RSS XML')
    ap.add_argument('-f', '--file',
        type=str, default='',
        help='File to write output json string')
    ap.add_argument('-v', '--verbose',
        default=False, action='store_true',
        help='Print parsed headlines')
    args = ap.parse_args()

    headlinesDict = execute(args.url)
    if args.verbose:
        output(headlinesDict)

    jsonStr = json.dumps(headlinesDict)
    if args.file != '':
        f = open(args.file, 'w')
        f.write(jsonStr)
        f.close()
    else:
        print jsonStr

if __name__ == '__main__':
    main()
