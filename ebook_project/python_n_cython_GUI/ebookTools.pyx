# This Python file uses the following encoding: utf-8

import io
import os

from natsort import natsorted
from zipfile import ZipFile
from datetime import date

class write_To_Html:
    def __init__(self):
        self.obj = self

    def open_txt(self, name, codec):
        return io.open(name, mode="r", encoding=codec)

    def ebook_divide(self, book, page, n_line, page_limit):
        # page   -> start with n page
        # n_line -> divide in every n lines
        # return:
        # divided page base on n_line and page_limit
        # stop -> True when reached to book's end
        # page -> current page number
        stop = None
        divided_page = {}
        while stop is None and page < page_limit:
            total_line = []
            i = 0
            while i < n_line:  # n lines for one page
                line = book.readline()
                if not line:  # reach to the end
                    stop = True
                    break
                if line != '\n':  # skip empty line may delete later for formatting
                    i += 1
                    total_line.append(line)
            divided_page[page] = total_line
            page += 1
            if stop:  #reach to the end
                break
        return divided_page, stop, page

    def msg_send(self, book, n_line, page_limit, rpc, save_path = "epub/chapters/", name = ""):
        scan_end = None  # reach to the book's ending
        responded_book_content = []
        current_page = 0  # page index
        try:
            path = os.getcwd()
            path = os.path.join(path,save_path) #new dir
            os.makedirs(path)
        except FileExistsError:
            print (".")
        else:
            print(".")

        while scan_end is None:
            divided_page, scan_end, current_page = self.ebook_divide(book, current_page, n_line,
                                                                     page_limit + current_page)
            self.decode_msg(rpc.call(divided_page),save_path,name)  # send a page with n lines
            # decode the received page in save to html
        return current_page

    def decode_msg(self, msg_list,save_path,name):
        # string_html = ["" for i in range(all_pages)]

        for pages in msg_list:
            for page_num, content in pages.items():
                #if there is old file, delete it
                old_HTML_file = open(save_path +"/"+name+ "page" +str(page_num)  + ".html", "w")
                old_HTML_file.write("")
                old_HTML_file.close()

                for paragraph in content:
                    new_HTML_file_binary = open(save_path +"/"+name+ "page"  +str(page_num)+ ".html", "ab")
                    new_HTML_file = open(save_path +"/"+name+ "page" +str(page_num)+ ".html", "a")
                    #append
                    self.write_to_html(new_HTML_file,new_HTML_file_binary, paragraph)
                    new_HTML_file.close()
                    new_HTML_file_binary.close()

    def write_to_html(self, new_HTML_file,new_HTML_file_binary, html_string):

        if html_string.strip()[0:1] == "<" and self.alphaChecker(html_string.strip()[1:2]):
            self.toHTML_string(new_HTML_file, html_string)
        else:
            self.toHTML_unicode(new_HTML_file_binary, html_string)

    def alphaChecker(self, this_char):
        check = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz/"
        if check.__contains__(this_char):
            return True
        return False

    def toHTML_unicode(self,file, html_string):
        file.write(html_string.encode('utf-8'))

    def toHTML_string(self,file, html_string):
        file.write(html_string)



# https://www.ibm.com/developerworks/xml/tutorials/x-epubtut/index.html
class createEPUB():
    def __init__(self):
        self.obj = self
        self.title = ""
        self.language = ""
        self.creator = ""
        self.publisher = ""
        self.description = ""
        self.date = ""
        self.identifier = ""

    def createContainer(self):
        save_path = "META-INF/"
        try:
            path = os.getcwd()
            path = os.path.join(path, save_path)  # new dir
            os.makedirs(path)
        except FileExistsError:
            print(".")
        else:
            print(".")

        newContainer = open(save_path + "container.xml", 'w');
        string = ("<?xml version='1.0' encoding='utf-8'?>\n" +
                  "<container version=\"1.0\" xmlns=\"urn:oasis:names:tc:opendocument:xmlns:container\">\n" +
                  "   <rootfiles>\n" +
                  "      <rootfile full-path=\"epub/content.opf\" media-type=\"application/oebps-package+xml\"/>\n" +
                  "   </rootfiles>\n"
                  + "</container>\n"
                  )
        newContainer.write(string)
        newContainer.close()

    def createmimetype(self):
        mimetype_string = "application/epub+zip"
        newmimetype = open("mimetype", 'wb')
        newmimetype.write(mimetype_string.encode('ascii'))
        newmimetype.close()

    def createOpt(self, page_num):
        save_path = "epub/"
        try:
            path = os.getcwd()
            path = os.path.join(path, save_path)  # new dir
            os.makedirs(path)
        except FileExistsError:
            print(".")
        else:
            print(".")

        oldOpt = open(save_path + "content.opf", "w")
        oldOpt.write("")
        oldOpt.close()  # clear the old opt file
        newOpt = open(save_path + "content.opf", "a")  # append mode
        newOpt.write("<?xml version=\"1.0\" encoding=\"utf-8\" standalone=\"yes\"?>\n")  # utf-8
        newOpt.write(
            "<package xmlns=\"http://www.idpf.org/2007/opf\" unique-identifier=\"BookId\" version=\"2.0\">\n")  #
        # package
        newOpt.write(
            "  <metadata xmlns:dc=\"http://purl.org/dc/elements/1.1/\" xmlns:opf=\"http://www.idpf.org/2007/opf\">\n")
        # metadata
        newOpt.write(
            "    <dc:identifier id=\"BookId\" opf:scheme=\"UUID\">urn:uuid:" + self.identifier + "</dc:identifier>\n")
        newOpt.write("    <dc:title>" + self.title + "</dc:title>\n")
        newOpt.write("    <dc:creator opf:role=\"aut\">" + self.creator + "</dc:creator>\n")
        newOpt.write("    <dc:language>" + self.language + "</dc:language>\n")
        today = date.today()
        day_format = today.strftime("%d-%m-%Y")
        newOpt.write("    <dc:date opf:event=\"modification\">" + day_format + "</dc:date>\n")
        newOpt.write("    <dc:publisher>" + self.publisher + "</dc:publisher>\n")
        newOpt.write("    <dc:description>" + self.description + "</dc:description>\n")
        newOpt.write("    <meta content=\"0.7.4\" name=\"Sigil version\" />\n")
        newOpt.write("  </metadata>\n")
        newOpt.write("  <manifest>\n")
        newOpt.write("<item href=\"toc.ncx\" id=\"ncx\" media-type=\"application/x-dtbncx+xml\" />\n")
        for i in range(page_num):
            file_string = "\"chapters/page" + str(i) + ".html\""
            page_string = "\"page" + str(i) + ".html\""
            newOpt.write("    <item href=" + file_string + " id=" + page_string + " media-type=\"text/html\"/>\n")
        newOpt.write("  </manifest>\n")

        newOpt.write("<spine toc=\"ncx\">\n")  # spine part
        for i in range(page_num):
            page_string = "\"page" + str(i) + ".html\"\n"
            newOpt.write("<itemref idref=" + page_string + " />\n")
        newOpt.write("</package>\n")
        newOpt.close()

    def createTOC(self, page_num):
        save_path = "epub/"
        oldToc = open(save_path + "toc.ncx", "w")
        oldToc.write("")
        oldToc.close()  # clear the old opt file
        newToc = open(save_path + "toc.ncx", "a")  # append mode
        newToc.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
        newToc.write("<!DOCTYPE ncx PUBLIC \"-//NISO//DTD ncx 2005-1//EN\"\n")
        newToc.write(" \"http://www.daisy.org/z3986/2005/ncx-2005-1.dtd\">\n")
        newToc.write("<ncx xmlns=\"http://www.daisy.org/z3986/2005/ncx/\" version=\"2005-1\">\n")
        newToc.write("  <head>")
        newToc.write("    <meta name=\"dtb:uid\" content=\"urn:uuid:" + self.identifier + " />\n")
        newToc.write("    <meta name=\"dtb:depth\" content=\"1\" />\n")
        newToc.write("    <meta name=\"dtb:totalPageCount\" content=\"0\" />\n")
        newToc.write("    <meta name=\"dtb:maxPageNumber\" content=\"0\" />\n")
        newToc.write("  </head>\n")
        newToc.write("  <docTitle>\n")
        newToc.write("    <text>" + self.title + "</text>\n")
        newToc.write("  </docTitle>\n")
        newToc.write("  <navMap>\n")
        for i in range(page_num):
            label_string = "page: " + str(i)
            file_string = "\"chapters/page" + str(i) + ".html\""
            newToc.write("<navPoint id=\"navPoint-" + str(-i) + "\" playOrder=\"" + str(i) + "\">\n")
            newToc.write("      <navLabel>\n")
            newToc.write("        <text>" + label_string + "</text\n>")
            newToc.write("</navLabel>\n")
            newToc.write("      <content src=" + file_string + " />\n")
            newToc.write("    </navPoint>\n")
        newToc.write("  </navMap>\n")
        newToc.write("</ncx>\n")

    def getFilePaths(self, epub_dir,meta_dir):
        paths = []  # loop through file list

        for root, dirs, files in os.walk(epub_dir, topdown=True):
            for filename in files:
                filepath = os.path.join(root, filename)
                paths.append(filepath)  # add epub to path

        for root, dirs, files in os.walk(meta_dir, topdown=True):
            for filename in files:
                filepath = os.path.join(root, filename)
                paths.append(filepath)  # add meta to path
        paths.append("mimetype")
        return paths

    def getHTMLPaths(self, html_dir):
        paths = []  # loop through file list

        for root, dirs, files in os.walk(html_dir, topdown=True):
            for filename in files:
                filepath = os.path.join(root, filename)
                paths.append(filepath)  # add epub to path
        return paths

    def toOneHTML(self,title,target_location):
        html_path = "epub/chapters"
        html_file_paths = self.getHTMLPaths(html_path)

        newHTMLfile = open(target_location+"/"+title+".html","w", encoding="utf-8")
        html_file_paths = self.naturalSort(html_file_paths)

        for files in html_file_paths:
            html = open(files,"r", encoding="utf-8")
            newHTMLfile.write(html.read())
            html.close()
            os.remove(files)
        newHTMLfile.close()
    #sort the file name only with numbers

    def naturalSort(self,file_name):
        return natsorted(file_name,key = lambda y:y.lower())


    def delete_Old_HTMl(self):
        html_path = "epub/chapters"
        html_file_paths = self.getHTMLPaths(html_path)


        for files in html_file_paths:
            os.remove(files)


    def zipFile(self, out_location):
        epub_path = "epub"
        meta_path = "META-INF"
        name = self.title
        # get all the file
        file_paths = self.getFilePaths(epub_path,meta_path)

        try:
            #path = os.getcwd()
            #path = os.path.join(path,out_location) #new dir
            os.makedirs(out_location)
        except FileExistsError:
            print (".")
        else:
            print("")
        # writing files to a zipfile
        with ZipFile(out_location+"/"+ name + ".epub", 'w') as zip:
            # writing each file one by one
            for file in file_paths:
                zip.write(file)

        print("finished convert to epub")
        self.delete_Old_HTMl()

    def setIdentifier(self, identifier):
        self.identifier = identifier

    def setTitle(self, title):
        self.title = title

    def setLanguage(self, lang):
        self.language = lang

    def setCreator(self, creator):
        self.creator = creator

    def setPublisher(self, publisher):
        self.publisher = publisher

    def setDescription(self, des):
        self.description = des













