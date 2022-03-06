import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as filedialog
import PyPDF2
import sys
import os
import re

# root window
root = tk.Tk()
root.geometry('500x400')
root.wm_title('PDF Editor')

# Create a style
style = ttk.Style(root)
# Set the theme with the theme_use method
style.theme_use('winnative')
# alt, clam, classic, default, vista, winnative, xpnative
# winnative, clam and alt are ok

# create a notebook
notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)

##############################################
# Shared functions

def AddFileShared(flag):
    # shared with explode, pass flag to EESetText
    ftypes = [('PDF files', '*.pdf'), ('All files', '*')]
    filename = filedialog.askopenfilename() 
    if flag < 3:
        EESetText(filename, flag)
    if flag == 3:
        SetDeleteText(filename)
    
def CountPages(filepath):
    # must be a PDF
    pdf = PyPDF2.PdfFileReader(filepath)
    return pdf.getNumPages()
    
def SetPages(numberOfPages, comboBox):
    pagelist = [] # reset if not already
    for i in range(numberOfPages):
        pagelist.append(str(i+1))
    comboBox['values'] = pagelist
    
def ClearFilesFromExtract(comboBox, labelName):
    comboBox['values'] = []
    labelName.set("Choose a file")
    # extractFilePath = ''    
    
# End shared functions
##############################################
    
##############################################
# Extract functions
    
def EESetText(filepath, flag):
    # shared with explode, flag controls behaviour
    filename, extension = os.path.splitext(filepath)
    var_to_set = ''
    which_function = ''
    if flag == 1:
        var_to_set, which_function = extract_label, 'extract'
    elif flag == 2:
        var_to_set, which_function = explode_label, 'explode'
    if extension.lower() != '.pdf':
        var_to_set.set("File is: {} \nFile is not a PDF, cannot {}.".format(filepath, which_function))
    elif CountPages(filepath) == 1:
        var_to_set.set("File is: {} \nThis only has one page, so there is nothing to {}.".format(filepath, which_function))
    else:
        if flag == 1:
            var_to_set.set("File is: {} \nFile has {} pages, which page should I extract?".format(filepath, CountPages(filepath)))
            SetPages(CountPages(filepath), extractCombo)
        else:
            var_to_set.set("File is: {} \nFile has {} pages, time to explode?".format(filepath, CountPages(filepath)))
        
   
def DoExtraction():
    textbox_text = extract_label.get()
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
    # print('Created: {}'.format(save_filename)) 
    tk.messagebox.showinfo(title='Alert', message='Extraction Complete!')
    
# End extract functions
##############################################

def DoExplode():
    textbox_text = explode_label.get()
    pattern = "File is: (.*?)\n"
    filepath = re.search(pattern, textbox_text).group(1)
    
    fname = os.path.splitext(os.path.basename(filepath))[0]
    directory = os.path.dirname(filepath) + '/'
    
    pdf = PyPDF2.PdfFileReader(filepath)
    for page in range(pdf.getNumPages()):
        pdf_writer = PyPDF2.PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(page))
        output_filename = directory + '{}_page_{}.pdf'.format(fname, page+1)
        
        with open(output_filename, 'wb') as out:
            pdf_writer.write(out)
            
        # print('Created: {}'.format(output_filename))
    tk.messagebox.showinfo(title='Alert', message='Kaboom!')

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
    # print(merge_filename_box.get(0,listsize-1))
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

##############################################
# Delete functions

def SetDeleteText(filepath):
    filename, extension = os.path.splitext(filepath)
    if extension.lower() != '.pdf':
        delete_label.set("File is: {} \nFile is not a PDF, cannot delete.".format(filepath))
    elif CountPages(filepath) == 1:
        delete_label.set("File is: {} \nThis only has one page, so there is nothing to delete.".format(filepath))
    else:
        countOfPages = CountPages(filepath)
        delete_label.set("File is: {} \nFile has {} pages, set pages to delete.".format(filepath, countOfPages))
        SetPages(countOfPages, deleteCombo_start)
        SetPages(countOfPages, deleteCombo_end)
        
def DoDelete():
    # check if valid
    try:
        startnumber = int(deleteCombo_start.get())
        endnumber = int(deleteCombo_end.get())
    except ValueError as ve:
        tk.messagebox.showinfo(title='Alert', message='Set yo pages') 
        return None
    if endnumber < startnumber:
        tk.messagebox.showinfo(title='Alert', message='Last page to delete cannot be lower than first page!') 
        return None
    
    # assuming validity    
    save_filename = filedialog.asksaveasfilename()
    textbox_text = delete_label.get()
    pattern = "File is: (.*?)\n"
    filepath = re.search(pattern, textbox_text).group(1)
    
    fname = os.path.splitext(os.path.basename(filepath))[0]
    directory = os.path.dirname(filepath) + '/'
    
    pdf = PyPDF2.PdfFileReader(filepath)
    pdf_writer = PyPDF2.PdfFileWriter()
    for page in range(pdf.getNumPages()):
        if page +1 < startnumber or page +1 > endnumber: 
            pdf_writer.addPage(pdf.getPage(page))
            with open(save_filename, 'wb') as out:
                pdf_writer.write(out)

    tk.messagebox.showinfo(title='Alert', message='File written.')        
    
# End delete functions
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
explode = ttk.Frame(notebook, width=500, height=350)

extract.grid(column=0, row=0, padx=15, pady=15)
merge.grid(column=0, row=0, padx=15, pady=15)
replace.grid(column=0, row=0, padx=15, pady=15)
delete.grid(column=0, row=0, padx=15, pady=15)
explode.grid(column=0, row=0, padx=15, pady=15)

# extract.rowconfigure(1, {'minsize': 300})
extract.columnconfigure(1, {'minsize': 300})

# add frames to notebook
notebook.add(extract, text='Extract')
notebook.add(merge, text='Merge')
notebook.add(replace, text='Replace')
notebook.add(delete, text='Delete')
notebook.add(explode, text='Explode')

##############################################
# Merge GUI elements
       
closeButton = ttk.Button(merge, text="Clear", command = ClearFiles)
closeButton.grid(row=1, column=1, padx=(10,10), pady=(10, 10), sticky = tk.W)
addFileButton = ttk.Button(merge, text="Add File", command = AddFile)
addFileButton.grid(row=1, column=0, padx=(10,10), pady=(10, 10), sticky = tk.W)   
mergeButton = ttk.Button(merge, text="Merge Files", command = DoMerger)
mergeButton.grid(row=5, column=0, padx=(10,10), pady=(10, 10), sticky = tk.W)   

# Add information text to merge
merge_information = tk.StringVar()
merge_information.set("This function allows for the merger (contatenation) of multiple PDFs.\nDrag and drop file names to reorder as required.")
label = tk.Label(merge, textvariable = merge_information, justify=tk.LEFT, anchor="w")
label.grid(row=2, column=0, padx=(10,10), pady=(10, 10), columnspan=4, sticky = tk.W+tk.E)

# add filelist to merge
merge_filename_box = DragDropListbox(merge, width=80)
merge_filename_box.grid(row=3, column=0, columnspan=2)

# End Merge GUI elements
##############################################

##############################################
# Extract GUI elements

closeButton = ttk.Button(extract, text="Clear", command=lambda: ClearFilesFromExtract(extractCombo, extract_label))
closeButton.grid(row=1, column=1, padx=(10,10), pady=(10, 10), sticky = tk.W)   
addFileButton = ttk.Button(extract, text="Add File", command=lambda: AddFileShared(1)) # Need lambda to pass argument
addFileButton.grid(row=1, column=0, padx=(10,10), pady=(10, 10), sticky = tk.W)   
extractButton = ttk.Button(extract, text="Extract", command = DoExtraction)
extractButton.grid(row=5, column=0, padx=(10,10), pady=(10, 10), sticky = tk.W)   

# Add information text to extract
extract_information = tk.StringVar()
extract_information.set("This function allows for the extraction of a single page from a multi-page PDF")
label = tk.Label(extract, textvariable = extract_information, justify=tk.LEFT, anchor="w")
label.grid(row=2, column=0, padx=(10,10), pady=(10, 10), columnspan=4, sticky = tk.W+tk.E)

# Add label to extract
extract_label = tk.StringVar()
extract_label.set("Choose a file with the 'Add File' button")
label = tk.Label(extract, textvariable = extract_label, justify=tk.LEFT, anchor="w")
label.grid(row=3, column=0, padx=(10,10), pady=(10, 10), columnspan=2, sticky = tk.W+tk.E)

# Add combobox for pagenumbers to extract
vlist = []
extractCombo = ttk.Combobox(extract, values = vlist)
extractCombo.set("Choose a page")
extractCombo.grid(row=4, column=0, padx=(10,10), pady=(10, 10), sticky = tk.W+tk.E)

# End Extract GUI elements
##############################################

##############################################
# Explode GUI elements

addFileButton = ttk.Button(explode, text="Add File", command=lambda: AddFileShared(2)) # Need lambda to pass argument
addFileButton.grid(row=1, column=0, padx=(10,10), pady=(10, 10), sticky = tk.W)   
explodeButton = ttk.Button(explode, text="Explode", command = DoExplode)
explodeButton.grid(row=5, column=0, padx=(10,10), pady=(10, 10), sticky = tk.W)   

# Add information text to explode
explode_information = tk.StringVar()
explode_information.set("Explode will split a multi-page PDF into single pages")
label = tk.Label(explode, textvariable = explode_information, justify=tk.LEFT, anchor="w")
label.grid(row=2, column=0, padx=(10,10), pady=(10, 10), columnspan=4, sticky = tk.W+tk.E)

# Add label to explode
explode_label = tk.StringVar()
explode_label.set("Choose a file with the 'Add File' button")
label = tk.Label(explode, textvariable = explode_label, justify=tk.LEFT, anchor="w")
label.grid(row=3, column=0, padx=(10,10), pady=(10, 10), columnspan=2, sticky = tk.W+tk.E)

# End Explode GUI elements
##############################################

##############################################
# Delete GUI elements

addFileButton = ttk.Button(delete, text="Add File", command=lambda: AddFileShared(3)) # 
addFileButton.grid(row=1, column=0, padx=(10,10), pady=(10, 10), sticky = tk.W)   
deleteButton = ttk.Button(delete, text="Delete", command = DoDelete) 
deleteButton.grid(row=5, column=0, padx=(10,10), pady=(10, 10), sticky = tk.W)   

# Add information text to delete
delete_information = tk.StringVar()
delete_information.set("This function allows for the deletion of one or more pages from a multi-page PDF")
label = tk.Label(delete, textvariable = delete_information, justify=tk.LEFT, anchor="w")
label.grid(row=2, column=0, padx=(10,10), pady=(10, 10), columnspan=4, sticky = tk.W+tk.E)

# Add label to delete
delete_label = tk.StringVar()
delete_label.set("Choose a file with the 'Add File' button")
label = tk.Label(delete, textvariable = delete_label, justify=tk.LEFT, anchor="w")
label.grid(row=3, column=0, padx=(10,10), pady=(10, 10), columnspan=2, sticky = tk.W+tk.E)

# Add comboboxes for pagenumbers to delete
delete_vlist_start = []
delete_vlist_end = []
deleteCombo_start = ttk.Combobox(delete, values = vlist)
deleteCombo_end = ttk.Combobox(delete, values = vlist)
deleteCombo_start.set("First page to delete")
deleteCombo_end.set("Last page to delete")
deleteCombo_start.grid(row=4, column=0, padx=(10,10), pady=(10, 10), sticky = tk.W+tk.E)
deleteCombo_end.grid(row=4, column=1, padx=(10,10), pady=(10, 10), sticky = tk.W+tk.E)

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

png_base64_string = """iVBORw0KGgoAAAANSUhEUgAAAJYAAABWCAIAAACii/gBAAABhGlDQ1BJQ0MgcHJvZmlsZQAAKJF9kT1Iw0AcxV8TtSIVBzuIOGSoThb8QhylikWwUNoKrTqYXPohNGlIUlwcBdeCgx+LVQcXZ10dXAVB8APE0clJ0UVK/F9SaBHjwXE/3t173L0DhHqZaVbHGKDptpmKx6RsbkUKvkJEFwSMQ5SZZSTSCxn4jq97BPh6F+VZ/uf+HL1q3mJAQCKeZYZpE68TT2/aBud94jArySrxOfGoSRckfuS64vEb56LLAs8Mm5nUHHGYWCq2sdLGrGRqxFPEEVXTKV/Ieqxy3uKslauseU/+wlBeX05zneYQ4lhEAklIUFDFBsqwEaVVJ8VCivZjPv5B158kl0KuDTByzKMCDbLrB/+D391ahckJLykUAzpfHOdjGAjuAo2a43wfO07jBBCfgSu95a/UgZlP0mstLXIE9G0DF9ctTdkDLneAgSdDNmVXEmkKhQLwfkbflAP6b4GeVa+35j5OH4AMdbV0AxwcAiNFyl7zeXd3e2//nmn29wMsp3KLNIn8WwAAAAlwSFlzAAAuIwAALiMBeKU/dgAAAAd0SU1FB+YDBgI5I8FlX5UAAAAZdEVYdENvbW1lbnQAQ3JlYXRlZCB3aXRoIEdJTVBXgQ4XAAAAvUlEQVR42u3dMQ6AIAxAUWuce//blgPUgbGQ90fGvqAxJhBV9ejkXiNAKIRCiFBn9/WliDCXsfUvCLvQg1QIhRChEAqhECIUQiEUQoRCKIRCiFAIhVAIEQqhEAohQiEUQiFEKIRCKIQIhVAIhRChEAqhECIUQiEUQoRCKIRCiFAIhVAIEeoOwsw0o+FFPzTfJQeTc8mBd6EQCqEQIhRCIRRChEIohEKIUAiFUAgv6uevvexCIRRChEIohNpvARgwD823LLzRAAAAAElFTkSuQmCC"""

menubar = tk.Menu(root)

root.config(menu=menubar)
file_menu = tk.Menu(menubar, tearoff=0)
# add a menu item to the menu
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=file_menu)

root.iconphoto(False, tk.PhotoImage(data=png_base64_string))
root.mainloop()