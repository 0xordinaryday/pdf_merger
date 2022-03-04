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
from wx.lib.agw.scrolledthumbnail import (ScrolledThumbnail, Thumb, NativeImageHandler)

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

        font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
        font.SetFamily(wx.FONTFAMILY_TELETYPE)
        font.SetPointSize(9)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.splitter = wx.SplitterWindow(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
        
        self.scroll = ScrolledThumbnail(self.splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
        self.scroll.SetScrollRate(5, 5)
        self.panel = wx.Panel(self.splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        button_sizer = wx.BoxSizer( wx.HORIZONTAL )
        
        openFileDlgBtn = wx.Button(self.panel, label='Add File', size=(70, 30))
        openFileDlgBtn.Bind(wx.EVT_BUTTON, self.onOpenFile)
        button_sizer.Add(openFileDlgBtn, 0, wx.ALL, 5 )
        saveFileDlgBtn = wx.Button(self.panel, label='Save File', size=(70, 30))
        saveFileDlgBtn.Bind(wx.EVT_BUTTON, self.onSaveFile)
        button_sizer.Add(saveFileDlgBtn, 0, wx.ALL, 5 )
        
        self.panel.SetSizer(button_sizer)
        self.panel.Layout()
        button_sizer.Fit(self.panel)
        self.splitter.SplitHorizontally( self.scroll, self.panel, 820)
        sizer.Add(self.splitter, 1, wx.EXPAND, 5)
        
        self.SetSizer(sizer)
        self.Layout()
        self.Centre(wx.BOTH)

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
            self.showDir()            
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
        
    def showDir(self):
        thumbnaildir = "C:/Temp/thumbnails"
        files = os.listdir(thumbnaildir)
        thumbs = []
        for f in files:
            if os.path.splitext(f)[1] in [".jpg", ".gif", ".png"]:
                thumbs.append(Thumb(thumbnaildir, f, caption=f, imagehandler=NativeImageHandler))
        self.scroll.ShowThumbs(thumbs)
        
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