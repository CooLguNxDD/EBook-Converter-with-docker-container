
## CMPT 383 Project
##Project Summary:
## Overall goal of the project

The overall goal of this project is to convert some text to a viewable container.

This program can transfer:

Pure Text File: Files that contain pure text such as the ".txt" file.
Website: The program works well with a website that contains a lot of text such as Wikipedia.

Most of the epub converters (such as Calibre or some online ebook converter) needs a lot of time to convert the txt 
file to epub file. Therefore, implement this problem with mixed language should speed up text processing.

## Languages

This project is implementing with Python, Go, and C

Python is to focus on the interaction system such as the user interface.

Go is to convert some pure text into HTML format.

And C is to manage the Input and Output of the system.

## Communication

1. Remote procedure call: Since the Go language and handle the queue concurrently, the server will not have a huge
   delay when the main program keeps sending a message to the queue. (the program sending tons of paragraphs to the
   queue in this case)
   
2. Foreign Function Interface: This project using Cython to connect and compile Python and C code. It also
compiles some python code(.pyd in Window 10, .so in Linux) into C compiler to speed up the process.

## STEP and Feature

Initial Docker Compose and Containers of the project:
```sh
docker-compose build && docker-compose up
```
When the container is up, The program will convert three samples into both HTML and EPUB file to the
"out" folder

Sample 1: A Chinese Book with 557,221 words in txt file with some special characters.
Sample 2: An English Book with 319,718 words(about 1,500,000 characters) in txt file.
Sample 3: The Wikipedia page of Python language

The program also features a simple Graphic User Interface(which can't be opened in the container)

The files are located in
```sh
cd ebook_project/python_n_cython_GUI
```

For Window 10, just open run_python_setup.cmd
```sh
cmd /c run_python_setup.cmd
```

For Linux: (since I can't test the process in Linux, I don't know the actual process or command.)
1. install all the modulo
2. setup cython
3. run main.py
```sh
pip install pika==1.1.0
pip install pyzmq==19.0.1
pip install beautifulsoup4
pip install lxml
pip install natsort
pip install Cython==3.0a6
python setup.py build_ext --inplace
python main.py
```

The GUI will then shown up:(not yet tested in Linux)
1. User can select a text file by Navigating directory with "Browse" Button
2. User can input a website and then click "Web Mode Button" to convert a website
3. User can set the output format "To HTML" and "To EPUB".
4. Select Target(output) location
5. input some info for epub(you can leave them blank except "title" which represents the output file name)
6. start convert by clicking "Convert"

## Additions
The most important of this project is the processing speed.
The program can convert a very large text file in a short period.

The program divides the text file into different chunks (the chunks are limited by how many lines per page and how many
pages per message) and sends it to the Rabbitmq server. The concurrency of Go benefits
the procedure a lot because it doesn't need to process the text line by line.

After the main program receive the response, It converts the chunks into small HTML files and then combines
them into a zip file(EPUB) or a Full HTML file with Cython.

## performance
Tested Program:
Calibre, online txt to epub: https://ebook.online-convert.com/convert-to-epub

In the Chinese sample, The program only takes 1.4771 seconds to convert to HTMl and 1.4921 seconds to EPUB.
While the program Calibre takes around 20s, and online converter takes around 25s

In the English sample, The program only takes 1.0229 seconds to convert to HTMl and 1.1032 seconds to EPUB.
While the program Calibre takes around 18s, and online converter takes around 22s
