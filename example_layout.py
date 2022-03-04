#!/usr/bin/env python


"""
ZetCode wxPython tutorial

In this example we create a Go To class
layout with wx.BoxSizer.

author: Jan Bodnar
website: www.zetcode.com
last modified: July 2020
"""

import wx
import wx.xrc
import os
import pypdfium2 as pdfium
from pathlib import Path
from shutil import rmtree

wildcard = "PDF files (*.pdf)|*.pdf|" \
            "All files (*.*)|*.*"
            
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

class pdfMerger(wx.Frame):

    def __init__(self, parent, id = wx.ID_ANY, title = u"PDF Merger", size = wx.Size(900, 600)):
        super(pdfMerger, self).__init__(parent, title=title)
        self.currentDirectory = os.getcwd()

        self.InitUI()
        self.Bind(wx.EVT_CLOSE, self.onClose) 

    def InitUI(self):

        panel = wx.Panel(self)

        font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
        font.SetFamily(wx.FONTFAMILY_TELETYPE)
        font.SetPointSize(9)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(panel, label='Class Name')
        st1.SetFont(font)
        hbox1.Add(st1, flag=wx.RIGHT, border=8)
        tc = wx.TextCtrl(panel)
        hbox1.Add(tc, proportion=1)
        vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        vbox.Add((-1, 10))

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        st2 = wx.StaticText(panel, label='Matching Classes')
        st2.SetFont(font)
        hbox2.Add(st2)
        vbox.Add(hbox2, flag=wx.LEFT | wx.TOP, border=10)

        vbox.Add((-1, 10))

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        tc2 = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        hbox3.Add(tc2, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbox3, proportion=1, flag=wx.LEFT|wx.RIGHT|wx.EXPAND,
            border=10)

        vbox.Add((-1, 25))

        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        cb1 = wx.CheckBox(panel, label='Case Sensitive')
        cb1.SetFont(font)
        hbox4.Add(cb1)
        cb2 = wx.CheckBox(panel, label='Nested Classes')
        cb2.SetFont(font)
        hbox4.Add(cb2, flag=wx.LEFT, border=10)
        cb3 = wx.CheckBox(panel, label='Non-Project classes')
        cb3.SetFont(font)
        hbox4.Add(cb3, flag=wx.LEFT, border=10)
        vbox.Add(hbox4, flag=wx.LEFT, border=10)

        vbox.Add((-1, 25))

        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        openFileDlgBtn = wx.Button(panel, label='Add File', size=(70, 30))
        openFileDlgBtn.Bind(wx.EVT_BUTTON, self.onOpenFile)
        hbox5.Add(openFileDlgBtn)
        saveFileDlgBtn = wx.Button(panel, label='Save File', size=(70, 30))
        saveFileDlgBtn.Bind(wx.EVT_BUTTON, self.onSaveFile)
        hbox5.Add(saveFileDlgBtn, flag=wx.LEFT|wx.BOTTOM, border=5)
        vbox.Add(hbox5, flag=wx.ALIGN_RIGHT|wx.RIGHT, border=10)

        panel.SetSizer(vbox)

    def onOpenFile(self, event):
        """
        Create and show the Open FileDialog
        """
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=self.currentDirectory, 
            defaultFile="",
            wildcard=wildcard,
            style=wx.FD_OPEN | wx.FD_MULTIPLE | wx.FD_CHANGE_DIR
            )
        if dlg.ShowModal() == wx.ID_OK:
            thumbnaildir = makedir()
            paths = dlg.GetPaths()
            print("You chose the following file(s):")
            for path in paths:
                print(path)
            for image, suffix in pdfium.render_pdf(path):
                image.save(f'{thumbnaildir}/output_{suffix}.jpg')
        dlg.Destroy()
        
    def onSaveFile(self, event):
        """
        Create and show the Save FileDialog
        """
        dlg = wx.FileDialog(
            self, message="Save file as ...", 
            defaultDir=self.currentDirectory, 
            defaultFile="", wildcard=wildcard, style=wx.FD_SAVE
            )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            print("You chose the following filename: %s" % path)
        dlg.Destroy()
        
    def onClose(self, event):
        # delete all the thumbnails, and the directory
        for path in Path("C:/Temp/thumbnails").glob("**/*"):
            if path.is_file():
                path.unlink()
            elif path.is_dir():
                rmtree(path)
        self.Destroy()

def main():

    app = wx.App()
    ex = pdfMerger(None)
    ex.Show()
    ex.SetSize(1200, 900)
    ex.Centre()
    app.MainLoop()


if __name__ == '__main__':
    main()