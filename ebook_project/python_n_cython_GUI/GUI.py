

from tkinter import *
import tkinter as tk
import tkinter.filedialog as tk_dialog
from ebookSendLocal import RpcClient
from ebookTools import write_To_Html
from ebookTools import createEPUB
from getWebText import webGo
import os


class ProgramGUI:
    def __init__(self):
        self.file_location = ""
        self.obj = self
        self.target_location = ""
        self.convertMode = ""
        self.fromWhere = ""

    def run(self):
        self.main_win = Tk()  # main window is created == master
        self.main_win.geometry("800x600+100+100")  # window size

        self.file_location_text = tk.StringVar()
        self.file_location_text.set("Select a file or Input a Website with Web Mode")


        self.convert_to_text = tk.StringVar()
        self.convert_to_text.set("Converting to: ")

        self.target_location_text = tk.StringVar()
        self.target_location_text.set("Target Location:")

        self.start_convert_text = tk.StringVar()
        self.start_convert_text.set("start!!!")

        self.browse_file(self.main_win, 20, 20)
        self.convert_Method_Frame(self.main_win, 20, 100)
        self.browse_Target_Location(self.main_win, 20, 200)
        self.set_EPUB_Element(self.main_win, 20, 300)
        self.convertButtonFrame(self.main_win, 20, 450)

        self.main_win.mainloop()
        # main_win.player_turn, main_win.player_turn_button = turn_button(main_win, 220, 20, 0)
        # main_win.ai_turn, main_win.ai_turn_button = turn_button(main_win, 390, 20, 1)

    def browse_file(self, main_win, placement_x, placement_y):
        self.topframe = Frame(main_win, width=800, height=100)
        self.topframe.place(x=placement_x, y=placement_y)  # position

        self.button = Button(self.topframe, text="Browse", bg="white", fg="black",
                             height=1, width=10,
                             font=("Arial", 16), command=lambda: self.browse_window())

        self.file_location_label = Label(self.topframe, textvariable=self.file_location_text,
                                         font=("Arial", 10))

        self.web_button = Button(self.topframe, text="Web Mode", bg="white", fg="black",
                                 height=1, width=10,
                                 font=("Arial", 16), command=lambda: self.browse_web())

        self.entry_web = Entry(self.topframe, width=50, font=("Arial", 12))
        self.entry_web.insert(END, "")
        self.file_location_label.place(x=300, y=15)

        self.button.place(x=3, y=5)
        self.web_button.place(x=150,y=5)
        self.entry_web.place(x=300,y = 50)

    def browse_window(self):
        curr_dir = os.getcwd()
        self.file_location = tk_dialog.askopenfilename(title="Select file", initialdir=curr_dir,
                                                       filetypes=(("txt files", "*.txt"), ("all files", "*.*")))
        print(self.file_location)
        self.fromWhere = "file"
        self.file_location_text.set("Selected: " + self.file_location)
    def browse_web(self):
        try:
            web = webGo()
            curr_dir = os.getcwd()
            self.file_location = os.path.join(curr_dir,web.run(self.entry_web.get(),"web","temp"))
            print(self.file_location)
            self.fromWhere = "web"
            self.file_location_text.set("Selected: " + self.file_location)
        except Exception as e:
            self.file_location_text.set("error: "+str(e))
            self.fromWhere = ""


    def convert_Method_Frame(self, main_win, placement_x, placement_y):
        self.convert_Method_F = Frame(main_win, width=800, height=100)
        self.convert_Method_F.place(x=placement_x, y=placement_y)  # position

        self.to_HTML_Button = Button(self.convert_Method_F, text="To HTML", bg="white", fg="black",
                                     height=1, width=10,
                                     font=("Arial", 16), command=lambda: self.convert_Method_HTML())
        self.to_EPUB_Button = Button(self.convert_Method_F, text="To EPUB", bg="white", fg="black",
                                     height=1, width=10,
                                     font=("Arial", 16), command=lambda: self.convert_Method_EPUB())

        self.convert_label = Label(self.convert_Method_F, textvariable=self.convert_to_text, font=("Arial", 10))

        self.to_HTML_Button.place(x=3, y=5)
        self.to_EPUB_Button.place(x=150, y=5)
        self.convert_label.place(x=3, y=60)

    def convert_Method_HTML(self):
        self.convertMode = "HTML"
        self.convert_to_text.set("Converting to: " + self.convertMode)

    def convert_Method_EPUB(self):
        self.convertMode = "EPUB"
        self.convert_to_text.set("Converting to: " + self.convertMode)

    def browse_Target_Location(self, main_win, placement_x, placement_y):
        self.target_location_frame = Frame(main_win, width=800, height=100)
        self.target_location_frame.place(x=placement_x, y=placement_y)  # position

        self.browse_target_button = Button(self.target_location_frame, text="Target", bg="white", fg="black",
                                           height=1, width=10,
                                           font=("Arial", 16), command=lambda: self.browse_target_window())

        self.target_location_label = Label(self.target_location_frame, textvariable=self.target_location_text,
                                           font=("Arial", 10))

        self.browse_target_button.place(x=3, y=25)
        self.target_location_label.place(x=3, y=5)

    def browse_target_window(self):
        curr_dir = os.getcwd()
        self.target_location = tk_dialog.askdirectory(title="Select Target Directory", initialdir=curr_dir) + "/"
        print(self.target_location)
        self.target_location_text.set("Target: " + self.target_location)

    def set_EPUB_Element(self, main_win, placement_x, placement_y):

        self.epub_element_frame = Frame(main_win, width=800, height=200)
        self.epub_element_frame.place(x=placement_x, y=placement_y)  # position

        self.epub_label = Label(self.epub_element_frame, text="Input Epub Elements: ", font=("Arial", 12))
        self.epub_label.place(x=3, y=5)

        self.entry_title_label = Label(self.epub_element_frame, text="Title: ", font=("Arial", 12))
        self.entry_title = Entry(self.epub_element_frame, width=30, font=("Arial", 12))
        self.entry_title.insert(END, "default")
        self.entry_title_label.place(x=3, y=40)
        self.entry_title.place(x=73, y=40)

        self.entry_creator_label = Label(self.epub_element_frame, text="Creator: ", font=("Arial", 12))
        self.entry_creator = Entry(self.epub_element_frame, width=30, font=("Arial", 12))
        self.entry_creator.insert(END, "")
        self.entry_creator_label.place(x=143, y=40)
        self.entry_creator.place(x=213, y=40)

        self.entry_publisher_label = Label(self.epub_element_frame, text="Publisher: ", font=("Arial", 12))
        self.entry_publisher = Entry(self.epub_element_frame, width=10, font=("Arial", 12))
        self.entry_publisher.insert(END, "")
        self.entry_publisher_label.place(x=283, y=40)
        self.entry_publisher.place(x=363, y=40)

        self.entry_identifier_label = Label(self.epub_element_frame, text="Identifier: ", font=("Arial", 12))
        self.entry_identifier = Entry(self.epub_element_frame, width=23, font=("Arial", 12))
        self.entry_identifier.insert(END, "")
        self.entry_identifier_label.place(x=453, y=40)
        self.entry_identifier.place(x=533, y=40)

        self.entry_language_label = Label(self.epub_element_frame, text="Language: ", font=("Arial", 12))
        self.entry_language = Entry(self.epub_element_frame, width=30, font=("Arial", 12))
        self.entry_language.insert(END, "")
        self.entry_language_label.place(x=3, y=80)
        self.entry_language.place(x=93, y=80)

        self.entry_description_label = Label(self.epub_element_frame, text="Description: ", font=("Arial", 12))
        self.entry_description = Entry(self.epub_element_frame, width=55, font=("Arial", 12))
        self.entry_description.insert(END, "")
        self.entry_description_label.place(x=153, y=80)
        self.entry_description.place(x=253, y=80)

    def convertButtonFrame(self, main_win, placement_x, placement_y):
        self.convert_Button_F = Frame(main_win, width=500, height=150)
        self.convert_Button_F.place(x=placement_x, y=placement_y)  # position

        self.start_convert_Button = Button(self.convert_Button_F, text="Convert", bg="white", fg="black",
                                           height=1, width=10,
                                           font=("Arial", 16), command=lambda: self.startConvert())

        self.start_convert_label = Label(self.convert_Button_F, textvariable=self.start_convert_text,
                                         font=("Arial", 12))

        self.start_convert_Button.place(x=3, y=5)
        self.start_convert_label.place(x=10, y=60)

    def startConvert(self):
        n_line = 0  # limit to n line per msg
        page_limit = 0  # limit to n page per msg
        if self.convertMode != "" and self.file_location != "" and self.target_location != "":
            # locations
            book_location = self.file_location
            target_location = self.target_location

            html_converter = write_To_Html()  # to html
            rpc = RpcClient()  # rpx server

            if self.convertMode == "HTML":  # HTML Mode
                epub_tools = createEPUB()
                print("html")
                n_line = 25
                page_limit = 5
                new_book = html_converter.open_txt(book_location, codec="utf-8")
                total_page = html_converter.msg_send(new_book, n_line, page_limit, rpc)
                epub_tools.toOneHTML(str(self.entry_title.get()),target_location)
                print("finish")
                self.start_convert_text.set("finished")
                new_book.close()
            elif self.convertMode == "EPUB":
                print("epub")
                n_line = 25
                page_limit = 5
                new_book = html_converter.open_txt(book_location, codec="utf-8")
                print("to html")
                total_page = html_converter.msg_send(new_book, n_line, page_limit, rpc)
                new_book.close()
                print("creating epub")
                self.createEPUBwithHTMLs(total_page, target_location)
                print("finish")
                self.start_convert_text.set("finished")
        else:
            self.start_convert_text.set("Info missing, please select all Mode/File/Target location")

    def createEPUBwithHTMLs(self, page_num, out_location):
        epub_tools = createEPUB()
        epub_tools.createContainer()
        epub_tools.createmimetype()

        epub_tools.setTitle(self.entry_title.get())
        epub_tools.setPublisher(self.entry_publisher.get())
        epub_tools.setDescription(self.entry_description.get())
        epub_tools.setIdentifier(self.entry_identifier.get())
        epub_tools.setCreator(self.entry_creator.get())
        epub_tools.setLanguage(self.entry_language.get())
        epub_tools.createOpt(page_num)
        epub_tools.createTOC(page_num)
        epub_tools.zipFile(out_location)
        print("go")
