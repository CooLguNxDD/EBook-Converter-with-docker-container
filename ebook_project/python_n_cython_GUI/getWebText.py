from urllib.request import urlopen
from bs4 import BeautifulSoup
import os
import re


class webGo():
    def __init__(self):
        self.obj = self
        self.title = ""
        self.save_location = ""

    def openWebPage(self, URL):
        new_source = urlopen(URL)
        new_soup = BeautifulSoup(new_source, "lxml")
        return new_soup

    def WebPageFormatter(self, soup):
        new_text = ""
        for all_para in soup.find_all(['h1', 'h2', 'p']):  # find all paragraph
            new_text += all_para.text+'\n'
        return new_text

    def reform(self, text):
        return re.sub(r'==.*?==+', '', text)

    def toTxt(self, in_text):

        try:
            path = os.getcwd()
            path = os.path.join(path, self.save_location)  # new dir
            os.makedirs(path)
        except FileExistsError:
            print(".")
        else:
            print(".")

        file = open(self.save_location + "/" + self.title + ".txt", "wb")
        file.write(in_text.encode(encoding="utf-8"))
        file.close()

    def run(self, URL, title, save):
        soup = self.openWebPage(URL)
        text = self.WebPageFormatter(soup)
        self.title = title
        self.save_location = save
        self.toTxt(text)
        return self.save_location + "/" + self.title + ".txt"
