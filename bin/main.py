#! /usr/bin/env python

'''
Filename: main.py
Author: Muchtar Suhari Putra (muchtarsputra at gmail.com)
Create: 11 April 2012
Description: Main program
'''

import wx, os, sys, time
import wx.grid as grid
import urllib2
import thread
from random import randint as rand
import random
import wx.lib.mixins.listctrl  as  listmix
import wx.lib.newevent

from function import *
import setting

if wx.Platform == '__WXMSW__':
    import wx.lib.iewin as iewin

wildcard = "Almanac (*.ALM)|*.ALM|" \
           "FOPRS Data (*.csv)|*.csv|" \
		   "Python source (*.py)|*.py|" \
           "All files (*.*)|*.*"
menu = {
	1: ['images/window-new64.png', 'New'],
	2: ['images/document-save64.png', 'Save'],
	3: ['images/exit32.png', 'Exit from program'],
	4: ['images/stock32.png', 'Data History'],
	5: ['images/abouth832.png', 'Location'],
	6: ['images/user32.png', 'Setting'],
	7: ['images/help32.png', 'Help'],
	8: ['images/about32.png', 'About'],
	9: ['images/tutorial32.png', 'Analysis'],
	10: ['images/document-open64.png', 'Open'],
	11: ['images/document-close64.png', 'Close'],
	}

images_list = [
	'images/login32.png', 'images/logout32.png', 'images/exit32.png', 'images/abouth832.png',
	'images/tutorial32.png', 'images/portofolio32.png', 'images/galeri32.png', 
	'images/stock32.png', 'images/pembelian32.png', 'images/publikasi32.png', 
	'images/user32.png', 'images/setting32.png', 'images/help32.png', 'images/about32.png']
	

musicdata = {
1 : ("Bad English", "The Price Of Love", 1, "Rock"),
2 : ("DNA featuring Suzanne Vega", "Tom's Diner", 1, "Rock"),
3 : ("George Michael", "Praying For Time", 1, "Rock"),
4 : ("Gloria Estefan", "Here We Are", 1, "Rock"),
5 : ("Linda Ronstadt", "Don't Know Much", 0, "Rock"),
6 : ("Michael Bolton", "How Am I Supposed To Live Without You", 0, "Blues"),
7 : ("Paul Young", "Oh Girl", 0, "Rock"),
8 : ("Paula Abdul", "Opposites Attract", 1, "Rock"),
9 : ("Richard Marx", "Should've Known Better", 0, "Rock"),
10: ("Rod Stewart", "Forever Young", 1, "Rock"),
11: ("Roxette", "Dangerous", 0, "Rock"),
}

FILE_LOCATION = ''
LOCATION = 'D:\\Python\\py-earth\\NANU\\'

info = "PyJigdo 1.0 - Jigdo System"
fileicon = "pyjigdo.ico"


(UpdateBarEvent, EVT_UPDATE_BARGRAPH) = wx.lib.newevent.NewEvent()
(DownloadFile, EVT_DOWNLOAD) = wx.lib.newevent.NewEvent()

		
class PanelChannel(wx.Panel):
	def __init__(self, parent, id, title='default', imagePath='images/galeri32.png'):
		wx.Panel.__init__(self, parent, -1)
		
		self.txt = wx.StaticText(self, -1, title)
		self.edit = wx.TextCtrl(self, -1, '0')
		
		iconize = wx.Bitmap(imagePath, wx.BITMAP_TYPE_PNG)
		self.logo = wx.StaticBitmap(self, -1, iconize)

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.txt, 0, wx.EXPAND | wx.ALL, 2)
		sizer.Add(self.edit, 0, wx.EXPAND | wx.ALL, 2)
		sizer.Add(self.logo, 0, wx.EXPAND | wx.ALL, 2)
		
		board = wx.BoxSizer(wx.VERTICAL)
		board.Add(sizer, 0, wx.EXPAND | wx.ALL, 2)

		sb = wx.StaticBox(self, -1, title)
		bsb = wx.StaticBoxSizer(sb, wx.VERTICAL)
		bsb.Add(board, 0, wx.EXPAND | wx.ALL, 0)

		border = wx.BoxSizer()
		border.Add(bsb, 1, wx.EXPAND | wx.ALL, 0)
		self.SetSizer(border)
		self.Layout()
		
	def SetValue(self, data):
		self.edit.SetValue(data)
		
	def SetImage(self, imagePath):
		newimage = wx.Bitmap(imagePath, wx.BITMAP_TYPE_PNG)
		self.logo.SetBitmap(newimage)
		
		
class PanelGrid(wx.Panel):
	def __init__(self, parent, id):
		wx.Panel.__init__(self, parent, -1)
		color = wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE)
		self.SetBackgroundColour(color)

		COL_SIZE = 0
		for i in range(len(colsize_tab)):
			COL_SIZE = COL_SIZE + colsize_tab[i]

		self.grid = grid.Grid(self, -1, size = (-1, -1)) #size=(COL_SIZE+100, 290))
		self.grid.CreateGrid(num_rows, num_cols)
		self.grid.SetDefaultColSize(50)

		self.attr = wx.grid.GridCellAttr()
		self.attr.SetBackgroundColour('#DDDDDD')
		
		for i in range(num_rows):
			if (i%2 == 0):
				self.grid.SetRowAttr(i, self.attr)
			else:
				pass
		
		for i in range(num_cols):
			self.grid.SetColSize(i, colsize_tab[i])

		for row in range(num_rows):
			for col in range(num_cols):
				self.grid.SetColLabelValue(col, label_tab[col])
				
		#for i in range(len(RectPropertyList)):
		#	self.grid.SetCellValue(i, 0, RectPropertyList[i])

		
		txt_date1 = wx.StaticText(self, -1, 'From')
		txt_date2 = wx.StaticText(self, -1, 'To')

		sizerDate = wx.FlexGridSizer(0,2,0,0)
		sizerDate.Add(txt_date1, 0, wx.ALIGN_CENTRE_VERTICAL | wx.ALL, 2)
		sizerDate.Add(txt_date2, 0, wx.ALIGN_CENTRE_VERTICAL | wx.ALL, 2)

		btn_show = wx.Button(self, -1, 'Show', size = (100, 30))
		
		sizer = wx.BoxSizer(wx.HORIZONTAL)
		sizer.Add(sizerDate, 0, wx.ALL, 2)
		sizer.Add(btn_show, 1, wx.ALL, 2)

		board = wx.BoxSizer(wx.VERTICAL)
		board.Add(sizer, 0, wx.ALL, 2)
		board.Add(self.grid, 1, wx.EXPAND | wx.ALL, 2)

		border = wx.BoxSizer()
		border.Add(board, 1, wx.EXPAND | wx.ALL, 0)
		self.SetSizer(border)
		self.ObjectID = 0
		
	def getObjectID(self, object = 0):
		self.ObjectID = object
		
	def changeValue(self, event):
		if self.ObjectID == 1002:
			for i in range(len(ImagePropertyList)):
				self.grid.SetCellValue(i, 0, ImagePropertyList[i])
				print 'Image property'
				
		elif self.ObjectID == 1003:
			for i in range(len(RectPropertyList)):
				self.grid.SetCellValue(i, 0, RectPropertyList[i])
				print 'Rect property'
				
		elif self.ObjectID == 1004:
			for i in range(len(PolyPropertyList)):
				self.grid.SetCellValue(i, 0, PolyPropertyList[i])
				print 'Poly property'
		

class TestListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
	def __init__(self, parent, ID, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
		wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
		listmix.ListCtrlAutoWidthMixin.__init__(self)
		

class BarThread:
	def __init__(self, win, barNum, val):
		self.win = win
		self.barNum = barNum
		self.val = val
		
	def Start(self):
		self.keepGoing = self.running = True
		thread.start_new_thread(self.Run, ())
		
	def Stop(self):
		self.keepGoing = False
		
	def IsRunning(self):
		return self.running
		
	def Run(self):
		while self.keepGoing:
			evt = UpdateBarEvent(barNum = self.barNum, value = int(self.val))
			wx.PostEvent(self.win, evt)
			
			sleeptime = (random.random() * 2) + 0.5
			time.sleep(sleeptime/4)
			
			sleeptime = sleeptime * 5
			if int(random.random() * 2):
				self.val = self.val + sleeptime
			else:
				self.val = self.val - sleeptime
				
			if self.val < 0: self.val = 0
			if self.val > 300: self.val = 300
			
		self.running = False
		
		
class DownloadAlmanac:
	def __init__(self, win, year, log):
		self.win = win
		self.year = year
		self.log = log
		self.listofFile = []
		self.fileDone = ''
		
	def Start(self):
		self.keepGoing = self.running = True
		thread.start_new_thread(self.download, ())
		
	def Stop(self):
		self.keepGoing = False
		
	def IsRunning(self):
		return self.running
		
	def Run(self):
		pass
		
	def download(self):
		year = self.year
		while self.keepGoing:
			
			try:
				#print 'Start to download for year %s' % year
				evt = DownloadFile(year = int(self.year), listFile = self.listofFile, fileDone = self.fileDone)
				wx.PostEvent(self.win, evt)

				self.log.WriteText('Start to download for year %s\n' % year)
				
				url = 'http://www.navcen.uscg.gov/?Do=gpsArchives&path=ALMANACS/YUMA&year=' + str(year)
				url_download = urllib2.urlopen(url)
				
				html = url_download.read()
			
				start_number =  html.find('GPS ALMANACS/YUMA FOR YEAR ' + str(year))
				end_number = html.find('<!-- End Page Content -->')
				
				self.log.WriteText('Get result...\n')
				temp = []
				for i in html[start_number:end_number].replace('\t', ''):
					if (i != '<') and (i != '>') and (1 != '\'') and (1 != '\r'):
						temp.append(i)
					
				atext = ' href="'
				btext = 'http://www.navcen.uscg.gov/'

				result = ''.join(temp).replace('/tr', '').replace('tr', '').replace('tda', '').replace('/a/td', '').replace('\r', '').replace('" ', ',').replace(atext, btext).split(',')
				self.log.WriteText('Result done.\n')
				
				self.listofFile = []
				for i in range(len(result[0:-1])):
					self.listofFile.append(result[i].split('\n')[-1])
					
				self.log.WriteText('This file will download:\n')
				for i in self.listofFile:
					self.log.WriteText('%s\n' % i)
					
				self.log.WriteText('List file done.\n')
				
				self.log.WriteText('Trying to download from: %s\n' % btext)
				for i in range(len(self.listofFile)):
					url = self.listofFile[i]
					
					try:
						url_to_download = urllib2.urlopen(str(url))
						html = url_to_download.read()
						
						meta = url_to_download.info()
						try:
							tempname = meta.getheaders("Content-Disposition")[0][22:-1].upper()
						except IndexError:
							tempname = 'temp'
							
						t = time.localtime(time.time())
						showtime = time.strftime('%H:%M:%S', t)
						#self.log.WriteText('Filename %s downloaded at %s\n' % (tempname, showtime))
						self.fileDone = 'Filename %s downloaded at %s\n' % (tempname, showtime)

						if os.path.exists(LOCATION + str(year)):
							output = open(LOCATION + str(year) + '\\' + tempname, 'wb')
							output.write(html)
							output.close()
						else:
							os.makedirs(LOCATION + str(year))
							#create __init__.py
							output = open(LOCATION + str(year) + '\\' + '__init__.py', 'wb')
							output.close()

							output = open(LOCATION + str(year) + '\\' + tempname, 'wb')
							output.write(html)
							output.close()
						
					except urllib2.URLError, error:
						self.log.WriteText("Error to download from %s. %s\n" % (url, error))
					
					except KeyboardInterrupt:
						self.log.WriteText("Download cancelled.\n")
						sys.exit()
			
			except urllib2.URLError, error:
				self.log.WriteText("Error to download from %s. %s\n" % (url, error))
				
			except KeyboardInterrupt:
				self.log.WriteText("Download cancelled.\n")
				sys.exit()

		
class MainForm(wx.Frame):
	def __init__(self, parent, id):
		wx.Frame.__init__(self, parent, id, title=info, size = (780,620))
		
		color = wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE)
		self.SetBackgroundColour(color)
		self.SetIcon(wx.Icon(fileicon, wx.BITMAP_TYPE_ICO))

		#initial
		self.today = ''
		
		self.start_cnt = 0
		
		#self.setMenu()
		self.setToolbar()
		
		pnl1 = wx.Panel(self, -1)

		self.log = wx.TextCtrl(pnl1, -1, '', size = (-1, 120), style = wx.TE_MULTILINE | wx.TE_PROCESS_ENTER)
		
		#Setting Status Bar
		self.statusbar = self.CreateStatusBar(4, wx.ST_SIZEGRIP)
		self.statusbar.SetStatusWidths([-1, -1, -1, -1])
		statusbar_fields = [(""), ("User: Operator"), ("")]
		
		for i in range(len(statusbar_fields)):
			self.statusbar.SetStatusText(statusbar_fields[i],i)

		logoBig     = wx.Bitmap(FILE_LOCATION + "images/user64.png", wx.BITMAP_TYPE_PNG)
		self.imgBig = wx.StaticBitmap(self, -1, logoBig, pos=(-1, -1), size=(64, 64))

		txt_logo = wx.StaticText(pnl1, -1, 'Insert location of .jigdo file and destination directory to save file to:')

		txt_url    = wx.StaticText(pnl1, -1, 'Insert URL')
		txt_saveto = wx.StaticText(pnl1, -1, 'Save to')
		
		edit_size = (500,-1)
		self.edit_url = wx.TextCtrl(pnl1, -1, '', size = edit_size)
		self.edit_saveto = wx.TextCtrl(pnl1, -1, '', size = edit_size)

		btn_size = (30,23)
		self.btn_url = wx.Button(pnl1, -1, '...', size = btn_size)
		self.btn_saveto = wx.Button(pnl1, -1, '...', size = btn_size)
		self.btn_download = wx.Button(pnl1, -1, 'Download', size = (100,30))
		
		self.Bind(wx.EVT_BUTTON, self.onOpen, self.btn_url)
		self.Bind(wx.EVT_BUTTON, self.onOpenDir, self.btn_saveto)
		self.Bind(wx.EVT_BUTTON, self.onDownload, self.btn_download)
		
		sizerEdit = wx.FlexGridSizer(0,3,0,0)
		sizerEdit.Add(txt_url, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
		sizerEdit.Add(self.edit_url, 1, wx.EXPAND | wx.ALL, 2)
		sizerEdit.Add(self.btn_url, 0, wx.EXPAND | wx.ALL, 2)
		sizerEdit.Add(txt_saveto, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
		sizerEdit.Add(self.edit_saveto, 1, wx.EXPAND | wx.ALL, 2)
		sizerEdit.Add(self.btn_saveto, 0, wx.EXPAND | wx.ALL, 2)
		
		imgSmile   = wx.Bitmap(FILE_LOCATION + "images/bigsmile16.png", wx.BITMAP_TYPE_PNG)
		imgSad     = wx.Bitmap(FILE_LOCATION + "images/sad16.png", wx.BITMAP_TYPE_PNG)
		self.il    = wx.ImageList(16, 16)
		self.idx1  = self.il.Add(imgSmile)
		self.idx2  = self.il.Add(imgSad)
		self.sm_dn = self.il.Add(imgSmile)
		
		self.list = TestListCtrl(pnl1, -1, style=wx.LC_REPORT  #| wx.BORDER_SUNKEN
			| wx.BORDER_NONE
			| wx.LC_EDIT_LABELS
			| wx.LC_SORT_ASCENDING
			#| wx.LC_NO_HEADER
			#| wx.LC_VRULES
			#| wx.LC_HRULES
			#| wx.LC_SINGLE_SEL
			)
			
		self.list.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
		
		pnlLeft = wx.BoxSizer(wx.VERTICAL)
		pnlLeft.Add(self.imgBig, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 2)
		pnlLeft.Add(txt_logo, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 2)
		pnlLeft.Add(sizerEdit, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 2)
		pnlLeft.Add(self.btn_download, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 2)
		
		pnlTop = wx.BoxSizer(wx.VERTICAL)
		pnlTop.Add(pnlLeft, 1, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
		pnlTop.Add(self.list, 1, wx.EXPAND | wx.ALL, 2)
		pnlTop.Add(self.log, 0, wx.EXPAND | wx.ALL, 2)

		pnlborder = wx.BoxSizer()
		pnlborder.Add(pnlTop, 1, wx.EXPAND | wx.ALL, 0)
		pnl1.SetSizer(pnlborder)
		pnl1.Layout()

		mainPanel = wx.BoxSizer()
		mainPanel.Add(pnl1, 1, wx.EXPAND | wx.ALL, 0)
		self.SetSizer(mainPanel)
		self.Layout()

		#Menampilkan jam
		self.timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
		self.timer.Start(1000)

		#EVENT
		self.PopulateList()
		self.Bind(wx.EVT_CLOSE, self.OnExit)
		
		self.Bind(EVT_DOWNLOAD, self.download)
		self.d = DownloadAlmanac(self, 2012, self.log)

		#self.Bind(EVT_UPDATE_BARGRAPH, self.onUpdate)
		
		self.threads = []
		self.threads.append(BarThread(self, 0, 50))
		self.threads.append(BarThread(self, 1, 75))
        #self.threads.append(CalcBarThread(self, 2, 100))
        #self.threads.append(CalcBarThread(self, 3, 150))
		
		#for t in self.threads:
		#	t.Start()
		
	def setMenu(self):
		menuBar = wx.MenuBar()
		
		# 1st menu from left
		mFile = wx.Menu()
		menuBar.Append(mFile, "&File")

		mOpen = mFile.Append(-1, "&Open", "This the text in the Statusbar")
		mSave = mFile.Append(-1, "&Save", "This the text in the Statusbar")
		mClose = mFile.Append(-1, "&Close", "This the text in the Statusbar")
		mFile.AppendSeparator()
		mExit = mFile.Append(-1, "&Exit", "This the text in the Statusbar")
		
		self.SetMenuBar(menuBar)
		
		self.Bind(wx.EVT_MENU, self.OnExit, mExit)
		self.Bind(wx.EVT_MENU, self.onOpen, mOpen)
		
	def setToolbar(self):
		tsize = (32,32)
		img_new      = wx.Bitmap(menu[1][0], wx.BITMAP_TYPE_PNG) #login32
		img_open     = wx.Bitmap(menu[10][0], wx.BITMAP_TYPE_PNG) #logout32
		img_close    = wx.Bitmap(menu[11][0], wx.BITMAP_TYPE_PNG) #exit32
		img_setting  = wx.Bitmap(images_list[11], wx.BITMAP_TYPE_PNG) #user32
		img_help     = wx.Bitmap(images_list[3], wx.BITMAP_TYPE_PNG) #abouth832
		img_about    = wx.Bitmap(images_list[13], wx.BITMAP_TYPE_PNG) #about32

		TBFLAGS = ( 
			wx.TB_HORIZONTAL #wx.TB_VERTICAL
			| wx.NO_BORDER
			| wx.TB_FLAT
			#| wx.TB_TEXT
			#| wx.TB_HORZ_LAYOUT
			)
		tb = self.CreateToolBar(style = TBFLAGS)
		self.btn_new    = tb.AddLabelTool(-1, 'New',    img_new,  shortHelp = 'New',  longHelp = 'New file')
		self.btn_open   = tb.AddLabelTool(-1, 'Open',   img_open, shortHelp = 'Open', longHelp = 'Open file')
		self.btn_exit  = tb.AddLabelTool(-1, 'Close',  img_close, shortHelp = 'Close', longHelp = 'Close file')
		tb.AddSeparator()
		self.btn_setting  = tb.AddLabelTool(-1, 'Setting',  img_setting, shortHelp = menu[6][1], longHelp = menu[6][1])
		tb.AddSeparator()
		self.btn_help   = tb.AddLabelTool(-1, 'Help',        img_help, shortHelp = menu[7][1], longHelp = menu[7][1])
		self.btn_about  = tb.AddLabelTool(-1, 'About',       img_about, shortHelp = menu[8][1], longHelp = menu[8][1])
		tb.SetToolBitmapSize(tsize)
		tb.Realize()
		
		#self.Bind(wx.EVT_TOOL, self.onNew, self.btn_new)
		#self.Bind(wx.EVT_TOOL, self.onOpen, self.btn_open)
		self.Bind(wx.EVT_TOOL, self.OnExit, self.btn_exit)
		#self.Bind(wx.EVT_TOOL, self.OnSetting, self.btn_setting)
		#self.Bind(wx.EVT_TOOL, self.OnHelp, self.btn_help)
		#self.Bind(wx.EVT_TOOL, self.OnAbout, self.btn_about)
		
	def OnTimer(self, event):
		t = time.localtime(time.time())
		#st1 = time.strftime('%A, %d %B %Y', t)
		st1 = formattanggal(t)
		st2 = time.strftime('%I:%M:%S', t)
		
		#self.txt_date.SetLabel(st1)
		#self.txt_time.SetLabel(st2)

		#self.statusbar.SetStatusText(self.today + ' ' + st2, 2)
		self.today = '%s-%s-%s' % (t[0], AddZero(t[1]), AddZero(t[2]))
		
	def OnExit(self, event):
		sys.exit()
		
	def OnSetting(self, event):
		dlg = setting.SettingMain(self, -1)
		dlg.ShowModal()
		dlg.Centre()
		
	def OnHistory(self, event):
		#dlg = history.HistoryMain(self, -1)
		#dlg.ShowModal()
		#dlg.Centre()
		pass
		
	def OnHelp(self, event):
		msg = "Call police, bro!!!?!?!\n\n" + \
			"Hehehehe....\n"
			
		dlg = wx.MessageDialog(None, msg, info,
			wx.OK | wx.ICON_INFORMATION)
		dlg.ShowModal()
		dlg.Destroy()
		
	def OnAbout(self, event):		
		msg = info+' \n' + \
			"By Physics Departement, University of Indonesia\n"
			
		dlg = wx.MessageDialog(None, msg, info,
			wx.OK | wx.ICON_INFORMATION)
		dlg.ShowModal()
		dlg.Destroy()
		
	def onOpen(self, event):
		dlg = wx.FileDialog(self, message="Choose an xml file",
			defaultDir=os.getcwd(), defaultFile="", wildcard = "Jigdo files (*.jigdo)|*.jigdo| XML files (*.xml)|*.xml| All files (*.*)|*.*", style=wx.OPEN | wx.CHANGE_DIR )
		
		if dlg.ShowModal() == wx.ID_OK:
			path = dlg.GetPath()
			self.path = path
			self.edit_url.SetValue('%s' % path)
			#self.log.Clear()
			#self.log.WriteText(path + '\n')

			#f = open(path, 'r')
			##outfile = 'temp_' + filename[:-4]+'.sql'
			##fout = open(outfile, 'w')
			#t = f.readlines()
			
			#for i in t:
			#	self.buffer = self.buffer + i
				
			#self.onReadXML()
			
		else:
			path = 'C:\\'
			
		dlg.Destroy()
		
	def onOpenDir(self, event):
		dlg = wx.DirDialog(self, "Choose a directory:", style=wx.DD_DEFAULT_STYLE #| wx.DD_DIR_MUST_EXIST
			#| wx.DD_CHANGE_DIR
			)
			
		if dlg.ShowModal() == wx.ID_OK:
			#self.log.WriteText('You selected: %s\n' % dlg.GetPath())
			self.edit_saveto.SetValue('%s' % dlg.GetPath())
			
		dlg.Destroy()
		
	def download(self, event):
		for i in event.listFile:
			#self.log.WriteText('Downloading...')
			print i
			
		print event.fileDone
			
		#self.log.WriteText('Downloading... %s' % event.fileDone)
		#self.log.WriteText('Downloading... %s' % event.year)
	
	def onUpdate(self, event):
		self.log.WriteText('barNum: %s, value: %s\n' % (event.barNum, event.value))
		
	def onDownload(self, event):
		#variables = {}
		#execfile( "jigdo-lite.bat", variables )
		#import compileall
		#compileall.compile_dir('D:\\Python\\py-jigdo', force=True)
		
		#import subprocess
		#arg1 = ""
		#arg2 = ""
		#subprocess.call(["jigdo-lite.bat", "", arg1, arg2])
		
		#self.downloadAlmanac()
		self.d.Start()
		
	def downloadAlmanac(self, year = 2012):
		try:
			#print 'Start to download for year %s' % year
			self.log.WriteText('Start to download for year %s\n' % year)
			
			url = 'http://www.navcen.uscg.gov/?Do=gpsArchives&path=ALMANACS/YUMA&year=' + str(year)
			url_download = urllib2.urlopen(url)
			
			html = url_download.read()
		
			start_number =  html.find('GPS ALMANACS/YUMA FOR YEAR ' + str(year))
			end_number = html.find('<!-- End Page Content -->')
			
			self.log.WriteText('Get result...\n')
			temp = []
			for i in html[start_number:end_number].replace('\t', ''):
				if (i != '<') and (i != '>') and (1 != '\'') and (1 != '\r'):
					temp.append(i)
				
			atext = ' href="'
			btext = 'http://www.navcen.uscg.gov/'

			result = ''.join(temp).replace('/tr', '').replace('tr', '').replace('tda', '').replace('/a/td', '').replace('\r', '').replace('" ', ',').replace(atext, btext).split(',')
			self.log.WriteText('Result done.\n')
			
			listFile = []
			for i in range(len(result[0:-1])):
				listFile.append(result[i].split('\n')[-1])
				
			self.log.WriteText('This file will download:\n')
			for i in listFile:
				self.log.WriteText('%s' % i)
				
			self.log.WriteText('List file done.\n')
			
			self.log.WriteText('Trying to download from: %s\n' % btext)
			for i in range(len(listFile)):
				url = listFile[i]
				
				try:
					url_to_download = urllib2.urlopen(str(url))
					html = url_to_download.read()
					
					meta = url_to_download.info()
					try:
						tempname = meta.getheaders("Content-Disposition")[0][22:-1].upper()
					except IndexError:
						tempname = 'temp'
						
					t = time.localtime(time.time())
					showtime = time.strftime('%H:%M:%S', t)
					self.log.WriteText('Filename %s downloaded at %s\n' % (tempname, showtime))

					if os.path.exists(LOCATION + str(year)):
						output = open(LOCATION + str(year) + '\\' + tempname, 'wb')
						output.write(html)
						output.close()
					else:
						os.makedirs(LOCATION + str(year))
						#create __init__.py
						output = open(LOCATION + str(year) + '\\' + '__init__.py', 'wb')
						output.close()

						output = open(LOCATION + str(year) + '\\' + tempname, 'wb')
						output.write(html)
						output.close()
					
				except urllib2.URLError, error:
					self.log.WriteText("Error to download from %s. %s\n" % (url, error))
				
				except KeyboardInterrupt:
					self.log.WriteText("Download cancelled.\n")
					sys.exit()
		
		except urllib2.URLError, error:
			self.log.WriteText("Error to download from %s. %s\n" % (url, error))
			
		except KeyboardInterrupt:
			self.log.WriteText("Download cancelled.\n")
			sys.exit()
		
	def PopulateList(self):
		if 0:
			# for normal, simple columns, you can add them like this:
			self.list.InsertColumn(0, "Artist")
			self.list.InsertColumn(1, "Title", wx.LIST_FORMAT_RIGHT)
			#self.list.InsertColumn(2, "Genre")
		else:
			# but since we want images on the column header we have to do it the hard way:
			info = wx.ListItem()
			info.m_mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_IMAGE | wx.LIST_MASK_FORMAT
			info.m_image = -1
			info.m_format = 0
			info.m_text = "Artist"
			self.list.InsertColumnInfo(0, info)
			
			info.m_format = wx.LIST_FORMAT_RIGHT
			info.m_text = "Title"
			self.list.InsertColumnInfo(1, info)
			
			#info.m_format = 0
			#info.m_text = "Genre"
			#self.list.InsertColumnInfo(2, info)
			
		items = musicdata.items()
		for key, data in items:
			if data[2] == 1:
				index = self.list.InsertImageStringItem(sys.maxint, data[0], self.idx1)
			else:
				index = self.list.InsertImageStringItem(sys.maxint, data[0], self.idx2)
			self.list.SetStringItem(index, 1, data[1])
			#self.list.SetStringItem(index, 2, data[2])
			self.list.SetItemData(index, key)
			
		self.list.SetColumnWidth(0, wx.LIST_AUTOSIZE)
		self.list.SetColumnWidth(1, wx.LIST_AUTOSIZE)
		#self.list.SetColumnWidth(2, 100)
		
		# show how to select an item
		self.list.SetItemState(5, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
		
		# show how to change the colour of a couple items
		'''
		item = self.list.GetItem(1)
		item.SetTextColour(wx.BLUE)
		self.list.SetItem(item)
		item = self.list.GetItem(4)
		item.SetTextColour(wx.RED)
		self.list.SetItem(item)
		'''
		
		self.currentItem = 0
		
		
		