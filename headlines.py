import urllib
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
            # print child.tag, child.attrib

    # print headlines
    for item in items:
        try:
            print item.find('title').text
            print item.find('description').text
            print item.find('link').text
            print item.find('guid').text
            print item.find('guid').get('isPermaLink')
            print item.find('pubDate').text
        except Exception as e:
            print "[Exception: Failed to encode]"
        finally:
            print ""

if __name__ == '__main__':
    #print get(URL_SOURCE)
    main()
