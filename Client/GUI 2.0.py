from tkinter import *
from tkinter import ttk
import tkintermapview
import tkinter.font as TkFont
from PIL import Image, ImageTk
import mysql.connector
import os

class App(Tk):
    def __init__(self):
        super().__init__()
        self["bg"] = "#d9d9d9"
        self.geometry('1120x630')
        self.minsize(1120,630)
        self.iconbitmap(r'C:\Users\ravid\OneDrive\מסמכים\GitHub\PythonCyberProject2023\Client\3105807.ico')
        self.title("TapMap")





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


class MapFrame(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self['bg'] = 'red'
        

        watermap = tkintermapview.TkinterMapView(self, max_zoom=18)
        watermap.set_address("32.0852937, 34.7816499")
        watermap.set_zoom(10)
        
        watermap.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga")
        
        taps = []

        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",
            database="water_taps"
        )

        mycursor = db.cursor()

        mycursor.execute("SELECT * FROM taps_table")

        

        for watertap in mycursor:
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



        watermap.grid(row=0, column=0, sticky="nsew")

        Grid.rowconfigure(self, 0, weight=1)
        Grid.columnconfigure(self, 0, weight=1)
class Menu_Button(Button):
     def __init__(self, icon, *args, **kwargs):
        Button.__init__(self, *args, **kwargs)
        
        self['bg'] = 'white'
        self['fg'] = 'black'
        self['image'] = icon
        self['height'] = 60
        #self['width'] = 120
        self['compound'] = RIGHT
        self['font'] = TkFont.Font(family="Rubik", size=24)
        self['relief'] = "flat"
        self['anchor'] = E


        
app = App()

MapFrame(app).grid(row=0,column=0, sticky="nsew")

menu_frame = Frame(app, bg='white')




menu_btns = []
menu_btns_text = ["מפה   ", "הוספה   ", "דיווח   ", "מידע   "]
icons = [
    ImageTk.PhotoImage(Image.open(r"C:\Users\ravid\OneDrive\מסמכים\GitHub\PythonCyberProject2023\Client\Icons\map.png").resize((30, 30))),
    ImageTk.PhotoImage(Image.open(r"C:\Users\ravid\OneDrive\מסמכים\GitHub\PythonCyberProject2023\Client\Icons\more.png").resize((30, 30))),
    ImageTk.PhotoImage(Image.open(r"C:\Users\ravid\OneDrive\מסמכים\GitHub\PythonCyberProject2023\Client\Icons\report.png").resize((30, 30))),
    ImageTk.PhotoImage(Image.open(r"C:\Users\ravid\OneDrive\מסמכים\GitHub\PythonCyberProject2023\Client\Icons\info.png").resize((30, 30)))
]




for i in range(len(menu_btns_text)):
  print(i)
  menu_btns.append(Menu_Button(icons[i], menu_frame, text=menu_btns_text[i]))
  menu_btns[i].grid(row=i, column=0, padx=10, pady=5, sticky="ewsn")



Grid.columnconfigure(menu_frame, 0, weight=1)

menu_frame.grid(row=0, column=1,padx=1, sticky="nsew")

Grid.rowconfigure(app, 0, weight=1)
Grid.columnconfigure(app, 0, weight=6)
Grid.columnconfigure(app, 1, weight=1)


app.mainloop()