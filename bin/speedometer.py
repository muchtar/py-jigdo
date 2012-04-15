#! /usr/bin/python

'''
Filename: pywit.py
Author: Muchtar Suhari Putra (muchtarsputra at gmail.com)
Create: 8 Januari 2011
Description: Class of pywit
'''

import wx
import wx.lib.colourdb
import wx.lib.fancytext as fancytext

from math import pi, sin, cos, log, sqrt, atan2

#Drawing options
# SM_NORMAL_DC Uses The Normal wx.PaintDC
# SM_BUFFERED_DC Uses The Double Buffered Drawing Style

SM_NORMAL_DC = 0
SM_BUFFERED_DC = 1

#---------------

#Speedmeter styles

SM_ROTATE_TEXT = 1
""" Draws the ticks rotated: the ticks are rotated accordingly to the tick marks positions. """
SM_DRAW_SECTORS = 2
""" Different intervals are painted in differend colours (every sector of the""" \
""" circle has its own colour). """
SM_DRAW_PARTIAL_SECTORS = 4
""" Every interval has its own colour, but only a circle corona is painted near the ticks. """
SM_DRAW_HAND = 8
""" The hand (arrow indicator) is drawn. """
SM_DRAW_SHADOW = 16
""" A shadow for the hand is drawn. """
SM_DRAW_PARTIAL_FILLER = 32
""" A circle corona that follows the hand position is drawn near the ticks. """
SM_DRAW_SECONDARY_TICKS = 64
""" Intermediate (smaller) ticks are drawn between principal ticks. """
SM_DRAW_MIDDLE_TEXT = 128
""" Some text is printed in the middle of the control near the center. """
SM_DRAW_MIDDLE_ICON = 256
""" An icon is drawn in the middle of the control near the center. """
SM_DRAW_GRADIENT = 512
""" A gradient of colours will fill the control. """
SM_DRAW_FANCY_TICKS = 1024
""" With this style you can use xml tags to create some custom text and""" \
""" draw it at the ticks position. See `wx.lib.fancytext` for the tags. """

#-----------------

#Event binding

SM_MOUSE_TRACK = 1

fontfamily = range(70, 78)
familyname = ["default", "decorative", "roman", "script", "swiss", "modern", "teletype"]

weights = range(90, 93)
weightsname = ["normal", "light", "bold"]

styles = [90, 93, 94]
stylesname = ["normal", "italic", "slant"]

#-------------


class BufferedWindow(wx.Window):
	def __init__ (self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize,
		style=wx.NO_FULL_REPAINT_ON_RESIZE, bufferedstyle=SM_BUFFERED_DC):
		
		wx.Window.__init__(self, parent, id, pos, size, style)
		
		self.Bind(wx.EVT_PAINT, self.OnPaint)
		self.Bind(wx.EVT_SIZE, self.OnSize)
		self.Bind(wx.EVT_ERASE_BACKGROUND, lambda x: None)
		
		self.OnSize(None)
		
	def Draw(self, dc):
		pass
		
	def OnPaint(self, event):
		#pass
		
		if self._bufferedstyle == SM_BUFFERED_DC:
			dc = wx.BufferedPaintDC(self, self._Buffer)
		else:
			dc = wx.PaintDC(self)
			dc.DrawBitmap(self._Buffer, 0, 0)
		
	def OnSize(self, event):
		#pass
		
		self.Width, self.Height = self.GetClientSizeTuple()
		
		if "__WXMAC__" in wx.Platform:
			if self.Width == 0:
				self.Width = 1
			if self.Height == 0:
				self.Height = 1
				
		self._Buffer = wx.EmptyBitmap(self.Width, self.Height)
		self.UpdateDrawing()
		
	def UpdateDrawing(self):
		#pass
		
		if self._bufferedstyle == SM_BUFFERED_DC:
			dc = wx.BufferedDC(wx.ClientDC(self), self._Buffer)
			self.Draw(dc)
			
		else:
			dc = wx.MemoryDC()
			dc.SelectObject(self._Buffer)
			
			self.Draw(dc)
			wx.ClientDC(self).Blit(0, 0, self.Width, self.Height, dc, 0, 0)


class Speedometer(BufferedWindow):
	def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
		size=wx.DefaultSize, agwStyle=SM_DRAW_HAND, bufferedstyle=SM_BUFFERED_DC, mousestyle=0):
		
		self._agwStyle = agwStyle
		self._bufferedstyle = bufferedstyle
		self._mousestyle = mousestyle
		
		BufferedWindow.__init__(self, parent, id, pos, size, 
			style = wx.NO_FULL_REPAINT_ON_RESIZE, bufferedstyle = bufferedstyle)
			
		if self._mousestyle & SM_MOUSE_TRACK:
			self.Bind(wx.EVT_MOUSE_EVENTS, self.OnMouseMotion)
		
	def Draw(self, dc):
		size = self.GetClientSize()
		
		if size.x < 21 or size.y < 21:
			return
			
		new_dim = size.Get()
		
		if not hasattr(self, "dim"):
			self.dim = new_dim
			
		self.scale = min([float(new_dim[0]) / self.dim[0],
							float(new_dim[1]) / self.dim[1]])
							
		#Create an empty bitmap
		self.faceBitmap = wx.EmptyBitmap(size.width, size.height)
		
		dc.BeginDrawing()
		
		dc.Clear()
		
		centerX = self.faceBitmap.GetWidth()/2
		centerY = self.faceBitmap.GetHeight()/2
		
		#dc.SetBrush(wx.BLUE_BRUSH)
		#dc.SetPen(wx.Pen('VIOLET', 4))
		#x = 10
		#y = 10
		#dc.DrawPoint(x,y)

		w = 30 #random.randint(10, SW)
		h = 80 #random.randint(10, SH)
		x = 10 #random.randint(0, W - w)
		y = 30 #random.randint(0, H - h)
		dc.SetPen(wx.Pen('YELLOW', 2))
		dc.SetBrush(wx.GREEN_BRUSH)
		dc.DrawRectangle(x,y,w,h)
		
	def SetIntervals(self, intervals=None):
		pass
		
	def GetIntervals(self):
		pass
		
	def SetSpeedValue(self, value=None):
		pass
		
	def GetSpeedValue(self):
		pass
		
	def OnMouseMotion(self, event):
		mousex = event.GetX()
		mousey = event.GetY()
		
		if event.Leaving():
			return
			
		pos = self.GetClientSize()
		size = self.GetPosition()
		centerX = self.CenterX
		centerY = self.CenterY
		
		direction = self.GetDirection()
		
		if event.LefIsDown():
			angle = atan2(float(mousey) - centerY, centerX - float(mousex)) + pi - self.EndAngle
			if angle >= 2*pi:
				angle = angle - 2*pi

			if direction == "Advance":
				currentvalue = (self.StartAngle - self.EndAngle - angle)*float(self.Span)/(self.StartAngle - self.EndAngle) + self.StartValue
			else:
				currentvalue = (angle)*float(self.Span)/(self.StartAngle - self.EndAngle) + self.StartValue

			if currentvalue >= self.StartValue and currentvalue <= self.EndValue:
				self.SetSpeedValue(currentvalue)

		event.Skip()
		
