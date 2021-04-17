#!/usr/bin/env python

# good tutorial at https://zetcode.com/wxpython/
# graphics tutorial


import sys
print(sys.version)
print(sys.version_info)

"""
Hello World, but with more meat.
"""

import wx
import ctypes

# makes dpi aware so GUI text isnt blurry
ctypes.windll.shcore.SetProcessDpiAwareness(1)

class GoodAsFrame(wx.Frame):
    """
    A Frame that says Hello World
    """

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(GoodAsFrame, self).__init__(*args, **kw)

        # determine the optimal size for the application with 8x5 geometry
        display_geom = wx.Display(0).GetGeometry()
        x_factor = int(display_geom[2]/800)
        y_factor = int(display_geom[3]/500)
        scale = min(x_factor,y_factor)

        self.SetSize(800*scale, 500*scale)
        self.Centre()

        # create a panel in the frame
        # pnl = wx.Panel(self)


        # # put some text with a larger bold font on it
        # st = wx.StaticText(pnl, label="Hello World!")
        # font = st.GetFont()
        # font.PointSize += 10
        # font = font.Bold()
        # st.SetFont(font)

        # and create a sizer to manage the layout of child widgets
        # sizer = wx.BoxSizer(wx.VERTICAL)
        # sizer.Add(st, wx.SizerFlags().Border(wx.TOP|wx.LEFT, 25))
        # pnl.SetSizer(sizer)

        # self.img = wx.svg.SVGimage.CreateFromFile("test.svg")
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        

        # create a menu bar
        self.makeMenuBar()

        # and a status bar with 2 fields
        self.CreateStatusBar(3)
        # self.status_bar.SetFieldsCount(2)
        self.SetStatusText("Welcome to Good As GUI!", 1)
        self.SetStatusText("Pretty good, eh?", 2)
        self.SetStatusText("this text is context dependant", 0)

        self.content_saved = True
        
        
    def OnPaint(self, event):
        dc = wx.PaintDC(self) 
        brush = wx.Brush("white")  
        dc.SetBackground(brush)  
        dc.Clear() 
            
        dc.DrawBitmap(wx.Bitmap("python.jpg"),10,10,True) 
        color = wx.Colour(255,0,0)
        b = wx.Brush(color) 
            
        dc.SetBrush(b) 
        dc.DrawCircle(300,125,50) 
        dc.SetBrush(wx.Brush(wx.Colour(255,255,255))) 
        dc.DrawCircle(300,125,30) 
            
        font = wx.Font(18, wx.ROMAN, wx.ITALIC, wx.NORMAL) 
        dc.SetFont(font) 
        dc.DrawText("Hello wxPython",400,10) 
            
        pen = wx.Pen(wx.Colour(0,0,255)) 
        dc.SetPen(pen) 
        dc.DrawLine(200,50,350,50) 
        dc.SetBrush(wx.Brush(wx.Colour(0,255,0), wx.CROSS_HATCH)) 
        dc.DrawRectangle(1000, 15, 90, 60)

    def makeMenuBar(self):
        """
        A menu bar is composed of menus, which are composed of menu items.
        This method builds a set of menus and binds handlers to be called
        when the menu item is selected.
        """

        # Make a file menu with Hello and Exit items
        file_menu = wx.Menu()
        # The "\t..." syntax defines an accelerator key that also triggers
        # the same event
        # open_item = wx.MenuItem(file_menu, id=1, text="&Open...\tCtrl+O", helpString="Open a Good As file")
        # open_item.SetBitmap(wx.Bitmap('exit.png'))
        # file_menu.Append(open_item)
        open_item = file_menu.Append(-1, "&Open...\tCtrl+O", "Open a Good As file")
        save_as_item = file_menu.Append(-1,'Save File As...\tCtrl+Shift+S',"Save the current file")
        
        file_menu.AppendSeparator()
        # When using a stock ID we don't need to specify the menu item's
        # label
        exitItem = file_menu.Append(wx.ID_EXIT)

        # Now a help menu for the about item
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        # Make the menu bar and add the two menus to it. The '&' defines
        # that the next letter is the "mnemonic" for the menu item. On the
        # platforms that support it those letters are underlined and can be
        # triggered from the keyboard.
        menuBar = wx.MenuBar()
        menuBar.Append(file_menu, "&File")
        menuBar.Append(helpMenu, "&Help")

        # Give the menu bar to the frame
        self.SetMenuBar(menuBar)

        # Finally, associate a handler function with the EVT_MENU event for
        # each of the menu items. That means that when that menu item is
        # activated then the associated handler function will be called.
        self.Bind(wx.EVT_MENU, self.OnSaveAs, save_as_item)
        self.Bind(wx.EVT_MENU, self.OnOpen, open_item)
        self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)


    def OnExit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)

    def OnOpen(self, event): #friggin CamelCase this is supposed to be python!

        if not self.content_saved:
            if wx.MessageBox("Current content has not been saved! Proceed?", "Please confirm",
                            wx.ICON_QUESTION | wx.YES_NO, self) == wx.NO:
                return

        # otherwise ask the user what new file to open
        with wx.FileDialog(self, "Open XYZ file", wildcard="XYZ files (*.xyz)|*.xyz|Any files (*.*)|*.*",
                        style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'r') as file:
                    self.doLoadData(file)
            except IOError:
                wx.LogError("Cannot open file '%s'." % newfile)
    
    def OnSaveAs(self, event):

        with wx.FileDialog(self, "Save XYZ file", wildcard="XYZ files (*.xyz)|*.xyz",
                        style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

            # save the current contents in the file
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'w') as file:
                    self.doSaveData(file)
            except IOError:
                wx.LogError("Cannot save current data in file '%s'." % pathname)

    def doLoadData(self, file):
        print("loading file")

    def doSaveData(self, file):
        print("saving file")

    def on_save(self, event):
        """Say hello to the user."""
        wx.MessageBox("Hello again from wxPython")


    def OnAbout(self, event):
        """Display an About Dialog"""
        wx.MessageBox("This is a wxPython Hello World sample",
                      "About Hello World 2",
                      wx.OK|wx.ICON_INFORMATION)


if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frm = GoodAsFrame(None, title='Good As GUI')
    frm.Show()
    app.MainLoop()