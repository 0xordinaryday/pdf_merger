import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as filedialog
import PyPDF2
import sys
import os
import re

# root window
root = tk.Tk()
root.geometry('500x300')
root.wm_title('PDF Editor')

# create a notebook
notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)

##############################################
# Extract functions

def AddFileForExtract():
    ftypes = [('PDF files', '*.pdf'), ('All files', '*')]
    filename = filedialog.askopenfilename() 
    # TODO
    ExtractSetText(filename)
    
def CountPages(filepath):
    # must be a PDF
    pdf = PyPDF2.PdfFileReader(filepath)
    return pdf.getNumPages()
    
def ExtractSetText(filepath):
    filename, extension = os.path.splitext(filepath)
    if extension.lower() != '.pdf':
        var.set("File is: {} \nFile is not a PDF, cannot extract.".format(filepath))
    elif CountPages(filepath) == 1:
        var.set("File is: {} \nThis only has one page already.".format(filepath))
    else: 
        var.set("File is: {} \nFile has {} pages, which page should I extract?".format(filepath, CountPages(filepath)))
        SetPages(CountPages(filepath))
        
def SetPages(numberOfPages):
    vlist = [] # reset if not already
    for i in range(numberOfPages):
        vlist.append(str(i+1))
    extractCombo['values'] = vlist
    
def ClearFilesFromExtract():
    vlist = []
    extractCombo['values'] = vlist
    var.set("Choose a file")
    extractFilePath = ''
    
def DoExtraction():
    textbox_text = var.get()
    pattern = "File is: (.*?)\n"
    filepath = re.search(pattern, textbox_text).group(1)
    # print(filepath)
    pdf = PyPDF2.PdfFileReader(filepath)
    pdf_writer = PyPDF2.PdfFileWriter()
    pagenumber = int(extractCombo.get())
    pdf_writer.addPage(pdf.getPage(pagenumber -1)) # zero indexed
    
    save_filename = filedialog.asksaveasfilename() 
    with open(save_filename, 'wb') as out:
        pdf_writer.write(out)
    print('Created: {}'.format(save_filename)) 
    tk.messagebox.showinfo(title='Alert', message='Extraction Complete!')
    

##############################################
# Merge functions

filename_list = []

def AddFile():
    ftypes = [('PDF files', '*.pdf'), ('All files', '*')]
    filenames = filedialog.askopenfilenames() # returns a tuple even if only one entry selected
    for filename in filenames:
        # display_name = os.path.split(filename)[1]
        if filename not in filename_list:
            filename_list.append(filename)
    # print(filename_list)
    add_files(filename_list)
    # pdf_splitter(filename)
    
def add_files(filelist):
    # Loop thru to fill listbox
    for filename in filelist:
        if filename not in getContents():
            merge_filename_box.insert(tk.END, filename)
        
def getContents():
    # get current contents of listbox
    listsize = merge_filename_box.size()
    print(merge_filename_box.get(0,listsize-1))
    return merge_filename_box.get(0,listsize-1)        
        
def ClearFiles():
    # Empty listbox
    listsize = merge_filename_box.size()
    merge_filename_box.delete(0,listsize-1)  
    
def DoMerger():
    save_filename = filedialog.asksaveasfilename() 
    files = getContents()
    mergeFile = PyPDF2.PdfFileMerger()
    for _pdf in files:
        mergeFile.append(PyPDF2.PdfFileReader(_pdf, 'rb'))
    mergeFile.write(save_filename)
    tk.messagebox.showinfo(title='Alert', message='Merge Complete!')  


# End merge functions
############################################## 
        
class DragDropListbox(tk.Listbox):
    """ A Tkinter listbox with drag'n'drop reordering of entries. """
    # https://stackoverflow.com/questions/66219059/drag-drop-list-in-tkinter
    def __init__(self, master, **kw):
        kw['selectmode'] = tk.SINGLE
        tk.Listbox.__init__(self, master, kw)
        self.bind('<Button-1>', self.setCurrent)
        self.bind('<B1-Motion>', self.shiftSelection)
        self.curIndex = None
        # super().__init__('Listbox')

    def setCurrent(self, event):
        self.curIndex = self.nearest(event.y)

    def shiftSelection(self, event):
        i = self.nearest(event.y)
        if i < self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i+1, x)
            self.curIndex = i
        elif i > self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i-1, x)
            self.curIndex = i    

# create frames
extract = ttk.Frame(notebook, width=500, height=350)
merge = ttk.Frame(notebook, width=500, height=350)
replace = ttk.Frame(notebook, width=500, height=350)
delete = ttk.Frame(notebook, width=500, height=350)
split = ttk.Frame(notebook, width=500, height=350)

extract.grid(column=0, row=0, padx=15, pady=15)
merge.grid(column=0, row=0, padx=15, pady=15)
replace.grid(column=0, row=0, padx=15, pady=15)
delete.grid(column=0, row=0, padx=15, pady=15)
split.grid(column=0, row=0, padx=15, pady=15)

# extract.rowconfigure(1, {'minsize': 300})
extract.columnconfigure(1, {'minsize': 300})

# add frames to notebook
notebook.add(extract, text='Extract')
notebook.add(merge, text='Merge')
notebook.add(replace, text='Replace')
notebook.add(delete, text='Delete')
notebook.add(split, text='Split')

##############################################
# Merge GUI elements
       
closeButton = ttk.Button(merge, text="Clear", command = ClearFiles)
closeButton.grid(row=0, column=1, padx=(10,10), pady=(10, 10))
addFileButton = ttk.Button(merge, text="Add File", command = AddFile)
addFileButton.grid(row=0, column=0, padx=(10,10), pady=(10, 10))
mergeButton = ttk.Button(merge, text="Merge Files", command = DoMerger)
mergeButton.grid(row=3, column=0, padx=(10,10), pady=(10, 10))

# add filelist to merge
merge_filename_box = DragDropListbox(merge, width=80)
merge_filename_box.grid(row=2, column=0, columnspan=2)

# End Merge GUI elements
##############################################

##############################################
# Extract GUI elements

closeButton = ttk.Button(extract, text="Clear", command = ClearFilesFromExtract) # ClearFilesFromExtract
closeButton.grid(row=0, column=1, padx=(10,10), pady=(10, 10), sticky = tk.W)   
addFileButton = ttk.Button(extract, text="Add File", command = AddFileForExtract) # AddFileForExtract
addFileButton.grid(row=0, column=0, padx=(10,10), pady=(10, 10), sticky = tk.W)   
mergeButton = ttk.Button(extract, text="Extract", command = DoExtraction) # DoExtraction
mergeButton.grid(row=4, column=0, padx=(10,10), pady=(10, 10), sticky = tk.W)   

# Add label to extract
var = tk.StringVar()
var.set("Choose a file")
label = tk.Label(extract, textvariable = var, justify=tk.LEFT, anchor="w")
label.grid(row=2, column=0, padx=(10,10), pady=(10, 10), columnspan=2, sticky = tk.W+tk.E)

# Add combobox for pagenumbers to extract
vlist = []
extractCombo = ttk.Combobox(extract, values = vlist)
extractCombo.set("Choose a page")
extractCombo.grid(row=3, column=0, padx=(10,10), pady=(10, 10), sticky = tk.W+tk.E)

# End Extract GUI elements
##############################################

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
        
       
    
###################    

menubar = tk.Menu(root)

root.config(menu=menubar)
file_menu = tk.Menu(menubar, tearoff=0)
# add a menu item to the menu
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=file_menu)

root.mainloop()