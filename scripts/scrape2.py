import numpy
import json
import urllib
import bs4
from bs4 import BeautifulSoup
import json

prefix = "https://www.law.cornell.edu"

def chapter_scrape(soup):
    letters2 = soup.find_all("div", {"class": "liicontent"})
    for e in letters2:
        if e.get_text().isspace():
            continue
        else:
            #print e.get_text().strip()
            s = e.get_text().strip()
            s = s.replace('\n                ', ' ')
            return s
    letters = soup.find_all("div", {"class": "item-list"})
    dict = {}
    for e in letters:
        if len(e.get_text()) <= 14:
            continue
        text = str(e).split('a alt=')
        text = text[1:]
        for elem in text:
            link = elem.split('href="')
            link = link[1].split('" title="')
            title = link[1].split('</a>')
            title = title[0].split('"')
            title = title[0]
            link = link[0]

            dict[title] = {}
            print str(prefix+link)
            page = urllib.urlopen(prefix + link).read()
            soup = BeautifulSoup(page, "html5lib")
            #print link
            dict[title] = chapter_scrape(soup)
            #print title
    return dict




def recursive_scrape(url_name):
    page = urllib.urlopen(url_name).read()
    soup = BeautifulSoup(page, "html5lib")
    letters = soup.find_all("li", class_="tocitem")
    print(len(letters))
    dict = {}
    for element in letters:
        dict[element.a.get_text()] = {}

        link = prefix + element.a["href"]
        page = urllib.urlopen(link).read()
        soup = BeautifulSoup(page, "html5lib")
        print element.a.get_text()
        dict[element.a.get_text()] = chapter_scrape(soup)

    #print dict
    with open('jlist.txt', 'w+') as outfile:
        json.dump(dict, outfile)


if __name__ == '__main__':
    recursive_scrape("https://www.law.cornell.edu/uscode/text")