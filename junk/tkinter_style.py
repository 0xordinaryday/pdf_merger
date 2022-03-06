#!/usr/bin/env python3

"""
ZetCode Tkinter tutorial

In this script, we use the pack manager
to position two buttons in the
bottom-right corner of the window.

Author: Jan Bodnar
Website: www.zetcode.com
"""

from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Button, Style
from PIL import Image, ImageTk
import glob, os
import pypdfium2 as pdfium
from pathlib import Path

def donothing():
   filewin = Toplevel(root)
   button = Button(filewin, text="Do nothing button")
   button.pack()

root = Tk()
photos = []
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=donothing)
filemenu.add_command(label="Open", command=donothing)
filemenu.add_command(label="Save", command=donothing)
filemenu.add_command(label="Save as...", command=donothing)
filemenu.add_command(label="Close", command=donothing)

filemenu.add_separator()

filemenu.add_command(label="Exit", command=root.quit)

class PDFMerger(Frame):

    def __init__(self):
        super().__init__()
        self.initUI()
        
    def AddFile(self):
        ftypes = [('PDF files', '*.pdf'), ('All files', '*')]
        thumbnaildir = makedir()
        size = 128, 128
        # dlg = filedialog.Open(self, filetypes = ftypes)
        # fl = dlg.show()
        filename = filedialog.askopenfilename()
        print("You chose the following file: " + filename)
        for image, suffix in pdfium.render_pdf(filename):
            image.thumbnail(size)
            image.save(f'{thumbnaildir}/thumb_{suffix}.jpg')
        redraw()

    def initUI(self):
        self.master.title("Buttons")
        self.style = Style()
        self.style.theme_use("default")

        frame = Frame(self, relief=RAISED, borderwidth=1)
        frame.pack(fill=BOTH, expand=True)

        self.pack(fill=BOTH, expand=True)

        closeButton = Button(self, text="Close")
        closeButton.pack(side=RIGHT, padx=5, pady=5)
        addFileButton = Button(self, text="Add File", command = self.AddFile)
        addFileButton.pack(side=RIGHT)

def makedir():
    # Directory will hold thumbnails generated from loaded PDFs
    directory = "thumbnails"

    # Parent Directory path
    parent_dir = "C:/Temp"
    
    # Path
    path = os.path.join(parent_dir, directory)
    
    # Create the directory
    try:
        os.makedirs(path, exist_ok = True)
        print("Directory '%s' created successfully" % directory)
    except OSError as error:
        print("Directory '%s' can not be created" % directory)          
    return path 
       
def displayImg(img):
    image = Image.open(img)
    photo = ImageTk.PhotoImage(image)
    photos.append(photo) #keep references!
    label = Label(image=photo)
    label.image = photo
    label.pack()

def redraw():
    print("called")
    for myfile in Path("C:/Temp/thumbnails").glob("**/*"):
        if myfile.is_file():
            displayImg(myfile)
            print(myfile)       

def onClose():
    for path in Path("C:/Temp/thumbnails").glob("**/*"):
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            rmtree(path)
    root.destroy()

def main():

    # root = tkinter.Tk()
    root.config(menu=menubar)
    root.geometry("300x200+300+300")
    app = PDFMerger()
    root.wm_protocol("WM_DELETE_WINDOW", onClose)
    root.mainloop()


if __name__ == '__main__':
    main()