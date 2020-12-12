# This Python file uses the following encoding: utf-8
import time

from ebookSend import RpcClient
from ebookTools import write_To_Html
from ebookTools import createEPUB
from getWebText import webGo
import os


class Program_With_Prefix:
    def __init__(self):
        self.file_location = ""
        self.obj = self
        self.target_location = ""
        self.convertMode = ""

        self.title = ""
        self.language = ""
        self.creator = ""
        self.publisher = ""
        self.description = ""
        self.identifier = ""

    def setMode(self):
        self.file_location = input("input the file location(.txt)")
        print(self.file_location)
        self.target_location = input("input the saving location")
        print(self.target_location)
        self.convertMode = input("input file format (HTML, EPUB)")
        print("start convert")
        self.startConvert()

    def setEPUBInfo(self):
        self.language = "test language"
        self.creator = "test creator"
        self.publisher = "test publisher"
        self.description = "test description"
        self.identifier = "test identifier"

    def setTitle(self, title):
        self.title = title

    def Run(self):
        project_location = os.getcwd()
        test_file_1 = "ebook_project/test_chinese_book.txt"
        test_file_1 = os.path.join(project_location, test_file_1)
        self.file_location = test_file_1
        self.target_location = os.path.join(project_location, "output")
        self.setTitle("test_chinese")
        tic = time.perf_counter()
        self.convertMode = "HTML"
        self.startConvert()
        toc = time.perf_counter()
        print(f"converted to HTML in {toc - tic:0.4f} seconds")

        tic = time.perf_counter()
        self.convertMode = "EPUB"
        self.startConvert()
        toc = time.perf_counter()
        print(f"converted to EPUB in {toc - tic:0.4f} seconds")

        test_file_0 = "ebook_project/test_english_book.txt"
        test_file_0 = os.path.join(project_location, test_file_0)
        self.file_location = test_file_0
        self.target_location = os.path.join(project_location, "output")
        self.setTitle("test_english")

        tic = time.perf_counter()
        self.convertMode = "HTML"
        self.startConvert()
        toc = time.perf_counter()
        print(f"converted to HTML in {toc - tic:0.4f} seconds")

        tic = time.perf_counter()
        self.convertMode = "EPUB"
        self.startConvert()
        toc = time.perf_counter()
        print(f"converted to EPUB in {toc - tic:0.4f} seconds")

        web = webGo()
        # web to txt
        tic = time.perf_counter()
        test_web = web.run("https://en.wikipedia.org/wiki/Python_(programming_language)", "python wiki", "temp")
        toc = time.perf_counter()
        print(f"load web content in {toc - tic:0.4f} seconds")

        self.file_location = os.path.join(project_location,test_web)
        self.target_location = os.path.join(project_location, "output")
        self.setTitle("test_web_python")
        tic = time.perf_counter()
        self.convertMode = "HTML"
        self.startConvert()
        toc = time.perf_counter()
        print(f"converted to HTML in {toc - tic:0.4f} seconds")
        tic = time.perf_counter()
        self.convertMode = "EPUB"
        self.startConvert()
        toc = time.perf_counter()
        print(f"converted to EPUB in {toc - tic:0.4f} seconds")


    def startConvert(self):
        # locations
        book_location = self.file_location
        target_location = self.target_location

        html_converter = write_To_Html()  # to html
        rpc = RpcClient()  # rpx server

        if self.convertMode == "HTML":  # HTML Mode
            print("converting to HTML")

            n_line = 99999
            page_limit = 9999  # only one html file will be created
            new_book = html_converter.open_txt(book_location, codec="utf-8")
            total_page = html_converter.msg_send(new_book, n_line, page_limit, rpc, save_path=target_location,
                                                 name=self.title)
            print("finish")
            new_book.close()
        elif self.convertMode == "EPUB":
            self.setEPUBInfo()
            n_line = 200
            page_limit = 20
            new_book = html_converter.open_txt(book_location, codec="utf-8")
            total_page = html_converter.msg_send(new_book, n_line, page_limit, rpc)
            new_book.close()
            self.createEPUBwithHTMLs(total_page, target_location)
            print("finish")

    def createEPUBwithHTMLs(self, page_num, out_location):
        epub_tools = createEPUB()
        epub_tools.createContainer()
        epub_tools.createmimetype()

        epub_tools.setTitle(self.title)
        epub_tools.setPublisher(self.publisher)
        epub_tools.setDescription(self.description)
        epub_tools.setIdentifier(self.identifier)
        epub_tools.setCreator(self.creator)
        epub_tools.setLanguage(self.language)
        epub_tools.createOpt(page_num)
        epub_tools.createTOC(page_num)
        epub_tools.zipFile(out_location)
        print("go")
