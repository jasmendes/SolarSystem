# -*- coding: cp1252 -*-
"""
author
       Ernesto P. Adorio, Ph.D
       University of the Philippines
       Extension Program in Pampanga
       ernesto.adorio@gmail.com
version 0.0.1 jan 21, 2008
for educational use.
"""
import wx 
import math


class body():
    def __init__(self, parent, distance, radius, rot= 2, name = "moon", color = "black", xy = None):
        self.parent = parent
        self.dist  = distance
        self.r     = radius
        self.name  = name
        self.theta = 0
        self.dtheta = rot
        self.color = color
        if xy is None:
            self.xy=(distance, 0) 
        else:
            self.xy    = xy[:]
        self.newxy = self.xy


# test it ...
Sun = body(None,     0, 40, rot = 0,        name = "Sol",  color = "yellow")
Mercury = body(Sun,70, 15, rot = 0.250/3,   name = "Mercury", color = "red")
Venus = body(Sun,140, 17, rot = 0.125/3,   name = "Venus", color = "green")

Earth = body(Sun,  210, 20, rot = 0.0170/2, name = "Earth",color = "blue")#13 voltas
Moon  = body(Earth, 40, 5, rot = 0.250/2., name = "Luna", color = "white")
asteroid = body(Sun,270, 1, rot = 0.1250/3,   name = "Aster", color = "black")
solar = [Sun, Mercury, Venus, Earth, Moon, asteroid]


    
    
class MyFrame(wx.Frame): 
    """a frame with a panel"""
    def __init__(self, parent=None, id=-1, title=None, dx= 500, dy= 500, solar= None, dtheta = 0.1625): 
        wx.Frame.__init__(self, parent, id, title) 
        self.panel = wx.Panel(self, size=(dx, dy)) 
        self.panel.Bind(wx.EVT_PAINT, self.on_paint)
        self.solar = solar
        self.xcenter = dx/2
        self.ycenter = dy/2

        self.Fit()
        self.timer= wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_timer_event)
        self.timer.Start(milliseconds=50, oneShot=False)
        self.dc= None
    
    def on_timer_event(self, event):
        if self.dc is None:
            self.dc= wx.PaintDC(self.panel)
        if True: #erase previous position drawing.
            self.dc.SetPen(wx.Pen('lightgray', 1))
            self.dc.SetBrush(wx.Brush('lightgray'))
            for body in self.solar:
                if body.parent: 
                    x,y  = body.xy[0]+body.parent.xy[0] +self.xcenter,\
                           body.xy[1]+body.parent.xy[1] +self.ycenter
                    self.dc.DrawCircle(x, y, body.r)
                    print x, y
                else:
                    x,y  = body.xy[0]+self.xcenter,\
                           body.xy[1]+self.ycenter
                    self.dc.DrawCircle(x, y, body.r)
            

        for body in self.solar:
            color = body.color
            self.dc.SetPen(wx.Pen(color, 1))
            self.dc.SetBrush(wx.Brush(color))
            if body.parent:
                self.dc.DrawCircle(body.newxy[0]+self.xcenter+body.parent.xy[0],
                                   body.newxy[1]+self.ycenter+body.parent.xy[1], body.r)
            else:
                self.dc.DrawCircle(body.newxy[0]+self.xcenter,
                                   body.newxy[1]+self.ycenter, body.r)
                
            body.theta += body.dtheta
            twopi= 2*math.pi
            if body.theta > twopi:
              body.theta= body.theta - twopi
            body.xy = body.newxy
            body.newxy=body.dist * math.cos(body.theta),body.dist * math.sin(body.theta)
                

    def on_paint(self, event):
        # establish the painting surface
        if self.dc is None:
            self.dc= wx.PaintDC(self.panel)

 

app= wx.PySimpleApp() 
frame1= MyFrame(title="Simple solar system", solar = solar, dx = 700, dy = 700)

frame1.Center() 
frame1.Show() 
app.MainLoop()
