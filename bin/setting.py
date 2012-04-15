#! /usr/bin/python

'''
Filename: setting.py
Author: Muchtar Suhari Putra (muchtarsputra at gmail.com)
Create: 4 Januari 2011
Description: Main program
'''

import wx, os, time
#import wx.lib.flatnotebook as fnb
import flatnotebook as fnb
import ConfigParser
from function import *

info = "PyCTC 1.0 - CENTRAL TRAIN CONTROL"
fileicon = "pyctc.ico"
fileconfig = "bin/pywit.conf"

listCom = ['COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8']

listChannel = {
	101: ['DigitalIn0', 'COM0'], 
	102: ['DigitalIn1', 'COM1'], 
	103: ['DigitalIn2', 'COM2'], 
	104: ['DigitalIn3', 'COM3'],
	105: ['DigitalIn4', 'COM4'],
	106: ['DigitalOut0', 'COM5'],
	107: ['DigitalOut1', 'COM6'],
	108: ['DigitalOut2', 'COM7'],
	109: ['DigitalOut3', 'COM8'],
	110: ['DigitalOut4', 'COM9']
	}


class PanelChannel(wx.Panel):
	def __init__(self, parent, id, title = 'default', value = '0'):
		wx.Panel.__init__(self, parent, -1)
		
		self.txt_title  = wx.StaticText(self, -1, title, size = (70,-1))
		self.edit       = wx.TextCtrl(self, -1, '0')
		self.ch         = wx.Choice(self, -1, choices = listCom, size=(70,-1))
		self.editAlarmH = wx.TextCtrl(self, -1, '0')
		self.editAlarmL = wx.TextCtrl(self, -1, '0')
		
		sizer = wx.BoxSizer(wx.HORIZONTAL)
		sizer.Add(self.txt_title, 0, wx.EXPAND | wx.ALL, 2)
		sizer.Add(self.edit, 0, wx.EXPAND | wx.ALL, 2)
		sizer.Add(self.ch, 0, wx.EXPAND | wx.ALL, 2)
		sizer.Add(self.editAlarmH, 0, wx.EXPAND | wx.ALL, 2)
		sizer.Add(self.editAlarmL, 0, wx.EXPAND | wx.ALL, 2)
		
		board = wx.BoxSizer(wx.VERTICAL)
		board.Add(sizer, 1, wx.EXPAND | wx.ALL, 2)

		border = wx.BoxSizer()
		border.Add(board, 1, wx.EXPAND | wx.ALL, 0)
		self.SetSizer(border)
		self.Layout()
		
	def SetTitle(self, title):
		self.txt_title.SetLabel(title)
		
	def SetValue(self, data):
		self.edit.SetValue(data)
		
	def GetValue(self):
		return '%s' % self.edit.GetValue()
		
		
class PanelSetChannel(wx.Panel):
	def __init__(self, parent, id, title = 'default', value = '0'):
		wx.Panel.__init__(self, parent, -1)
		color = wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE)
		self.SetBackgroundColour(color)

		self.config_sensor1  = ''
		self.config_sensor2  = ''
		self.config_sensor3  = ''
		self.config_sensor4  = ''
		self.config_sensor5  = ''
		self.config_sensor6  = ''
		self.config_sensor7  = ''
		self.config_sensor8  = ''
		self.config_sensor9  = ''
		self.config_sensor10 = ''

		self.DigitalIn0 = PanelChannel(self, -1)
		self.DigitalIn1 = PanelChannel(self, -1)
		self.DigitalIn2 = PanelChannel(self, -1)
		self.DigitalIn3 = PanelChannel(self, -1)
		self.DigitalIn4 = PanelChannel(self, -1)
		self.DigitalOut0 = PanelChannel(self, -1)
		self.DigitalOut1 = PanelChannel(self, -1)
		self.DigitalOut2 = PanelChannel(self, -1)
		self.DigitalOut3 = PanelChannel(self, -1)
		self.DigitalOut4 = PanelChannel(self, -1)
		
		pnlMain = wx.BoxSizer(wx.VERTICAL)
		pnlMain.Add(self.DigitalIn0, 0, wx.EXPAND | wx.ALL, 1)
		pnlMain.Add(self.DigitalIn1, 0, wx.EXPAND | wx.ALL, 1)
		pnlMain.Add(self.DigitalIn2, 0, wx.EXPAND | wx.ALL, 1)
		pnlMain.Add(self.DigitalIn3, 0, wx.EXPAND | wx.ALL, 1)
		pnlMain.Add(self.DigitalIn4, 0, wx.EXPAND | wx.ALL, 1)
		pnlMain.Add(self.DigitalOut0, 0, wx.EXPAND | wx.ALL, 1)
		pnlMain.Add(self.DigitalOut1, 0, wx.EXPAND | wx.ALL, 1)
		pnlMain.Add(self.DigitalOut2, 0, wx.EXPAND | wx.ALL, 1)
		pnlMain.Add(self.DigitalOut3, 0, wx.EXPAND | wx.ALL, 1)
		pnlMain.Add(self.DigitalOut4, 0, wx.EXPAND | wx.ALL, 1)
		
		self.GetConfig()
		
		self.txt_title  = wx.StaticText(self, -1, 'Sensor Name', size=(60, -1))
		self.txt_name   = wx.StaticText(self, -1, 'Sensor Name Display', size=(90, -1))
		self.txt_port   = wx.StaticText(self, -1, 'Port', size=(60, -1))
		self.txt_alarmH = wx.StaticText(self, -1, 'Alarm High', size=(70, -1))
		self.txt_alarmL = wx.StaticText(self, -1, 'Alarm Low', size=(70, -1))
		stline = wx.StaticLine(self, -1, style=wx.LI_HORIZONTAL)
		
		pnlText = wx.BoxSizer(wx.HORIZONTAL)
		pnlText.Add(self.txt_title, 1, wx.EXPAND | wx.ALL, 2)
		pnlText.Add(self.txt_name, 1, wx.EXPAND | wx.ALL, 2)
		pnlText.Add(self.txt_port, 1, wx.EXPAND | wx.ALL, 2)
		pnlText.Add(self.txt_alarmH, 1, wx.EXPAND | wx.ALL, 2)
		pnlText.Add(self.txt_alarmL, 1, wx.EXPAND | wx.ALL, 2)
		
		#Layout utama
		pnlbox = wx.BoxSizer(wx.VERTICAL)
		pnlbox.Add(pnlText, 0, wx.EXPAND | wx.ALL, 2)
		pnlbox.Add(stline, 0, wx.EXPAND | wx.ALL, 2)
		pnlbox.Add(pnlMain, 0, wx.EXPAND | wx.ALL, 2)

		pnlborder = wx.BoxSizer()
		pnlborder.Add(pnlbox, 1, wx.EXPAND | wx.ALL, 0)
		self.SetSizer(pnlborder)
		self.Layout()
		
	def GetConfig(self):
		config = ConfigParser.ConfigParser()
		config.read(fileconfig)

		self.config_sensor1  = config.get('MAIN', 'sensor1_title', 0)
		self.config_sensor2  = config.get('MAIN', 'sensor2_title', 0)
		self.config_sensor3  = config.get('MAIN', 'sensor3_title', 0)
		self.config_sensor4  = config.get('MAIN', 'sensor4_title', 0)
		self.config_sensor5  = config.get('MAIN', 'sensor5_title', 0)
		self.config_sensor6  = config.get('MAIN', 'sensor6_title', 0)
		self.config_sensor7  = config.get('MAIN', 'sensor7_title', 0)
		self.config_sensor8  = config.get('MAIN', 'sensor8_title', 0)
		self.config_sensor9  = config.get('MAIN', 'sensor9_title', 0)
		self.config_sensor10 = config.get('MAIN', 'sensor10_title', 0)
		
		self.sensor1_value = config.get('MAIN', 'sensor1_value', 0)
		self.sensor2_value = config.get('MAIN', 'sensor2_value', 0)
		self.sensor3_value = config.get('MAIN', 'sensor3_value', 0)
		self.sensor4_value = config.get('MAIN', 'sensor4_value', 0)
		self.sensor5_value = config.get('MAIN', 'sensor5_value', 0)
		self.sensor6_value = config.get('MAIN', 'sensor6_value', 0)
		self.sensor7_value = config.get('MAIN', 'sensor7_value', 0)
		self.sensor8_value = config.get('MAIN', 'sensor8_value', 0)
		self.sensor9_value = config.get('MAIN', 'sensor9_value', 0)
		self.sensor10_value = config.get('MAIN', 'sensor10_value', 0)
		
		self.DigitalIn0.SetTitle(self.config_sensor1)
		self.DigitalIn1.SetTitle(self.config_sensor2)
		self.DigitalIn2.SetTitle(self.config_sensor3)
		self.DigitalIn3.SetTitle(self.config_sensor4)
		self.DigitalIn4.SetTitle(self.config_sensor5)
		self.DigitalOut0.SetTitle(self.config_sensor6)
		self.DigitalOut1.SetTitle(self.config_sensor7)
		self.DigitalOut2.SetTitle(self.config_sensor8)
		self.DigitalOut3.SetTitle(self.config_sensor9)
		self.DigitalOut4.SetTitle(self.config_sensor10)

		self.DigitalIn0.SetValue(self.sensor1_value)
		self.DigitalIn1.SetValue(self.sensor2_value)
		self.DigitalIn2.SetValue(self.sensor3_value)
		self.DigitalIn3.SetValue(self.sensor4_value)
		self.DigitalIn4.SetValue(self.sensor5_value)
		self.DigitalOut0.SetValue(self.sensor6_value)
		self.DigitalOut1.SetValue(self.sensor7_value)
		self.DigitalOut2.SetValue(self.sensor8_value)
		self.DigitalOut3.SetValue(self.sensor9_value)
		self.DigitalOut4.SetValue(self.sensor10_value)
		
	def SetConfig(self):
		config = ConfigParser.RawConfigParser()
		config.read(fileconfig)
		
		config_sensor1  = self.DigitalIn0.GetValue()
		config_sensor2  = self.DigitalIn1.GetValue()
		config_sensor3  = self.DigitalIn2.GetValue()
		config_sensor4  = self.DigitalIn3.GetValue()
		config_sensor5  = self.DigitalIn4.GetValue()
		config_sensor6  = self.DigitalOut0.GetValue()
		config_sensor7  = self.DigitalOut1.GetValue()
		config_sensor8  = self.DigitalOut2.GetValue()
		config_sensor9  = self.DigitalOut3.GetValue()
		config_sensor10 = self.DigitalOut4.GetValue()

		#config.add_section('MAIN')
		config.set('MAIN', 'sensor1_value', config_sensor1)
		config.set('MAIN', 'sensor2_value', config_sensor2)
		config.set('MAIN', 'sensor3_value', config_sensor3)
		config.set('MAIN', 'sensor4_value', config_sensor4)
		config.set('MAIN', 'sensor5_value', config_sensor5)
		config.set('MAIN', 'sensor6_value', config_sensor6)
		config.set('MAIN', 'sensor7_value', config_sensor7)
		config.set('MAIN', 'sensor8_value', config_sensor8)
		config.set('MAIN', 'sensor9_value', config_sensor9)
		config.set('MAIN', 'sensor10_value', config_sensor10)

		#Writing configuration file
		with open(fileconfig, 'wb') as configfile:
			config.write(configfile)


class PanelSetPreferences(wx.Panel):
	def __init__(self, parent, id):
		wx.Panel.__init__(self, parent, -1)
		color = wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE)
		self.SetBackgroundColour(color)
		
		#initial
		self.useProxy = False
		self.maplocation = ''
		
		self.txt_map  = wx.StaticText(self, -1, 'Map Location', size = (100,-1))
		self.edit_map = wx.TextCtrl(self, -1, '-')
		self.check = wx.CheckBox(self, -1, 'Use Proxy')

		self.txt_proxy      = wx.StaticText(self, -1, 'HTTP Proxy')
		self.edit_proxy     = wx.TextCtrl(self, -1, '', size = (140,-1))
		self.txt_proxyport  = wx.StaticText(self, -1, 'Port')
		self.edit_proxyport = wx.TextCtrl(self, -1, '', size = (60,-1))
		self.txt_username   = wx.StaticText(self, -1, 'Username')
		self.edit_username  = wx.TextCtrl(self, -1, '', size = (140,-1))
		self.txt_password   = wx.StaticText(self, -1, 'Password')
		self.edit_password  = wx.TextCtrl(self, -1, '', size = (140,-1), style = wx.TE_PASSWORD)
		
		sizer = wx.BoxSizer(wx.HORIZONTAL)
		sizer.Add(self.txt_map, 0, wx.EXPAND | wx.ALL, 2)
		sizer.Add(self.edit_map, 1, wx.EXPAND | wx.ALL, 2)
		
		sizerProxy = wx.FlexGridSizer(0,4,0,0)
		sizerProxy.Add(self.txt_proxy, 0, wx.EXPAND | wx.ALL, 4)
		sizerProxy.Add(self.edit_proxy, 0, wx.EXPAND | wx.ALL, 4)
		sizerProxy.Add(self.txt_proxyport, 0, wx.EXPAND | wx.ALL, 4)
		sizerProxy.Add(self.edit_proxyport, 0, wx.EXPAND | wx.ALL, 4)
		sizerProxy.Add(self.txt_username, 0, wx.EXPAND | wx.ALL, 4)
		sizerProxy.Add(self.edit_username, 0, wx.EXPAND | wx.ALL, 4)
		sizerProxy.Add((10,10))
		sizerProxy.Add((10,10))
		sizerProxy.Add(self.txt_password, 0, wx.EXPAND | wx.ALL, 4)
		sizerProxy.Add(self.edit_password, 0, wx.EXPAND | wx.ALL, 4)

		sbProxy = wx.StaticBox(self, -1, 'Proxy Setting')
		bsb = wx.StaticBoxSizer(sbProxy, wx.VERTICAL)
		bsb.Add(sizerProxy, 0, wx.EXPAND | wx.ALL, 0)

		pnlMain = wx.BoxSizer(wx.VERTICAL)
		pnlMain.Add(sizer, 0, wx.EXPAND | wx.ALL, 2)
		pnlMain.Add(self.check, 0, wx.EXPAND | wx.ALL, 2)
		pnlMain.Add(bsb, 0, wx.EXPAND | wx.ALL, 2)

		#Layout utama
		pnlbox = wx.BoxSizer(wx.VERTICAL)
		pnlbox.Add(pnlMain, 1, wx.EXPAND | wx.ALL, 2)

		pnlborder = wx.BoxSizer()
		pnlborder.Add(pnlbox, 1, wx.EXPAND | wx.ALL, 0)
		self.SetSizer(pnlborder)
		self.Layout()
		
		self.GetConfig()
		self.SetEnable()
		self.Bind(wx.EVT_CHECKBOX, self.OnCheckProxy, self.check)
		
	def GetConfig(self):
		config = ConfigParser.ConfigParser()
		config.read(fileconfig)
		self.maplocation = config.get('MAIN', 'map')
		
		self.edit_map.SetValue(self.maplocation)
		
	def SetConfig(self):
		pass
		
	def OnCheckProxy(self, event):
		self.SetEnable(event.IsChecked())

	def SetEnable(self, status=False):
		self.edit_proxy.Enable(status)
		self.edit_proxyport.Enable(status)
		self.edit_username.Enable(status)
		self.edit_password.Enable(status)
		

class SettingMain(wx.Dialog):
	def __init__(self, parent, id):
		wx.Dialog.__init__(self, parent, id, title="PyWIT 1.0 - Setting", size = (500,520))
		
		color = wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE)
		self.SetBackgroundColour(color)
		self.SetIcon(wx.Icon(fileicon, wx.BITMAP_TYPE_ICO))
		
		#initial
		self.maplocation = ''

		'''
		``FNB_VC71`` 0x1 Use Visual Studio 2003 (VC7.1) style for tabs.
		``FNB_FANCY_TABS`` 0x2 Use fancy style - square tabs filled with gradient colouring.
		``FNB_TABS_BORDER_SIMPLE`` 0x4 Draw thin border around the page.
		``FNB_NO_X_BUTTON`` 0x8 Do not display the 'X' button.
		``FNB_NO_NAV_BUTTONS`` 0x10 Do not display the right/left arrows.
		``FNB_MOUSE_MIDDLE_CLOSES_TABS`` 0x20 Use the mouse middle button for cloing tabs.
		``FNB_BOTTOM`` 0x40 Place tabs at bottom - the default is to place them at top.
		``FNB_NODRAG`` 0x80 Disable dragging of tabs.
		``FNB_VC8`` 0x100 Use Visual Studio 2005 (VC8) style for tabs.
		``FNB_X_ON_TAB`` 0x200 Place 'X' close button on the active tab.
		``FNB_BACKGROUND_GRADIENT`` 0x400 Use gradients to paint the tabs background.
		``FNB_COLOURFUL_TABS`` 0x800 Use colourful tabs (VC8 style only).
		``FNB_DCLICK_CLOSES_TABS`` 0x1000 Style to close tab using double click.
		``FNB_SMART_TABS`` 0x2000 Use `Smart Tabbing`, like ``Alt`` + ``Tab`` on Windows.
		``FNB_DROPDOWN_TABS_LIST`` 0x4000 Use a dropdown menu on the left in place of the arrows.
		``FNB_ALLOW_FOREIGN_DND`` 0x8000 Allows drag 'n' drop operations between different FlatNotebooks.
		``FNB_HIDE_ON_SINGLE_TAB`` 0x10000 Hides the Page Container when there is one or fewer tabs.
		``FNB_DEFAULT_STYLE`` 0x10020 FlatNotebook default style.
		``FNB_FF2`` 0x20000 Use Firefox 2 style for tabs.
		``FNB_NO_TAB_FOCUS`` 0x40000 Does not allow tabs to have focus.
		``FNB_RIBBON_TABS`` 0x80000 Use the Ribbon Tabs style
		'''

		self.fnBook = fnb.FlatNotebook(self, wx.ID_ANY, agwStyle = (fnb.FNB_NO_X_BUTTON | fnb.FNB_NO_NAV_BUTTONS | fnb.FNB_NODRAG | fnb.FNB_DEFAULT_STYLE))
		self.fnBook.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_APPWORKSPACE))

		self.pnlChannel     = PanelSetChannel(self.fnBook, -1)
		self.pnlPreferences = PanelSetPreferences(self.fnBook, -1)
		#self.pnlChannel.Enable(False)

		self.fnBook.AddPage(self.pnlChannel, 'Setting Channel', True, -1)
		self.fnBook.AddPage(self.pnlPreferences, 'Preferences', True, -1)
		self.fnBook.SetSelection(0)

		btn_save = wx.Button(self, -1, 'Save', size=(100, 30))
		btn_close = wx.Button(self, -1, 'Close', size=(100, 30))
		
		self.Bind(wx.EVT_BUTTON, self.OnSave, btn_save)
		self.Bind(wx.EVT_BUTTON, self.OnExit, btn_close)
		
		pnlButton = wx.BoxSizer(wx.HORIZONTAL)
		pnlButton.Add(btn_save, 1, wx.EXPAND | wx.ALL, 2)
		pnlButton.Add(btn_close, 1, wx.EXPAND | wx.ALL, 2)
		
		#Layout utama
		pnlbox = wx.BoxSizer(wx.VERTICAL)
		pnlbox.Add(self.fnBook, 1, wx.ALL | wx.ALIGN_CENTRE_HORIZONTAL, 4)
		pnlbox.Add(pnlButton, 0, wx.ALL | wx.ALIGN_RIGHT, 4)

		pnlborder = wx.BoxSizer()
		pnlborder.Add(pnlbox, 1, wx.EXPAND | wx.ALL, 0)
		self.SetSizer(pnlborder)
		self.Layout()
		
	def OnExit(self, event):
		self.Destroy()
		
	def GetConfig(self):
		self.config = ConfigParser.ConfigParser()
		self.config.read(fileconfig)
		oke =  self.config.get('MAIN', 'map', 0)
		config_sensor1  = self.config.get('MAIN', 'sensor1_title', 0)
		config_sensor2  = self.config.get('MAIN', 'sensor2_title', 0)
		config_sensor3  = self.config.get('MAIN', 'sensor3_title', 0)
		config_sensor4  = self.config.get('MAIN', 'sensor4_title', 0)
		config_sensor5  = self.config.get('MAIN', 'sensor5_title', 0)
		config_sensor6  = self.config.get('MAIN', 'sensor6_title', 0)
		config_sensor7  = self.config.get('MAIN', 'sensor7_title', 0)
		config_sensor8  = self.config.get('MAIN', 'sensor8_title', 0)
		config_sensor9  = self.config.get('MAIN', 'sensor9_title', 0)
		config_sensor10 = self.config.get('MAIN', 'sensor10_title', 0)
		
		self.maplocation = self.config.get('MAIN', 'map')

		self.DigitalIn0.SetTitle(config_sensor1)
		self.DigitalIn1.SetTitle(config_sensor2)
		self.DigitalIn2.SetTitle(config_sensor3)
		self.DigitalIn3.SetTitle(config_sensor4)
		self.DigitalIn4.SetTitle(config_sensor5)
		self.DigitalOut0.SetTitle(config_sensor6)
		self.DigitalOut1.SetTitle(config_sensor7)
		self.DigitalOut2.SetTitle(config_sensor8)
		self.DigitalOut3.SetTitle(config_sensor9)
		self.DigitalOut4.SetTitle(config_sensor10)
		
		return oke
		
	def SetConfig(self, data):
		pass
		
	def OnSave(self, event):
		#pass
		#val = self.GetConfig()
		#print self.config.get('MAIN', 'map', 0)
		self.pnlChannel.SetConfig()
	
		