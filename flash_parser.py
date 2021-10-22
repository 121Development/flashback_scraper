import urllib.request
import bs4 as bs
import time
import os
import re
import csv
import optparse
import time
from datetime import datetime


__location__ = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))
alphabet = re.compile('[^a-zA-ZåäöÅÄÖ \.]')

author_posts_dictionary = {}
one_author_posts = []


def getArguments():

    parser = optparse.OptionParser()

    parser.add_option("-u", "--url", dest="url",
                      help="URL to Flashback thread, example: https://www.flashback.org/t3360954")
    parser.add_option("-p", "--pages", dest="pages",
                      help="Pages for Flashback thread you whish to parse")
    parser.add_option("-s", "--user", dest="user",
                      help="If you want to scrape posts from one user only, specify user name (case sensitive)")
    (options, arguments) = parser.parse_args()
    if not options.url:
        parser.error("[-] Please specify an URL --help for info.")
    elif not options.pages:
        parser.error(
            "[-] Please specify number of pages of thread--help for info.")
    return options


def threadParser(url, page):

    print("---------------------- Parsing Page " +
          str(page) + "----------------------")
    pageAuthorlist = []
    pagePostlist = []
    url_contents = urllib.request.urlopen(url + "p" + str(page)).read()
    soup = bs.BeautifulSoup(url_contents, "html.parser")

    for div in soup.find_all("div", {'class': "post-bbcode-quote-wrapper"}):
        div.decompose()
    for div in soup.find_all('a'):
        div.decompose()
    for div in soup.find_all('img'):
        div.decompose()

    usernames = soup.findAll("div", {"class": "dropdown"})

    for username in usernames:
        pageAuthorlist.append(" ".join(username.get_text().split()))

    div = soup.findAll("div", {"class": "post_message"})
    for post in div:
        tmp = str(post)
        ind1 = tmp.find('\n')
        ind2 = tmp.rfind('\n')
        tmp = tmp[ind1 + 1:ind2].replace("<br/>",
                                         " ").replace("<i>", " ").replace("</i>", " ")

        pagePostlist.append(" ".join(alphabet.sub(' ', tmp).split()))

    print("[i] Authors: " + str(pageAuthorlist) + "\n")
    return pageAuthorlist, pagePostlist


def addAuthorPostToDict(author, post):
    if author in author_posts_dictionary.keys():
        print('[i] Author is already in dict, appending post to author')
        tmpPost = author_posts_dictionary.pop(author)
        author_posts_dictionary.update({author: tmpPost + ' | ' + post})

    else:
        print('[i] Updating dict with new author and post')
        author_posts_dictionary.update({author: post})


def appendPostToOneAuthor(post):
    one_author_posts.append(post)


def pageCounter(url, numberofpages, user):
    print("inside page counter")

    if user is None:
        for page in range(1, numberofpages):
            pageAuthorlist, pagePostlist = threadParser(url, page)
            x = 0
            for author in pageAuthorlist:
                addAuthorPostToDict(author, pagePostlist[x])
                x = x + 1
            time.sleep(2)

    else:
        for page in range(1, numberofpages):
            pageAuthorlist, pagePostlist = threadParser(url, page)
            x = 0
            for author in pageAuthorlist:
                if author == user:
                    appendPostToOneAuthor(pagePostlist[x])
                x = x + 1
            time.sleep(2)

    print("!! ---------------------- Scrape Complete ---------------------- !!\n")
    if user is None:
        print("[i] Scraped posts from " +
              str(len(author_posts_dictionary)) + " authors\n")
    else:
        print("[i] Scraped " + str(len(one_author_posts)) +
              " posts from user " + user + "\n")


def writeDictToCSV(author_post_dict, url):
    date = datetime.today().strftime('%Y-%m-%d')
    file_title = 'flashback_thread_' + url[-8:-1] + '_parsed_' + date + '.csv'

    print("[-] Writing File...")
    f = open(os.path.join(__location__, file_title),
             "w", encoding="utf-8")

    writer = csv.writer(f)
    for key, value in author_post_dict.items():
        writer.writerow([key, value])
    print("[-] File Complete")


def writePostListForOneAuthorsToCSV(one_author_posts, url, user):
    date = datetime.today().strftime('%Y-%m-%d')
    file_title = 'flashback_thread_' + \
        url[-8:-1] + '_user_' + user + '_parsed_' + date + '.csv'

    print("[-] Writing File...")
    f = open(os.path.join(__location__, file_title),
             "w", encoding="utf-8")

    writer = csv.writer(f)
    writer.writerow([user])
    for post in one_author_posts:
        writer.writerow([post])
    print("[-] File Complete")


if __name__ == '__main__':
    op = getArguments()
    global user
    user = None
    if op.user is not None:
        user = op.user
    pageCounter(op.url, int(op.pages), op.user)
    if user is None:
        writeDictToCSV(author_posts_dictionary, op.url)
    else:
        writePostListForOneAuthorsToCSV(one_author_posts, op.url, op.user)
