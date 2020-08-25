import pymysql as MySQLdb
from ID_DEFINE import *
import base64
from MyConfig import DataBaseConfig
import wx
import string


def TransformBase64(img_name):
    """
    image -> base64
    :param img_name:
    :return:
    """
    try:
        with open(img_name, 'rb') as file:
            image_data = file.read()
            base64_data = base64.b64encode(image_data)  # 'bytes'型数据
            str_base64_data = base64_data.decode()  # str型数据
            return str_base64_data
    except:
        return "erro"


class DataBase:
    def __init__(self, keyword):
        self.keyword = keyword
        self.configCFG = DataBaseConfig()
        self.witchDB = 0
        self.Setup()

    def Setup(self):
        isSuccess, self.witchDB, self.testCloud, self.formalCloud, self.testLocal, self.formalLocal = self.configCFG.GetValue()
        if not isSuccess:
            wx.MessageBox("系统数据服务器还没正确配置，请您先设置数据服务器的相关参数！", "信息提示窗口")
            dbParameterSetupDLG = DataBaseParameterSetupDialog(self, self.witchDB, self.testCloud, self.formalCloud,
                                                               self.testLocal, self.formalLocal)
            dbParameterSetupDLG.Centre()
            if dbParameterSetupDLG.ShowModal() == wx.ID_OK:
                witchDB, testCloud, formalCloud, testLocal, formalLocal = dbParameterSetupDLG.GetValue()
                self.configCFG.UpdateValue(witchDB, testCloud, formalCloud, testLocal, formalLocal)
            dbParameterSetupDLG.Destroy()

    def Connect(self):
        try:
            if self.witchDB == 0:  # TEST_LOCAL_DB
                database = self.formalCloud
            elif self.witchDB == 1:  # TEST_CLOUD_DB
                database = self.testCloud
            elif self.witchDB == 2:  # FORMAL_LOCAL_DB
                database = self.formalLocal
            else:
                database = self.testLocal
            self.db = MySQLdb.connect(host=database[0], user=database[1], passwd=database[2],
                                      db=database[3], charset=database[4])
        except:
            return ID_DB_CONNECT_ERROR, ''
        self.cursor = self.db.cursor()
        self.cursor.execute("SELECT VERSION()")
        data = self.cursor.fetchone()
        return ID_NO_ERROR, data


class OurchatDB(DataBase):
    def __init__(self):
        keyword = 'OurChatDB'
        DataBase.__init__(self, keyword)

    def GetCPUId(self, myId):
        error, data = self.Connect()
        data = []
        if error == ID_NO_ERROR:
            sql = "select `登录状态` from user where `Id` = %s" % myId
            try:
                self.cursor.execute(sql)
            except:
                self.db.rollback()
                error = ID_DB_TABLE_RAEAD_ERROR
            else:
                data = self.cursor.fetchone()
                if data:
                    data = data[0]
            self.db.close()
        return error, data

    def UpdateCPUId(self, myId, cpuId):
        error, data = self.Connect()
        if error == ID_NO_ERROR:
            sql = "UPDATE user SET `登录状态` = '%s' where `Id` = %s" % (cpuId, myId)
            try:
                self.cursor.execute(sql)
                self.db.commit()
            except:
                self.db.rollback()
                error = ID_DB_TABLE_UPDATE_ERROR
            self.db.close()
        return error

    def GetFriendMessageOutlook(self, myId, friendId):
        error, data = self.Connect()
        num = 0
        lastMessage = ''
        lastTime = None
        data = []
        if error == ID_NO_ERROR:
            sql = "select `对话`, `时间` from ourchat " \
                  "where  `Id` = %s and `对象`=%s  and `未读`= 'TRUE' order by `Index` ASC" % (friendId, myId)
            try:
                self.cursor.execute(sql)
            except:
                self.db.rollback()
                error = ID_DB_TABLE_RAEAD_ERROR
            else:
                data = self.cursor.fetchall()
                num = self.cursor.rowcount
                sql = "select `对话`, `时间` from ourchat " \
                      "where  (`Id` = %s and `对象`=%s) or (`Id` = %s and `对象`=%s) order by `Index` DESC" % (
                          friendId, myId, myId, friendId)
                self.cursor.execute(sql)
                data = self.cursor.fetchone()
                if data:
                    lastMessage, lastTime = data
                else:
                    lastMessage = ""
                    lastTime = ""
            self.db.close()
        return error, friendId, num, lastMessage, lastTime

    def GetFriendInfo(self, userId):
        error, data = self.Connect()
        data = []
        if error == ID_NO_ERROR:
            sql = "select `Id`,`姓名`,`昵称`,`头像`,`地区` from user where `Id` = %s" % userId
            try:
                self.cursor.execute(sql)
            except:
                self.db.rollback()
                error = ID_DB_TABLE_RAEAD_ERROR
            else:
                data = self.cursor.fetchone()
            self.db.close()
        return error, data

    def GetMyOwnInfo(self, userId):
        error, data = self.Connect()
        data = []
        if error == ID_NO_ERROR:
            sql = "select `昵称`,`姓名`,`密码`,`好友列表`,`头像`,`地区` from user where `Id` = %s" % userId
            try:
                self.cursor.execute(sql)
            except:
                self.db.rollback()
                error = ID_DB_TABLE_RAEAD_ERROR
            else:
                data = self.cursor.fetchone()
            self.db.close()
        return error, data

    def GetUserInfo(self):
        error, data = self.Connect()
        data = []
        if error == ID_NO_ERROR:
            sql = "select `Id`,`昵称`,`姓名`,`密码`,`头像` from user"
            try:
                self.cursor.execute(sql)
            except:
                self.db.rollback()
                error = ID_DB_TABLE_RAEAD_ERROR
            else:
                data = self.cursor.fetchall()
            self.db.close()
        return error, data

    def SaveMessage(self, userId, messageContents, messageObject):
        messageTime = ''
        error, data = self.Connect()
        if error == ID_NO_ERROR:
            sql = "INSERT INTO ourchat(`Id`,`对话`,`对象`,`时间`)VALUES (%s,'%s',%s,CURRENT_TIMESTAMP)" % (
                userId, messageContents, messageObject)
            try:
                self.cursor.execute(sql)
                self.db.commit()  # 必须有，没有的话插入语句不会执行
            except:
                self.db.rollback()
                error = ID_DB_TABLE_UPDATE_ERROR
            self.db.close()
        return error

    def UpdateNickName(self, userId, nickName):
        messageTime = ''
        error, data = self.Connect()
        if error == ID_NO_ERROR:
            sql = "UPDATE user SET `昵称` = '%s' where `Id` = %s" % (nickName, userId)
            try:
                self.cursor.execute(sql)
                self.db.commit()
            except:
                self.db.rollback()
                error = ID_DB_TABLE_UPDATE_ERROR
            self.db.close()
        return error

    def UpdatePassword(self, userId, newPassword):
        error, data = self.Connect()
        if error == ID_NO_ERROR:
            sql = "UPDATE user SET `密码` = '%s' where `Id` = %s" % (newPassword, userId)
            try:
                self.cursor.execute(sql)
                self.db.commit()
            except:
                self.db.rollback()
                error = ID_DB_TABLE_UPDATE_ERROR
            self.db.close()
        return error

    def ReadMessages(self, userId, objectUserId):
        error, data = self.Connect()
        data = []
        if error == ID_NO_ERROR:
            sql = "select `Index`,`Id`,`时间`,`对话`,`对象` from ourchat " \
                  "where (`Id` = %s and `对象`=%s) or (`Id` = %s and `对象`=%s) order by `Index` asc" % (
                      userId, objectUserId, objectUserId, userId)
            try:
                self.cursor.execute(sql)
            except:
                self.db.rollback()
                error = ID_DB_TABLE_RAEAD_ERROR
            else:
                data = self.cursor.fetchall()
            self.db.close()
        return error, data

    def UpdateMessagesHaveRead(self, userId, objectUserId):
        error, data = self.Connect()
        if error == ID_NO_ERROR:  # UPDATE info_parameter SET express = %s
            sql = "UPDATE ourchat SET `未读` = 'FALSE'" \
                  "where (`Id` = %s and `对象`=%s) or (`Id` = %s and `对象`=%s) order by `Index` asc" % (
                      userId, objectUserId, objectUserId, userId)
            try:
                self.cursor.execute(sql)
                self.db.commit()
            except:
                self.db.rollback()
                error = ID_DB_TABLE_RAEAD_ERROR
            else:
                data = self.cursor.fetchall()
            self.db.close()
        return error

    def ReadNewMessages(self, lastId, userId, objectUserId):
        error, data = self.Connect()
        data = []
        if error == ID_NO_ERROR:
            # sql = "select `Index`,`Id`,`时间`,`对话`,`对象` from ourchat where `Index`>%s order by `Index` asc"%lastId
            sql = "select `Index`,`Id`,`时间`,`对话`,`对象` from ourchat " \
                  "where ((`Id` = %s and `对象`=%s) or (`Id` = %s and `对象`=%s)) and `Index`>%s order by `Index` asc" % (
                      userId, objectUserId, objectUserId, userId, lastId)
            try:
                self.cursor.execute(sql)
            except:
                self.db.rollback()
                error = ID_DB_TABLE_RAEAD_ERROR
            else:
                data = self.cursor.fetchall()
            self.db.close()
        return error, data

    def SaveIcon(self, myId, myIcon):
        error, data = self.Connect()
        if error == ID_NO_ERROR:
            sql = "UPDATE user SET `头像` = '%s' where `Id` = %s" % (myIcon, myId)
            try:
                self.cursor.execute(sql)
                self.db.commit()
            except:
                self.db.rollback()
                error = ID_DB_TABLE_UPDATE_ERROR
            self.db.close()
        return error


class DataBaseParameterSetupDialog(wx.Dialog):
    def __init__(self, parent, witchDB, testCloud, formalCloud, testLocal, formalLocal):
        wx.Dialog.__init__(self)
        self.witchDB = witchDB = 0
        self.SetExtraStyle(wx.DIALOG_EX_METAL)
        # parent, id, title, pos, size, style, name
        self.Create(None, -1, "数据库参数设置窗口", pos=wx.DefaultPosition, size=(645, 400), style=wx.DEFAULT_DIALOG_STYLE,
                    name="DBSetup")
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add((-1, 10))
        hbox = wx.BoxSizer()
        hbox.Add((20, -1))
        hbox.Add(wx.StaticText(self, -1, "要使用的数据库服务器位置："), 0, wx.TOP, 3)
        hbox.Add((20, -1))
        self.serverPositionCOMBO = wx.ComboBox(self, -1, value="本地", size=(100, 25), choices=["本地", "云端"])
        self.serverPositionCOMBO.SetSelection(self.witchDB % 2)
        hbox.Add(self.serverPositionCOMBO, wx.LEFT, 10)
        hbox.Add((30, -1))
        hbox.Add(wx.StaticText(self, -1, "要使用的数据库服务器类型："), 0, wx.TOP, 3)
        self.serverTypeCOMBO = wx.ComboBox(self, -1, value="测试", size=(100, 25), choices=["测试", "运行"])
        self.serverTypeCOMBO.SetSelection(self.witchDB / 2)
        hbox.Add((20, -1))
        hbox.Add(self.serverTypeCOMBO, wx.LEFT, 10)
        vbox.Add(hbox)
        vbox.Add((-1, 5))
        hbox = wx.BoxSizer()
        hbox.Add((10, -1))
        self.testLocalPNL = MySQLDBServerPararmeterPanel(self, title="本地测试服务器: ", value=testLocal)
        hbox.Add(self.testLocalPNL)
        hbox.Add((5, -1))
        self.testCloudPNL = MySQLDBServerPararmeterPanel(self, title="云端测试服务器: ", value=testCloud)
        hbox.Add(self.testCloudPNL)
        vbox.Add(hbox)
        hbox = wx.BoxSizer()
        hbox.Add((10, -1))
        self.formalLocalPNL = MySQLDBServerPararmeterPanel(self, title="本地运行服务器: ", value=formalLocal)
        hbox.Add(self.formalLocalPNL)
        hbox.Add((5, -1))
        self.formalCloudPNL = MySQLDBServerPararmeterPanel(self, title="云端运行服务器: ", value=formalCloud)
        hbox.Add(self.formalCloudPNL)
        vbox.Add(hbox)
        self.SetSizer(vbox)
        line = wx.StaticLine(self, -1, size=(20, -1), style=wx.LI_HORIZONTAL)
        vbox.Add(line, 0, wx.GROW | wx.RIGHT | wx.TOP, 5)
        btnsizer = wx.StdDialogButtonSizer()
        okBTN = wx.Button(self, wx.ID_OK, '确定', size=(200, 30))
        okBTN.SetDefault()
        btnsizer.AddButton(okBTN)
        cancelBTN = wx.Button(self, wx.ID_CANCEL, '取消', size=(200, 30))
        btnsizer.AddButton(cancelBTN)
        btnsizer.Realize()
        vbox.Add(btnsizer, 1, wx.ALIGN_CENTER | wx.ALL, 5)
        self.SetSizer(vbox)
        self.SetSelectionColour()
        self.Bind(wx.EVT_COMBOBOX, self.OnComboChanged)
        okBTN.Bind(wx.EVT_BUTTON, self.OnOk)

    def OnOk(self, event):
        event.Skip()

    def OnComboChanged(self, event):
        self.witchDB = self.serverTypeCOMBO.GetSelection() * 2 + self.serverPositionCOMBO.GetSelection()
        self.SetSelectionColour()

    def SetSelectionColour(self):
        if self.witchDB == 0:
            self.testLocalPNL.SetBackgroundColour(wx.Colour('pink'))
            self.testCloudPNL.SetBackgroundColour(wx.Colour(240, 240, 240))
            self.formalLocalPNL.SetBackgroundColour(wx.Colour(240, 240, 240))
            self.formalCloudPNL.SetBackgroundColour(wx.Colour(240, 240, 240))
        elif self.witchDB == 1:
            self.testLocalPNL.SetBackgroundColour(wx.Colour(240, 240, 240))
            self.testCloudPNL.SetBackgroundColour(wx.Colour('pink'))
            self.formalLocalPNL.SetBackgroundColour(wx.Colour(240, 240, 240))
            self.formalCloudPNL.SetBackgroundColour(wx.Colour(240, 240, 240))
        elif self.witchDB == 2:
            self.testLocalPNL.SetBackgroundColour(wx.Colour(240, 240, 240))
            self.testCloudPNL.SetBackgroundColour(wx.Colour(240, 240, 240))
            self.formalLocalPNL.SetBackgroundColour(wx.Colour('pink'))
            self.formalCloudPNL.SetBackgroundColour(wx.Colour(240, 240, 240))
        else:
            self.testLocalPNL.SetBackgroundColour(wx.Colour(240, 240, 240))
            self.testCloudPNL.SetBackgroundColour(wx.Colour(240, 240, 240))
            self.formalLocalPNL.SetBackgroundColour(wx.Colour(240, 240, 240))
            self.formalCloudPNL.SetBackgroundColour(wx.Colour('pink'))
        self.Refresh()

    def GetValue(self):
        self.witchDB = self.serverTypeCOMBO.GetSelection() * 2 + self.serverPositionCOMBO.GetSelection()
        testLocal = self.testLocalPNL.GetValue()
        testCloud = self.testCloudPNL.GetValue()
        formalLocal = self.formalLocalPNL.GetValue()
        formalCloud = self.formalCloudPNL.GetValue()
        return self.witchDB, testCloud, formalCloud, testLocal, formalLocal


class MySQLDBServerPararmeterPanel(wx.Panel):
    def __init__(self, parent, title, value=None):
        if value is None:
            value = ['', '', '', '']
        size = (300, 130)
        wx.Panel.__init__(self, parent, -1, size=size)
        vbox = wx.BoxSizer(wx.VERTICAL)
        staticBOX = wx.StaticBox(self, -1, label=title, size=size)
        vvbox = wx.BoxSizer(wx.VERTICAL)
        vvbox.Add((-1, 10))
        hhbox = wx.BoxSizer()
        hhbox.Add((15, -1))
        hhbox.Add(wx.StaticText(staticBOX, -1, label="IP地址:", size=(50, -1)), 0, wx.TOP, 3)
        hhbox.Add((5, -1))
        self.ipTXT = IPTextCtrl(staticBOX, -1, IP=value[0], size=(150, 25))
        hhbox.Add(self.ipTXT)
        vvbox.Add(hhbox, 0, wx.TOP, 10)
        hhbox = wx.BoxSizer()
        hhbox.Add((15, -1))
        hhbox.Add(wx.StaticText(staticBOX, -1, label="用户名：", size=(50, -1)), 0, wx.TOP, 3)
        hhbox.Add((5, -1))
        self.userNameTXT = wx.TextCtrl(staticBOX, -1, value=value[1], size=(75, 25))
        hhbox.Add(self.userNameTXT)
        hhbox.Add((10, -1))
        hhbox.Add(wx.StaticText(staticBOX, -1, label="密码：", size=(50, -1)), 0, wx.TOP, 3)
        hhbox.Add((5, -1))
        self.pswTXT = wx.TextCtrl(staticBOX, -1, value=value[2], size=(75, 25))
        hhbox.Add(self.pswTXT)
        vvbox.Add(hhbox, 0, wx.TOP, 5)
        hhbox = wx.BoxSizer()
        hhbox.Add((15, -1))
        hhbox.Add(wx.StaticText(staticBOX, -1, label="数据库：", size=(50, -1)), 0, wx.TOP, 3)
        hhbox.Add((5, -1))
        self.dbTXT = wx.TextCtrl(staticBOX, -1, value=value[3], size=(75, 25))
        hhbox.Add(self.dbTXT)
        hhbox.Add((10, -1))
        hhbox.Add(wx.StaticText(staticBOX, -1, label="字符集：", size=(50, -1)), 0, wx.TOP, 3)
        hhbox.Add((5, -1))
        self.charSetCOMBO = wx.ComboBox(staticBOX, -1, value=value[4], size=(75, 25),
                                        choices=["utf8", "gbk", 'unicode'])
        hhbox.Add(self.charSetCOMBO)
        vvbox.Add(hhbox, 0, wx.TOP, 10)
        staticBOX.SetSizer(vvbox)
        vbox.Add(staticBOX)
        self.SetSizer(vbox)

    def GetValue(self):
        value = [self.ipTXT.GetValue(), self.userNameTXT.GetValue(), self.pswTXT.GetValue(), self.dbTXT.GetValue(),
                 self.charSetCOMBO.GetValue()]
        return value


class IPTextCtrl(wx.Panel):
    def __init__(self, parent, id, IP, size, log=None):
        wx.Panel.__init__(self, parent, id, size)
        self.log = log
        hbox = wx.BoxSizer()
        self.CTRL = []
        for i in range(4):
            ctrl = wx.TextCtrl(self, -1, size=(40, -1), style=wx.TE_CENTRE)
            ctrl.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
            ctrl.Bind(wx.EVT_CHAR, self.OnChar)
            self.CTRL.append(ctrl)
            hbox.Add(ctrl, 0)
            if i < 3:
                hbox.Add(wx.StaticText(self, label="."), 0, wx.ALL, 8)
        self.SetValue(IP)
        self.SetSizer(hbox)

    def GetValue(self):
        values = '%s.%s.%s.%s' % (
            self.CTRL[0].GetValue(), self.CTRL[1].GetValue(), self.CTRL[2].GetValue(), self.CTRL[3].GetValue())
        return values

    def OnChar(self, evt):
        keycode = evt.GetKeyCode()
        if keycode == 46:  # 按键'.'
            for i in range(3):
                if self.CTRL[i].HasFocus():
                    ls = self.CTRL[i].GetValue()
                    # self.CTRL[i].SetValue(ls)
                    self.CTRL[i + 1].SetFocus()
                    self.CTRL[i + 1].SetSelection(0, -1)
                    break
        else:
            evt.Skip()
        # self.GetParent().keylog.LogKeyEvent("Char", evt)

    def OnKillFocus(self, event):
        error = False
        for i in self.CTRL:
            j = i.GetValue()
            for k in j:
                if k not in string.digits:
                    i.SetBackgroundColour('pink')
                    i.SetFocus()
                    error = True
                    break
                else:
                    i.SetBackgroundColour('white')
            if error:
                wx.Bell()
                break
        if not error:
            event.Skip()

    def SetValue(self, value):
        if value == "":
            ip_list = ['', '', '', '']
        else:
            ip_list = value.split('.')
        for i in range(4):
            self.CTRL[i].SetValue(ip_list[i])


class MyValidator(wx.Validator):
    def __init__(self, flag=None, pyVar=None):
        wx.Validator.__init__(self)
        self.flag = flag
        self.Bind(wx.EVT_CHAR, self.OnChar)

    def Clone(self):
        return MyValidator(self.flag)

    def Validate(self, win):
        tc = self.GetWindow()
        val = tc.GetValue()

        if self.flag == ALPHA_ONLY:
            for x in val:
                if x not in string.ascii_letters:
                    return False

        elif self.flag == DIGIT_ONLY:
            for x in val:
                if x not in string.digits:
                    return False

        elif self.flag == IP_ONLY:
            for x in val:
                if x not in string.digits + '.':
                    return False

        return True

    def OnChar(self, event):
        key = event.GetKeyCode()

        if key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255:
            event.Skip()
            return

        if self.flag == ALPHA_ONLY and chr(key) in string.ascii_letters:
            event.Skip()
            return

        if self.flag == DIGIT_ONLY and chr(key) in string.digits:
            event.Skip()
            return

        if self.flag == IP_ONLY and chr(key) in string.digits + '.':
            event.Skip()
            return

        if not wx.Validator.IsSilent():
            wx.Bell()

        return
