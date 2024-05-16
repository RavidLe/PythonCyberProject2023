import os
from tkinter import *  
from tkinter import ttk
import tkintermapview
from tkinter import font
from PIL import Image, ImageTk
import mysql.connector
import rsa
import time
import json

HOST = '10.0.0.25'
PORT = 9090
FORMAT = 'utf-8'

public_key, private_key = rsa.newkeys(1024)

class App(Tk):
    def __init__(self):
        super().__init__()
        self.geometry('900x600')
        self.iconbitmap(r'C:\Users\ravid\OneDrive\מסמכים\GitHub\PythonCyberProject2023\Client\3105807.ico')
        self.title("TapMap")

class FrameHeadline(Label):
    def __init__(self, *args, **kwargs):
        Label.__init__(self, *args, **kwargs)

        self['font'] = font.Font(family='bahnschrift', size=35, weight='bold')
        
        
class MenuBotton(Button):
    def __init__(self, *args, **kwargs):
        Button.__init__(self,  *args, **kwargs)
        self['width'] = 20
        self['pady'] = 35
        self['bg'] = 'deepskyblue2'
        self['fg'] = 'white'
        self['activebackground']='navy'
        self['activeforeground']='white'
        self['font'] = font.Font(family='bahnschrift', size=31, weight='bold')
        self['relief'] = 'flat'
        self['bd'] = 0


class MenuFrame(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self['height'] = 600
        self['width'] = 200
        self['bg'] = 'deepskyblue2'
        self.pack_propagate(False)
        
        btnsnames = ['Main', 'Map', 'Add', 'About']
        btnscmds = [None, None, None, None]

        for i in range(4):
            MenuBotton(self, text=btnsnames[i]).pack(side='top')


class SideFrame(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self['height'] = 600
        self['width'] = 700

class InputBox(Entry):
    def __init__(self, *args, **kwargs):
        Entry.__init__(self, *args, **kwargs)

class LabelInputBox(Label):
    def __init__(self, *args, **kwargs):
        Label.__init__(self, *args, **kwargs)
        self['font'] = font.Font(family='bahnschrift', size=18, weight='bold')
        self['padx'] = 30
        self['pady'] = 10


class AddFrame(SideFrame):
    def __init__(self, *args, **kwargs):
        SideFrame.__init__(self, *args, **kwargs)
        color = 'skyBlue1'
        self['bg'] = color
        
        self.grid_propagate(False)
        
        headlineframe = Frame(self, width=700,height=80, bg= color, padx=20, pady=10, )
        headlineframe.grid_propagate(False)
        headlineframe.grid(row=0, sticky=N)

        FrameHeadline(headlineframe, text="Add a tap", bg = color).place(relx=0.5, rely=0.5, anchor=CENTER)

        LocationFrame = Frame(self, width=600, height=120, bg='white')
        LocationFrame.grid_propagate(False)

        LabelInputBox(LocationFrame, text="Location:", bg='white').grid(row=0, column=0)

        options = ['Address', 'Coordinates', 'Choose on map']

        clicked = StringVar()
        clicked.set(options[0])
        
        def Select(event):
            print(1)
            if LocationCombo.get() == options[2]:
                entry = Entry(LocationFrame, width=200)
                entry.grid(row=1,column=2)

        LocationCombo = ttk.Combobox(LocationFrame, value=options, font=font.Font(family='bahnschrift', size=10, weight='bold'), state='readonly', width=13)
        LocationCombo.current(0)
        LocationCombo.bind_all("<<ComboxSelected>>", Select)
        LocationCombo.grid(row=1, column=1)
        
        LocationFrame.grid(row=1,column=0, sticky=N)

        drop = options
        

class WaterMapMarker():

    def __init__(self, watermap, name, x, y, score):

        self.name = name
        self.score = score
        self.x = x
        self.y = y

        self.image = os.path.join(r'C:\Users\ravid\OneDrive\מסמכים\GitHub\PythonCyberProject2023\client\3105806.png')
        self.icon = ImageTk.PhotoImage(Image.open(self.image).resize((12, 12)))
        self.marker = watermap.set_marker(x, y, icon=self.icon)
        self.marker_polygon = watermap.set_polygon([(x+0.006, y),(x,y+0.006),(x-0.006,y),(x,y-0.006)], border_width = 0, outline_color = None, fill_color = None)
        

    def get_marker_polygon(self):
        return self.marker_polygon
    
    def get_name(self):
        return self.name
    
    def get_score(self):
        return self.score
    
    def get_marker(self):
        return self.marker
    
    def update_icon_size(self, zoom):
        if zoom<8:
            zoom = 8
        newsize = int((zoom-7)**1.5)+10
        self.icon = ImageTk.PhotoImage(Image.open(self.image).resize((newsize, newsize))) 
        self.marker.change_icon(self.icon)

                


class MapFrame(SideFrame):
    def __init__(self, *args, **kwargs):
        SideFrame.__init__(self, *args, **kwargs)
        

        

        watermap = tkintermapview.TkinterMapView(self,height = 600, width = 700, max_zoom=18)
        watermap.set_address("32.0852937, 34.7816499")
        watermap.set_zoom(10)
        
        watermap.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga")
        
        taps = []
        
        socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.connect((HOST, PORT))

        server_public = socket.recv(1024).decode(FORMAT)

        socket.send(rsa.encrypt("get".encode(FORMAT), server_public))
        time.sleep(0.1)
        socket.send(rsa.encrypt(public_key.encode(FORMAT), server_public))

        file = open("data.json", "wb")

        file_bytes = b""

        done = FALSE

        while not done:
            data = rsa.decrypt(socket.recv(1024), private_key).decode(FORMAT)
            if file_bytes[-5:] == b"<END>":
                done = True
            else:
                file_bytes += data

        file.write(file_bytes)

        socket.close()
        
        data = json.load(file)


        for watertap in data:
           taps.append(WaterMapMarker(watermap, watertap[1], watertap[2], watertap[3], watertap[4]))
        
        def updatezoom(event):
            for tap in taps:
                tap.update_icon_size(watermap.zoom)

        watermap.canvas.bind_all('<MouseWheel>', updatezoom)
        watermap.canvas.bind_all("<Button-1>",updatezoom)
        
        def motion(event):
            
            for tap in taps:
                
                
                
                c = tap.get_marker_polygon().canvas_polygon_positions

                if event.y > c[1] and event.x < c[2] and event.y < c[5] and event.x > c[6]:
                    text = ""
                    for i in range(int(tap.get_score())):
                        text += ("★")
                    text +=  " " + tap.get_name()
                    tap.get_marker().set_text(text)
                else:
                    tap.get_marker().set_text("")
        
                
        watermap.canvas.bind('<Motion>', motion)

        watermap.grid(row=1,column=0)

        file.close()

        
        
        

        

    


app = App()


menu = MenuFrame(app)
menu.grid(row=0, column=0)


MapFrame(app).grid(row=0,column=1)

app.mainloop()
