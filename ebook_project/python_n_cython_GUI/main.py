# This Python file uses the following encoding: utf-8

print("run main please")
from GUI import ProgramGUI
from textGUI import ProgramTextGUI
from getWebText import webGo

def main():


    print("ok 1")
    wiki = webGo()
    wiki.run("https://en.wikipedia.org/wiki/Python_(programming_language)","python","temp/")
    programGUI = ProgramGUI()
    print("ok 2")
    programGUI.run()
    print("ok 3")

main()
