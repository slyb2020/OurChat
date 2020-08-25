import base64
from MyBitmapButton import MyBitmapButton
from MyThreads import *


class ChatIcon(wx.Panel):
    def __init__(self, parent, myId, friendId, userName='', nickName='', icon='', homeTown='', clock='', lastMessage='',
                 newMessageNum=0):
        wx.Panel.__init__(self, parent, -1, size=(240, 65), name=str(friendId))
        self.myId = myId
        self.friendId = friendId
        self.focusState = False
        hbox = wx.BoxSizer()
        self.button = MyBitmapButton(self, -1, size=(70, 65), name=str(friendId))
        if icon:
            with open(DEFAULT_PATH + '/ls.png', 'wb') as file:
                image = base64.b64decode(icon)  # 解码
                file.write(image)
            bmp = wx.Bitmap(DEFAULT_PATH + '/ls.png')
        else:
            bmp = wx.Bitmap(USER_PATH + '/%s.png' % friendId)
        self.button.SetBitmap(bmp)
        hbox.Add(self.button, 0)
        vbox = wx.BoxSizer(wx.VERTICAL)
        hhbox = wx.BoxSizer()
        text = wx.StaticText(self, -1, label=userName, size=(100, 20))
        hhbox.Add(text, 0, wx.TOP, border=8)
        hhbox.Add((10, -1), 1)
        self.lastMessageClockLABEL = wx.StaticText(self, label=clock, size=(50, 30))
        hhbox.Add(self.lastMessageClockLABEL, 0, wx.TOP, border=8)
        vbox.Add(hhbox, 0, wx.EXPAND)
        hhbox = wx.BoxSizer()
        if len(lastMessage) > 12:
            message = lastMessage[0:12] + "..."
        else:
            message = lastMessage
        self.lastMessageLABEL = wx.StaticText(self, label=message, size=(150, 30))
        hhbox.Add(self.lastMessageLABEL, 0, wx.BOTTOM, border=5)
        hhbox.Add((1, -1), 1)
        if newMessageNum == 0:
            num = ''
        else:
            num = "(%d)" % newMessageNum
        self.lastMessageNumLABEL = wx.StaticText(self, label=num, size=(30, 30))
        hhbox.Add(self.lastMessageNumLABEL, 0, wx.BOTTOM, border=5)
        vbox.Add(hhbox, 0, wx.EXPAND)
        hbox.Add((5, -1))
        hbox.Add(vbox, 1, wx.EXPAND)
        self.SetSizer(hbox)

        self.friendInfoUpdater = wx.PyTimer(self.StartFriendUpdate)
        self.friendInfoUpdater.Start(1000)
        self.updateMiddlePanelThread = UpdateMiddlePanelThread(self)
        self.Bind(EVT_UPDATE_MIDDLEPANEL, self.OnUpdate)

    def OnUpdate(self, event):
        self.button.SetNewMessageCount(event.num)
        self.UpdateLastMessage(event.num, event.lastMessage, event.lastTime)

    def StartFriendUpdate(self):
        self.updateMiddlePanelThread.Start(self.myId, self.friendId)

    def UpdateLastMessage(self, num, lastMessage, lastTime):
        if len(lastMessage) > 12:
            message = lastMessage[0:12] + "..."
        else:
            message = lastMessage
        if num == 0:
            number = ''
        else:
            number = "(%d)" % num
        self.lastMessageLABEL.SetLabel(message)
        self.lastMessageClockLABEL.SetLabel(str(lastTime)[11:])
        self.lastMessageNumLABEL.SetLabel(number)

    def SetFocus(self):
        self.focusState = True
        self.SetBackgroundColour(wx.Colour(200, 200, 200))
        self.Refresh()

    def LostFocus(self):
        self.focusState = False
        self.SetBackgroundColour(wx.Colour(235, 235, 235))
        self.Refresh()
