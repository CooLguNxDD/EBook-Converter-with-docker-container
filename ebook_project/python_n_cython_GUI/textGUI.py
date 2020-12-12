# This Python file uses the following encoding: utf-8

from ebookSendLocal import RpcClient
from ebookTools import write_To_Html
from ebookTools import createEPUB

class ProgramTextGUI:
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
        self.title = input("set title")
        self.language = input("set language")
        self.creator = input("set creator")
        self.publisher = input("set publisher")
        self.description = input("set description")
        self.identifier = input("set identifier")



    def startConvert(self):
        while (self.convertMode != "HTML" and self.convertMode!="EPUB") or self.file_location == "" or self.target_location=="":
            print("empty location or wrong format")
            self.setMode()
        #locations
        book_location = self.file_location
        target_location = self.target_location

        html_converter = write_To_Html() # to html
        rpc = RpcClient()  # rpx server

        if self.convertMode == "HTML": #HTML Mode
            n_line = 99999
            page_limit = 9999  #only one html file will be created
            new_book = html_converter.open_txt(book_location, codec="utf-8")
            total_page = html_converter.msg_send(new_book, n_line, page_limit, rpc, save_path = target_location)
            print("finish")
            new_book.close()
        elif self.convertMode == "EPUB":
            self.setEPUBInfo()
            n_line = 200
            page_limit = 20
            new_book = html_converter.open_txt(book_location, codec="utf-8")
            total_page = html_converter.msg_send(new_book, n_line, page_limit, rpc)
            new_book.close()
            self.createEPUBwithHTMLs(total_page,target_location)
            print("finish")


    def createEPUBwithHTMLs(self,page_num,out_location):
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


