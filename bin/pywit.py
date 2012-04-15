#! /usr/bin/python

'''
Filename: pywit.py
Author: Muchtar Suhari Putra (muchtarsputra at gmail.com)
Create: 8 Januari 2011
Description: Class of pywit
'''

import wx, serial

SERIALRX = wx.NewEventType()
# bind to serial data receive events
EVT_SERIALRX = wx.PyEventBinder(SERIALRX, 0)

#Bind serial event to wx
class SerialRxEvent(wx.PyCommandEvent):
	eventType = SERIALRX
	
	def __init__(self, windowID, data):
		wx.PyCommandEvent.__init__(self, self.eventType, windowID)
		self.data = data
		
	def Clone(self):
		self.__class__(self.GetId(), self.data)
		

class PyWIT:
	def __init__(self):
		self.__value = 0
		
		#Event Serial
		#self.Bind(EVT_SERIALRX, self.OnSerialRead)
		
	def Open(self):
		pass
		
	def Close(self):
		pass
		
	def Connect(self):
		pass
		
	def Disconnect(self):
		pass
		
	def Write(self):
		pass
		
	def Read(self):
		pass
		
	def SetValue(self, value = 1):
		self.__value += value
		
	def GetValue(self):
		return self.__value
		
	def OnSerialRead(self, event):
		pass
		