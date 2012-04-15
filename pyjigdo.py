#! /usr/bin/env python

'''
Filename: pyjigdo.py
Author: Muchtar Suhari Putra (muchtarsputra at gmail.com)
Create: 11 April 2012
Description: Application program to download with Jigdo (Jigsaw Download)
'''

import wx
import bin.main as main

class MyApp(wx.App):
	def OnInit(self):
		win = main.MainForm(None, -1)
		win.Centre()
		#win.Maximize()
		win.Show(True)
		self.SetTopWindow(win)
		return True

app = MyApp()
app.MainLoop()