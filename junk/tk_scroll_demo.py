import tkinter
from tkinter import filedialog
from tkinter.ttk import Button, Style
from PIL import Image, ImageTk
import glob, os
import pypdfium2 as pdfium
from pathlib import Path
import ScrollFrame

# ********************************
# Example usage of the above class
# ********************************

photos = []

class PDFMerger(tkinter.Frame):
    def __init__(self, root):

        tkinter.Frame.__init__(self, root)
        self.scrollFrame = ScrollFrame.ScrollFrame(self) # add a new scrollable frame; definition is in ScrollFrame.py
  
    def printMsg(self, msg):
        print(msg)
        
    def AddFile(self):
        ftypes = [('PDF files', '*.pdf'), ('All files', '*')]
        thumbnaildir = self.makedir()
        size = 128, 128
        # dlg = filedialog.Open(self, filetypes = ftypes)
        # fl = dlg.show()
        filename = filedialog.askopenfilename()
        print("You chose the following file: " + filename)
        for image, suffix in pdfium.render_pdf(filename):
            image.thumbnail(size)
            # self.displayImg(image)
            image.save(f'{thumbnaildir}/thumb_{suffix}.jpg')
        self.redraw()
            
    def makedir(self):
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
        
    def displayImg(self, img):
        image = Image.open(img)
        photo = ImageTk.PhotoImage(image)
        photos.append(photo) #keep references!
        label = tkinter.Label(image=photo)
        label.image = photo
        # label.pack()
    
    def redraw(self):
        for myfile in Path("C:/Temp/thumbnails").glob("**/*"):
            if myfile.is_file():
                image = Image.open(myfile)
                photo = ImageTk.PhotoImage(image)
                photos.append(photo) #keep references!
                label = tkinter.Label(image=photo)
                label.image = photo
                tkinter.Button(self.scrollFrame.viewPort, text=label, image=myfile)
                print(myfile)     
        # Now add some controls to the scrollframe. 
        # NOTE: the child controls are added to the view port (scrollFrame.viewPort, NOT scrollframe itself)
            #for myfile in Path("C:/Temp/thumbnails").glob("**/*"):
                # a = row
                # tkinter.Label(self.scrollFrame.viewPort, text="%s" % row, width=3, borderwidth="1", relief="solid").grid(row=row, column=0)
                # t="this is the second column for row %s" %row
                #tkinter.Button(self.scrollFrame.viewPort, text='t', image=myfile) # , command=lambda x=a: self.printMsg("Hello " + str(x))).grid(row=row, column=1)
    
            # when packing the scrollframe, we pack scrollFrame itself (NOT the viewPort)
        self.scrollFrame.pack(side="top", fill="both", expand=True)
            

def onClose():
    for path in Path("C:/Temp/thumbnails").glob("**/*"):
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            rmtree(path)
    root.destroy()

def main():
    # root.geometry("300x200+300+300")
 
    # root window
    root = tkinter.Tk()
    app = PDFMerger(root)
    root.title('PDFMerger')
    root.wm_protocol("WM_DELETE_WINDOW", onClose) 
    
    menubar = tkinter.Menu(root)
    root.config(menu=menubar)
    
    file_menu = tkinter.Menu(menubar, tearoff=0)
    
    # add a menu item to the menu
    file_menu.add_command(label="Add File", command=app.AddFile)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)
    
    menubar.add_cascade(label="File", menu=file_menu)
    
    PDFmerge = PDFMerger(root).pack(side="top", fill="both", expand=True)
    root.mainloop()    

if __name__ == "__main__":
    main()
    
  