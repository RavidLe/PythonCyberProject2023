import os
from tkinter import *  
import tkintermapview
from tkinter import font
from PIL import Image, ImageTk
import json
import socket

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

class WaterMapMarker():

    

    def __init__(self, watermap, name, score, x, y):

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
        z = int((zoom-7)**1.5)+10
        print(z)
        self.icon = ImageTk.PhotoImage(Image.open(self.image).resize((z, z))) 
        self.marker.change_icon(self.icon)
        

class MapFrame(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self['height'] = 600
        self['width'] = 700

        FrameHeadline(self, text="Look for Water").grid(row=0,column=0)

        watermap = tkintermapview.TkinterMapView(self,height = 500, width = 680, max_zoom=18)
        watermap.set_address("32.0852937, 34.7816499")
        watermap.set_zoom(10)
        
        watermap.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga")
        
        taps = []

        for watertap in data['watertaps']:
           taps.append(WaterMapMarker(watermap, watertap['name'], watertap['score'], watertap['posX'], watertap['posY']))
        
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
                    for i in range(tap.get_score()):
                        text += ("★")
                    text +=  " " + tap.get_name()
                    tap.get_marker().set_text(text)
                else:
                    tap.get_marker().set_text("")
        
                

        watermap.canvas.bind('<Motion>', motion)



        watermap.grid(row=1,column=0)
        

        
def update_data():

    host = '10.0.0.25'    
    port = 6080

    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    client_socket.connect((host, port))
        
    file_bytes = b""

    done = False

    while not done:
        data = client_socket.recv(1024)
        if data == b"<END>":
            done = True
        else:
            file_bytes += data
        
        
    print(file_bytes)
    

    f = open(r"C:\Users\ravid\OneDrive\מסמכים\GitHub\PythonCyberProject2023\Client\database.json", "wb")
    f.write(file_bytes)
    print(file_bytes)

    client_socket.close()

    
    
    

    
    
    
        





update_data()

f = open(r"C:\Users\ravid\OneDrive\מסמכים\GitHub\PythonCyberProject2023\Client\database.json")
data = json.load(f)




app = App()

menu = MenuFrame(app)
menu.pack(side='left')

MapFrame(app).pack()

app.mainloop()
