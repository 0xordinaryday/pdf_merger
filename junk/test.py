import os
import wx
from wx.lib.agw.scrolledthumbnail import (ScrolledThumbnail, Thumb, NativeImageHandler)

class MyFrame(wx.Frame):

  def __init__(self, parent):
    wx.Frame.__init__(self, parent, -1, "Ya boy", size=(1200,300))
    
    self.scroll = ScrolledThumbnail(self, -1, size=(400,300))
    
  def ShowDir(self, dir):
    dir = os.getcwd()
    files = os.listdir(dir)
    thumbs = []
    for f in files:
      if os.path.splitext(f)[1] in [".jpg", ".gif", ".png"]:
        thumbs.append(Thumb(dir, f, caption=f, imagehandler=NativeImageHandler))
    self.scroll.ShowThumbs(thumbs)
    
app = wx.App(False)
frame = MyFrame(None)
frame.ShowDir(os.getcwd())
frame.Show(True)

app.MainLoop()