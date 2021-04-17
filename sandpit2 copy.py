#!/usr/bin/env python

import wx
# import images

# There are two different approaches to drawing, buffered or direct.
# This sample shows both approaches so you can easily compare and
# contrast the two by changing this value.
BUFFERED = 0

#---------------------------------------------------------------------------
class Mywin(wx.Frame): 
            
   def __init__(self, parent, title): 
      super(Mywin, self).__init__(parent, title = title,size = (500,300))  
      self.InitUI()
         
   def InitUI(self): 
      # self.Bind(wx.EVT_PAINT, self.OnPaint)
      scrollWin = MyCanvas( self, -1 )
      self.Centre() 
      self.Show(True)

class MyCanvas(wx.ScrolledWindow):
    def __init__(self, parent, id = -1, size = wx.DefaultSize):
        wx.ScrolledWindow.__init__(self, parent, id, (0, 0), size=size, style=wx.SUNKEN_BORDER)

        self.lines = []
        self.maxWidth  = 1000
        self.maxHeight = 1000
        self.x = self.y = 0
        self.curLine = []
        self.drawing = False

        self.SetVirtualSize((self.maxWidth, self.maxHeight))
        self.SetScrollRate(20,20)

        if BUFFERED:
            # Initialize the buffer bitmap.  No real DC is needed at this point.
            self.buffer = wx.Bitmap(self.maxWidth, self.maxHeight)
            dc = wx.BufferedDC(None, self.buffer)
            dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
            dc.Clear()


        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftButtonEvent)
        self.Bind(wx.EVT_LEFT_UP,   self.OnLeftButtonEvent)
        self.Bind(wx.EVT_MOTION,    self.OnLeftButtonEvent)
        self.Bind(wx.EVT_PAINT,     self.OnPaint)


    def getWidth(self):
        return self.maxWidth

    def getHeight(self):
        return self.maxHeight


    def OnPaint(self, event):
        if BUFFERED:
            # Create a buffered paint DC.  It will create the real
            # wx.PaintDC and then blit the bitmap to it when dc is
            # deleted.  Since we don't need to draw anything else
            # here that's all there is to it.
            dc = wx.BufferedPaintDC(self, self.buffer, wx.BUFFER_VIRTUAL_AREA)
        else:
            dc = wx.PaintDC(self)
            self.PrepareDC(dc)
            # Since we're not buffering in this case, we have to
            # (re)paint the all the contents of the window, which can
            # be potentially time consuming and flickery depending on
            # what is being drawn and how much of it there is.
            self.DoDrawing(dc)


    def SetXY(self, event):
        self.x, self.y = self.ConvertEventCoords(event)

    def ConvertEventCoords(self, event):
        newpos = self.CalcUnscrolledPosition(event.GetX(), event.GetY())
        return newpos

    def OnLeftButtonEvent(self, event):
        if self.IsAutoScrolling():
            self.StopAutoScrolling()

        if event.LeftDown():
            self.SetFocus()
            self.SetXY(event)
            self.curLine = []
            self.CaptureMouse()
            self.drawing = True

        elif event.Dragging() and self.drawing:
            if BUFFERED:
                # If doing buffered drawing we'll just update the
                # buffer here and then refresh that portion of the
                # window.  Then the system will send an event and that
                # portion of the buffer will be redrawn in the
                # EVT_PAINT handler.
                dc = wx.BufferedDC(None, self.buffer)
            else:
                # otherwise we'll draw directly to a wx.ClientDC
                dc = wx.ClientDC(self)
                self.PrepareDC(dc)

            dc.SetPen(wx.Pen('MEDIUM FOREST GREEN', 4))
            coords = (self.x, self.y) + self.ConvertEventCoords(event)
            self.curLine.append(coords)
            dc.DrawLine(*coords)
            self.SetXY(event)

            if BUFFERED:
                # figure out what part of the window to refresh, based
                # on what parts of the buffer we just updated
                x1,y1, x2,y2 = dc.GetBoundingBox()
                x1,y1 = self.CalcScrolledPosition(x1, y1)
                x2,y2 = self.CalcScrolledPosition(x2, y2)
                # make a rectangle
                rect = wx.Rect()
                rect.SetTopLeft((x1,y1))
                rect.SetBottomRight((x2,y2))
                rect.Inflate(2,2)
                # refresh it
                self.RefreshRect(rect)

        elif event.LeftUp() and self.drawing:
            self.lines.append(self.curLine)
            self.curLine = []
            self.ReleaseMouse()
            self.drawing = False


if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    win = Mywin(None,'Drawing demo') 
    app.MainLoop()