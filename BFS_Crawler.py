from collections import deque, Counter

import requests
from bs4 import BeautifulSoup


class link:
    def __init__(self, url, depth=0):
        super().__init__()
        self.url = url
        self.mostFrequentWord = None
        self.linksOnPage = list()
        self.depth = depth

    def extractDetails(self, htmlCode):
        soup = BeautifulSoup(htmlCode, 'html.parser')
        for url in soup.findAll('a'):
            href = url.get('href')
            if href and href[:4] == "http":
                self.linksOnPage.append(href)

        text = " ".join(soup.strings)
        text = text.split()
        wordFrequency = Counter(text)
        for word in wordFrequency:
            if word == '' or word == ' ' or word == '\n':
                continue
            if self.mostFrequentWord is None:
                self.mostFrequentWord = (word, wordFrequency[word])
            elif wordFrequency[word] > self.mostFrequentWord[1]:
                self.mostFrequentWord = (word, wordFrequency[word])
        if self.mostFrequentWord is None:
            self.mostFrequentWord = ('NA', -1)


def outputToFileScreen(message):
    print(message)
    print(message, file=file)


def crawler(startURL, limit, timeout=10):
    assert isinstance(startURL, str), 'URL Not in string format'
    visited = set()
    listOfLinks = []
    outputToFileScreen("Crawling Started\n")
    queue = deque()
    queue.append(startURL)
    queue.append('-1')
    visited.add(startURL)
    depth = 0
    while len(queue) > 0 and (len(listOfLinks) < limit or limit == -1):
        url = queue[0]
        queue.popleft()
        if url == '-1':
            depth += 1
            if (len(queue) != 0):
                queue.append('-1')
        else:
            try:
                outputToFileScreen("Trying To parse {}".format(url))
                htmlCode = requests.get(url, timeout=timeout).text
                outputToFileScreen("Completed Parsing {}\n".format(url))
            except:
                outputToFileScreen("Unable To parse {}\n".format(url))
                continue
            Link = link(url, depth)
            Link.extractDetails(htmlCode)
            listOfLinks.append(Link)
            for eachLink in Link.linksOnPage:
                if eachLink not in visited:
                    queue.append(eachLink)
                    visited.add(eachLink)

    outputToFileScreen("Finished Crawling\n")
    return listOfLinks


if __name__ == '__main__':
    file = open("log.txt", 'w')

    try:
        startURL = input("Enter Starting Url(Start with http:// or https://): ")
        maxNumberOfLinksToParse = int(input("Enter Max number of Links to parse(-1 for No Limit): "))
        timeout = int(input("Enter Maximum time for a page(in seconds):"))
    except:
        print("Invalid Input")
        exit()

    listOfLinks = crawler(startURL, maxNumberOfLinksToParse)

    outputToFileScreen("Result")
    outputToFileScreen("Total Pages Parsed: {}\n".format(len(listOfLinks)))

    for link in listOfLinks:
        outputToFileScreen(
            "URL: {}\nDepth: {}\nMost Frequent Word: {}\nNumber of Links on Page: {}\n".format(link.url, link.depth,
                                                                                               link.mostFrequentWord,
                                                                                               len(link.linksOnPage)))
