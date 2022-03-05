import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as filedialog
from PyPDF2 import PdfFileReader, PdfFileWriter
import sys
import os

# root window
root = tk.Tk()
root.geometry('400x300')
root.wm_title('PDF Editor')

# create a notebook
notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)

def AddFile():
    ftypes = [('PDF files', '*.pdf'), ('All files', '*')]
    filename = filedialog.askopenfilename()
    print("You chose the following file: " + filename)
    pdf_splitter(filename)

# create frames
extract = ttk.Frame(notebook, width=400, height=280)
merge = ttk.Frame(notebook, width=400, height=280)
replace = ttk.Frame(notebook, width=400, height=280)
delete = ttk.Frame(notebook, width=400, height=280)
split = ttk.Frame(notebook, width=400, height=280)

extract.grid(column=0, row=0, padx=15, pady=15)
merge.grid(column=0, row=0, padx=15, pady=15)
replace.grid(column=0, row=0, padx=15, pady=15)
delete.grid(column=0, row=0, padx=15, pady=15)
split.grid(column=0, row=0, padx=15, pady=15)

# add frames to notebook

notebook.add(extract, text='Extract')
notebook.add(merge, text='Merge')
notebook.add(replace, text='Replace')
notebook.add(delete, text='Delete')
notebook.add(split, text='Split')

# add buttons to extract        
closeButton = ttk.Button(extract, text="Close", command = root.quit)
closeButton.grid(row=0, column=1, padx=(10,10), pady=(10, 10))
addFileButton = ttk.Button(extract, text="Add File", command = AddFile)
addFileButton.grid(row=0, column=0, padx=(10,10), pady=(10, 10))

##################
# Extractor
##################

def pdf_splitter(path):
    fname = os.path.splitext(os.path.basename(path))[0]
    directory = os.path.dirname(path) + '/'
    
    pdf = PdfFileReader(path)
    for page in range(pdf.getNumPages()):
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(page))
        output_filename = directory + '{}_page_{}.pdf'.format(
            fname, page+1)
        
        with open(output_filename, 'wb') as out:
            pdf_writer.write(out)
            
        print('Created: {}'.format(output_filename))
        
def singlepage(path, pagenumber):
    fname = os.path.splitext(os.path.basename(path))[0]
    directory = os.path.dirname(path) + '/'
    
    pdf = PdfFileReader(path)
    pdf_writer = PdfFileWriter()
    pdf_writer.addPage(pdf.getPage(pagenumber))
    output_filename = directory + '{}_page_{}.pdf'.format(fname, pagenumber+1)
    with open(output_filename, 'wb') as out:
        pdf_writer.write(out)
        
    print('Created: {}'.format(output_filename))        
    
###################    

menubar = tk.Menu(root)

root.config(menu=menubar)
file_menu = tk.Menu(menubar, tearoff=0)
# add a menu item to the menu
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=file_menu)

root.mainloop()