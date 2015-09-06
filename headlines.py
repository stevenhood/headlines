import urllib
import json
import xml.etree.ElementTree as ET

URL_SOURCE = 'http://feeds.bbci.co.uk/news/rss.xml'

def get(url):
    u = urllib.urlopen(url)
    data = u.read()
    return data

def parse(xml):
    root = ET.fromstring(xml)
    return root

def main():
    data = get(URL_SOURCE)
    root = parse(data)
    channel = root[0]
    # print data

    # build up list of headline items
    items = []
    for child in channel:
        if child.tag == 'item':
            items.append(child)

    myDict = {}
    i = 0
    for item in items:
        f = lambda tag: item.find(tag).text
        # store each item as dict
        myDict[i] = {
            'title': f('title'),
            'description': f('description'),
            'link': f('link'),
            'guid': f('guid'),
            'isPermaLink': item.find('guid').get('isPermaLink'),
            'pubDate': f('pubDate')
        }
        i += 1

    # for key in myDict.keys():
    #     print key, myDict[key]

    print json.dumps(myDict)

if __name__ == '__main__':
    #print get(URL_SOURCE)
    main()
