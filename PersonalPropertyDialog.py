import wx
import base64
import os
from ID_DEFINE import *
import MySQL
class PersonalPropertyDialog(wx.Dialog):
    def __init__(self, parent,myId,myNickName='',myIcon='',myHomeTown='',myBarCode='',size=wx.DefaultSize, pos=wx.DefaultPosition,
                 style=wx.DEFAULT_DIALOG_STYLE, name='PersonalProperty Dialog'):
        wx.Dialog.__init__(self)
        self.SetExtraStyle(wx.DIALOG_EX_METAL)
        self.Create(parent, -1, "设置个人信息", pos, size, style, name)
        self.myId = myId
        self.myNickName = myNickName
        self.myIcon = myIcon
        self.myHomeTown = myHomeTown
        self.myBarCode = myBarCode
        self.bmp = ''
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer()
        hbox.Add((10,-1))
        hbox.Add(wx.StaticText(self, label="我的头像"), 0, wx.TOP | wx.RIGHT | wx.BOTTOM, 20)
        self.iconBTN = wx.Button(self, -1, size = (60, 60))
        self.iconBTN.Bind(wx.EVT_BUTTON, self.OnModifyMyIcon)
        if(self.myIcon!=''):
            with open(DEFAULT_PATH+'\\ls.png', 'wb') as file:
                image = base64.b64decode(self.myIcon)  # 解码
                file.write(image)
                # file.write(self.myIcon)
            bmp = wx.Bitmap(DEFAULT_PATH+'\\ls.png')
        else:
            print("there")
            bmp = wx.Bitmap(USER_PATH+'\\1.png')
        self.iconBTN.SetBitmap(bmp)
        hbox.Add((200, -1),1)
        hbox.Add(self.iconBTN, 0, wx.RIGHT, 10)
        vbox.Add(hbox, 0, wx.EXPAND | wx.ALL, 10)
        line = wx.StaticLine(self, -1, size=(20, -1), style=wx.LI_HORIZONTAL)
        vbox.Add(line, 0, wx.EXPAND)

        hbox = wx.BoxSizer()
        hbox.Add((10,-1))
        hbox.Add(wx.StaticText(self, label="我的ID编号"), 0, wx.TOP | wx.RIGHT | wx.BOTTOM, 10)
        idNameBTN = wx.Button(self, -1, label = str(self.myId), size = (120, 30))
        idNameBTN.Enable(False)
        idNameBTN.SetBackgroundColour(wx.Colour(240,240,240))
        hbox.Add((200, -1),1)
        hbox.Add(idNameBTN, 0, wx.RIGHT, 10)
        vbox.Add(hbox, 0, wx.EXPAND | wx.ALL, 10)
        line = wx.StaticLine(self, -1, size=(20, -1), style=wx.LI_HORIZONTAL)
        vbox.Add(line, 0, wx.EXPAND)

        hbox = wx.BoxSizer()
        hbox.Add((10,-1))
        hbox.Add(wx.StaticText(self, label="我的昵称"), 0, wx.TOP | wx.RIGHT | wx.BOTTOM, 10)
        self.nickNameBTN = wx.Button(self, -1, label = self.myNickName, size = (120, 30))
        self.nickNameBTN.Bind(wx.EVT_BUTTON, self.OnModifyNickName)
        hbox.Add((200, -1),1)
        hbox.Add(self.nickNameBTN, 0, wx.RIGHT, 10)
        vbox.Add(hbox, 0, wx.EXPAND | wx.ALL, 10)
        line = wx.StaticLine(self, -1, size=(20, -1), style=wx.LI_HORIZONTAL)
        vbox.Add(line, 0, wx.EXPAND)

        hbox = wx.BoxSizer()
        hbox.Add((10,-1))
        hbox.Add(wx.StaticText(self, label="我的地址"), 0, wx.TOP | wx.RIGHT | wx.BOTTOM, 10)
        nickNameBTN = wx.Button(self, -1, label = self.myHomeTown, size = (120, 30))
        hbox.Add((200, -1),1)
        hbox.Add(nickNameBTN, 0, wx.RIGHT, 10)
        vbox.Add(hbox, 0, wx.EXPAND | wx.ALL, 10)
        line = wx.StaticLine(self, -1, size=(20, -1), style=wx.LI_HORIZONTAL)
        vbox.Add(line, 0, wx.EXPAND)

        hbox = wx.BoxSizer()
        hbox.Add((10,-1))
        hbox.Add(wx.StaticText(self, label="我的二维码"), 0, wx.TOP | wx.RIGHT | wx.BOTTOM, 20)
        iconBTN = wx.Button(self, -1, size = (200, 200))
        bmp = wx.Bitmap(DEFAULT_PATH+'/QRcode.jpg')
        iconBTN.SetBitmap(bmp)
        hbox.Add((200, -1),1)
        hbox.Add(iconBTN, 0, wx.RIGHT, 10)
        vbox.Add(hbox, 0, wx.EXPAND | wx.ALL, 10)
        line = wx.StaticLine(self, -1, size=(20, -1), style=wx.LI_HORIZONTAL)
        vbox.Add(line, 0, wx.EXPAND)

        btnsizer = wx.StdDialogButtonSizer()
        okBTN = wx.Button(self, wx.ID_OK, '返     回',size=(400,40))
        okBTN.SetDefault()
        btnsizer.AddButton(okBTN)
        btnsizer.Realize()
        vbox.Add(btnsizer, 1, wx.ALIGN_CENTER | wx.ALL, 20)
        self.SetSizer(vbox)
        vbox.Fit(self)
    def OnModifyMyIcon(self,event):
        wildcard = "文本文件 (*.png)|*.png|" \
                   "所有文件 (*.*)|*.*"
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=ICO_PATH+'ico48/',
            defaultFile="*.png",
            wildcard=wildcard,
            style=wx.FD_OPEN | wx.FD_MULTIPLE |
                  wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST |
                  wx.FD_PREVIEW
        )
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetFilename()
            with open(filename, 'rb') as file:
                image_data = file.read()
                base64_data = base64.b64encode(image_data)  # 'bytes'型数据
                self.myIcon = base64_data.decode()  # str型数据
                self.bmp = wx.Bitmap(dlg.GetFilename())
            import shutil
            shutil.copyfile(filename,USER_PATH+'%s.png'%self.myId)
            ourchatDB = MySQL.OurchatDB()
            error = ourchatDB.SaveIcon(self.myId, self.myIcon)
            if (error == ID_NO_ERROR):
                self.iconBTN.SetBitmap(self.bmp)
        dlg.Destroy()

    def OnModifyNickName(self, evt):
        dlg = wx.TextEntryDialog(
                self, ' ',
                '修改我的昵称', " ")

        dlg.SetValue(self.myNickName)

        if dlg.ShowModal() == wx.ID_OK:
            self.myNickName = dlg.GetValue()
            self.nickNameBTN.SetLabel(self.myNickName)
            ourchatDB = MySQL.OurchatDB(D)
            error = ourchatDB.UpdateNickName(self.myId, self.myNickName)
            if (error == ID_NO_ERROR):
                self.nickNameBTN.SetLabel(self.myNickName)
        dlg.Destroy()

    def GetValue(self):
        return self.myNickName, self.myHomeTown,self.myIcon,self.bmp