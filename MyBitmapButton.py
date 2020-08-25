import os
import wx

DEFAULT_PATH = os.path.abspath('.\\') + '\\'
IMAGE_PATH = os.path.abspath('.\\') + '\\bitmaps\\'


class MyBitmapButton(wx.Button):
    def __init__(self, parent, id=-1, label='', pos=wx.DefaultPosition, size=wx.DefaultSize, name=""):
        wx.Button.__init__(self, parent, id, label, pos, size)
        self.name = name
        self.newMessageCount = 0
        self.bitmap = None
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, evt):
        evt.GetId()
        imageLs = None
        dc = wx.PaintDC(self)
        # dc.SetBackground(wx.Brush("#FFBB99"))
        # dc.SetBackground(wx.Brush("white"))
        dc.Clear()
        if not self.bitmap:
            originIMG = wx.Image(IMAGE_PATH + 'toucan.png', wx.BITMAP_TYPE_PNG).Rescale(width=70, height=65,
                                                                                        quality=wx.IMAGE_QUALITY_HIGH).Mirror(
                horizontally=True)
            self.bitmap = originIMG.ConvertToBitmap()
        else:
            imageLS = self.bitmap.ConvertToImage().Rescale(width=70, height=65, quality=wx.IMAGE_QUALITY_HIGH)
            imageLs = imageLS.ConvertToBitmap()
        dc.DrawBitmap(imageLs, 0, 0, True)
        # dc.SetFont()
        if self.newMessageCount > 0:
            dc.SetTextForeground("white")
            dc.SetPen(wx.Pen("red", 1))
            dc.SetBrush(wx.Brush("red"))
            dc.DrawCircle(55, 15, 8)
            if self.newMessageCount > 99:
                dc.DrawText('...', 51, 4)
            elif self.newMessageCount > 9:
                dc.DrawText(str(self.newMessageCount), 48, 7)
            else:
                dc.DrawText(str(self.newMessageCount), 52, 7)

    def SetBitmap(self, bitmap, direction=wx.LEFT):
        self.bitmap = bitmap
        self.Refresh()

    def SetNewMessageCount(self, count):
        self.newMessageCount = count
        self.Refresh()

    def GetName(self):
        return self.name
