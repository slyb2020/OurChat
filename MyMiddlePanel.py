import wx.lib.scrolledpanel as scrolled

from ChatIcon import ChatIcon
from MyThreads import *


class MiddlePanel(scrolled.ScrolledPanel):
    def __init__(self, parent, id, size=wx.DefaultSize):
        scrolled.ScrolledPanel.__init__(self, parent, id, size)
        self.itemList = []
        self.Bind(wx.EVT_BUTTON, self.OnChaterIconClick)
        self.SetAutoLayout(1)
        self.SetupScrolling()

    def AddItem(self, myId, userId, userName='', nickName='', icon='', homeTown='', clock='', lastMessage='',
                newMessageNum=0):
        chatIcon = ChatIcon(self, myId, userId, userName, nickName, icon, homeTown, clock, lastMessage, newMessageNum)
        self.itemList.append(chatIcon)
        return chatIcon.updateMiddlePanelThread

    def MyRefresh(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        for item in self.itemList:
            vbox.Add(item, 0, wx.EXPAND)
        self.SetSizer(vbox)
        # self.Layout()

    def OnChaterIconClick(self, event):
        name = event.GetEventObject().GetName()
        for item in self.itemList:
            item.LostFocus()
            if item.GetName() == name:
                item.SetFocus()
        event.Skip()
