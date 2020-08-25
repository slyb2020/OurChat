import wx
import os
# dirName = os.path.dirname(os.path.abspath(__file__))
# bitmapDir = os.path.join(dirName, 'bitmaps')
# sys.path.append(os.path.split(dirName)[0])
ICO_PATH = os.path.abspath('.\\')+'\\ico48\\'
USER_PATH = os.path.abspath('.\\')+'\\user\\'
DEFAULT_PATH = os.path.abspath('.\\')
VERSION = '0.20200725A'

ALPHA_ONLY = 1
DIGIT_ONLY = 2
FLOAT_ONLY = 3
SIGNED_FLOAT_ONLY = 4
EXPRESS_ONLY=5
IP_ONLY=6

ID_WINDOW_LEFT = wx.NewIdRef()
ID_NO_ERROR = wx.NewIdRef()
ID_DB_CONNECT_ERROR = wx.NewIdRef()
ID_DB_TABLE_UPDATE_ERROR = wx.NewIdRef()
ID_DB_TABLE_RAEAD_ERROR = wx.NewIdRef()
ID_SETUP_PSWD = wx.NewIdRef()
ID_CHECKOUT = wx.NewIdRef()
ID_CHECKIN = wx.NewIdRef()
ID_SETUP_PROPERTY = wx.NewIdRef()
ID_HELP = wx.NewIdRef()
licenseText = "blah " * 25 + "\n\n" + "yadda " * 10
