import urllib.request
import bs4 as bs
import optparse
import time
import os
from datetime import datetime

__location__ = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))


def getArguments():

    parser = optparse.OptionParser()

    parser.add_option("-u", "--url", dest="url",
                      help="URL to Flashback thread")
    parser.add_option("-p", "--pages", dest="pages",
                      help="Pages for Flashback thread")
    (options, arguments) = parser.parse_args()
    if not options.url:
        parser.error("[-] Please specify an URL --help for info.")
    elif not options.pages:
        parser.error(
            "[-] Please specify number of pages of thread--help for info.")
    return options


options = getArguments()


def threadParser(url):
    print("---------------------- Parsing Post ----------------------")
    contents = ""
    url_contents = urllib.request.urlopen(url).read()
    soup = bs.BeautifulSoup(url_contents, "html.parser")

    for div in soup.find_all("div", {'class': "post-bbcode-quote-wrapper"}):
        div.decompose()
    for div in soup.find_all('a'):
        div.decompose()
    for div in soup.find_all('img'):
        div.decompose()

    div = soup.findAll("div", {"class": "post_message"})

    for post in div:
        tmp = str(post)
        ind1 = tmp.find('\n')
        ind2 = tmp.rfind('\n')
        tmp = tmp[ind1 + 1:ind2].replace("<br/>", " ").replace(
            "<i>", " ").replace("</i>", " ").replace("'", '"')
        tmp = " ".join(tmp.split())
        contents = contents + "\n" + tmp
    print("[i] Content snippet: " + contents[0:45] + "\n")
    return contents


def pageCounter(url, pages):

    date = datetime.today().strftime('%Y-%m-%d')
    file_title = 'flashback_tread_' + url[-8:-1] + '_parsed_' + date + '.csv'

    print("opening file")
    f = open(os.path.join(__location__, file_title),
             "w", encoding="utf-8")

    for x in range(1, int(pages)):
        text = threadParser(url + "p" + str(x))
        f.write(text)
        print("[+] writing to file\n")
        time.sleep(1)

    print("!! ---------------------- Scrape Complete ---------------------- !!\n")


if __name__ == '__main__':
    op = getArguments()
    pageCounter(op.url, op.pages)
