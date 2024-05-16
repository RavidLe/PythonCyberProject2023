from tkinter import *
import tkintermapview
import tkinter.font as TkFont
from PIL import Image, ImageTk
import os
import rsa
import time
import json
import socket
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA



HOST = '10.0.0.25' # IP of server
PORT = 9090 # PORT of server
FORMAT = 'utf-8' # The Format of encoding and decoding which needs to be idetical to the server's format

public_key, private_key = rsa.newkeys(1024) # creating a private and public key for asymetrical encryption

# fuction the resposible to the communication with the server
def call_server(request, user, info = []): 
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creating a tcp connection with the server
    conn.connect((HOST, PORT)) 


    server_public = rsa.PublicKey.load_pkcs1(conn.recv(1024)) # reciving the public key of the server for asymetrical encryption

    #sending to server the password and username
    conn.send(user.get_username())
    time.sleep(0.1)

    conn.send(user.get_password())
    time.sleep(0.1)

    print("recived key from server")

    if request == "send":
        conn.send(rsa.encrypt("/send".encode(FORMAT), server_public)) # command
        
        for data in info:
            conn.send(rsa.encrypt(str(data).encode(FORMAT), server_public)) # sending each prameter in a diffrent packet
            time.sleep(0.1) #delay so the packets won't mix
    
    elif request == "report":
        conn.send(rsa.encrypt("/report".encode(FORMAT), server_public)) # command

        for data in info:
            conn.send(rsa.encrypt(str(data).encode(FORMAT), server_public)) # sending each prameter in a diffrent packet
            time.sleep(0.1) #delay so the packets won't mix

    conn.close() 

class User():
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def __init__(self):
        self.username = ""
        self.password = ""
    
    def get_username(self):
        return self.username
    def get_password(self):
        return self.password
    
    def set_username(self, username):
        self.username = username
    def set_password(self, password):
        self.password = password


class loginFrame(Frame):
    def __init__(self, frames, user, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

        self['bg'] = 'white' # background color

        def login():
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creating a tcp connection with the server
            conn.connect((HOST, PORT)) 

            server_public = rsa.PublicKey.load_pkcs1(conn.recv(1024)) # reciving the public key of the server for asymetrical encryption

            print("recived key from server")

            username = rsa.encrypt(username_entry.get().encode(FORMAT), server_public)
            password = rsa.encrypt(password_entry.get().encode(FORMAT), server_public)

            conn.send(username)
            time.sleep(0.1)
            conn.send(password)

            ans = conn.recv(1024).decode(FORMAT) 
            if ans == "allowed":
                conn.send(rsa.encrypt("/get".encode(FORMAT), server_public)) # command to the server
                time.sleep(0.1) # setting a delay so that the two messages above and below won't mix with each other due to the sendig being to quick

                conn.send(public_key.save_pkcs1("PEM")) # sending the server the public key 

                # all the messages from know on will be encrypted

                # sending a large file (database) therefore there is a need in symetrical encryption

                key = rsa.decrypt(conn.recv(1024), private_key) # reciving the common key for the symetrical encryption
                nonce = rsa.decrypt(conn.recv(1024), private_key) # reciving the nonce
                cipher = AES.new(key, AES.MODE_EAX, nonce) # creating the cipher which allow to decrypted the file

                print("recived rsa key")

                file_bytes = b"" # the bytes of the file
                done = FALSE  # indication if the transfer is done

                while not done: 

                    data = conn.recv(1024) # recving data in packets (1024)
    
                    if file_bytes[-5:] == b"<END>": # <END> is an sign that the file ends
                        print("DONE")
                        done = True # if <END> shows that transfer is done
        
                    else:
                        file_bytes += data # if not done continue to recive packets

                file = open("data", "wb") # create a file for the data
    
                file.write(cipher.decrypt(file_bytes[:-5])) # write to bytes decrypted without the last five bytes (<END>)
                file.close()

                self.destroy()

                i = 0
                for frame in frames[:-1]:
                    frame.grid(row=0, column=0,padx=1, sticky="nsew")
                    i += 1
                frames[i].grid(row=0, column=1,padx=1, sticky="nsew")
                
                frames[0].tkraise()

                user.set_password(password)
                user.set_username(username)


            elif ans == "denied":
                error_msg = Label(self, text="שגיאה בפרטים", bg = 'white', fg='red', font = TkFont.Font(family="Rubik", size=24)) # error message
                error_msg.place(relx = 1, rely = 0.5, anchor='e')
                error_msg.after(2000 , lambda: error_msg.destroy()) # removing it after two seconds

                username_entry.delete(0, END)
                password_entry.delete(0, END) 
                
            else:
                error_msg = Label(self, text="בעיית תקשרות", bg = 'white', fg='red', font = TkFont.Font(family="Rubik", size=24)) # error message
                error_msg.place(relx = 1, rely = 0.5, anchor='e')
                error_msg.after(2000 , lambda: error_msg.destroy()) # removing it after two seconds    

                username_entry.delete(0, END)
                password_entry.delete(0, END)           
           

        # titles and label from the login
        title = Label(self, text="!TAPMAPברוכים הבאים ל", bg = 'white', font=TkFont.Font(family="Rubik", size=36))
        username_label = FormLabel(self, text=":שם משתמש")
        password_label = FormLabel(self, text=":סיסמא")

        # enter user name and password
        username_entry = EntryInfo(self)
        password_entry = EntryInfo(self, show="*")

        # login button
        login_button = Button(self, text="התחברות", bg ="light cyan", font=TkFont.Font(family="Rubik", size=36), command=login)

        # placing everything
        title.pack(anchor="n")
        username_label.pack(anchor="n")
        username_entry.pack(anchor="n")
        password_label.pack(anchor="n")
        password_entry.pack(anchor="n")
        login_button.pack(pady=20, anchor="n")






# settings of the window
class App(Tk):
    def __init__(self):
        super().__init__()
        self["bg"] = "#d9d9d9" # background color of the window
        self.geometry('1120x630') # size of the window
        self.minsize(1120,630)
        self.iconbitmap('Client\icon5807.ico') # icon of the window
        self.title("TapMap") # title of the window


class WaterMapMarker():

    def __init__(self, watermap, name, x, y, score):

        self.name = name # name that will be shown on the label
        self.score = score # score that will be shown on the label
        self.x = x # location of the mark
        self.y = y # ""

        self.icon = ImageTk.PhotoImage(Image.open('client\icon5806.png').resize((12, 12))) # resize it to a optimal size
        self.marker = watermap.set_marker(x, y, icon=self.icon) # creating a marker
        self.marker_polygon = watermap.set_polygon([(x+0.006, y),(x,y+0.006),(x-0.006,y),(x,y-0.006)],
                                                    border_width = 0, outline_color = None, fill_color = None) # creating a polygon for the marker
        

    def get_marker_polygon(self):
        return self.marker_polygon
    
    def get_name(self):
        return self.name
    
    def get_score(self):
        return self.score
    
    def get_marker(self):
        return self.marker
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def update_icon_size(self, zoom):
        if zoom<8:
            zoom = 8
        newsize = int((zoom-7)**1.5)+10
        self.icon = ImageTk.PhotoImage(Image.open('client\icon5806.png').resize((newsize, newsize))) 
        self.marker.change_icon(self.icon)

# shown when a tap is clicked
class MarkerFrame(Frame):
    def __init__(self, container, name, score):
        super().__init__(container)

        Label(self, text="שם הברזייה"+ ": " + name, bg="white", font = TkFont.Font(family="Rubik", size=30) ).pack(ipadx= 20,side="right") #wirting the name of the tap
        Label(self, text="דירוג" + ": " +str(score), bg="white", font = TkFont.Font(family="Rubik", size=30) ).pack(ipadx= 20, side="right") #writing the score of the tap
        self['bg'] = 'white' #background color is white
        print(name, score)
        

    def getscore(self):
        return self.score 


class MapFrame(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

        map = tkintermapview.TkinterMapView(self, max_zoom=18) # creating an interactive map widget
        map.set_address("32.0852937, 34.7816499") # when the map is opened it will show Tel Aviv
        map.set_zoom(10) # setting the zoom when opening a map
        
        map.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga") # the map will be google map style

        self.map = map #class varible
        
class ChooseLocationMap(MapFrame):
    def __init__(self, l, *args, **kwargs):
        MapFrame.__init__(self, *args, **kwargs)
        
        map = self.map
        
        # when clicking left click
        def left_click_event(coordinates_tuple): 

            map.delete_all_marker() # remove all previous markers on the mark
            
            #when choosing an marker
            def Send(): 
                l.location_entry.insert(0, coordinates_tuple) # insert the the entry box of the location in the add page the chosen coords (X,Y)
                self.destroy() # returns to the add page
                
                
            x_pos = coordinates_tuple[0] # position where clicked
            y_pos = coordinates_tuple[1] 

            marker = map.set_marker(x_pos, y_pos, text = "")  # creating a marker where clicked

            if map.zoom < 15: 
                map.set_zoom(15) # setting zoom to 15 if zoom is not already bigger

            map.set_position(x_pos, y_pos) # foucsing on the marker

            ChooseBtn = Button(self, text="בחר", bg="light green",
                               font=TkFont.Font(family="Rubik", size=24), relief="ridge", borderwidth=1, command= lambda: Send()) #creating the choose button if clicked calling f send
            
            ChooseBtn.place(relx=0.5, rely=1, anchor= "s") # placing button
    


        map.add_left_click_map_command(left_click_event)  # if left click is triggered           


        map.grid(row=0, column=0, sticky="nsew") # placing map

        Grid.rowconfigure(self, 0, weight=1) # adjusting grid so it will be spread on the frame
        Grid.columnconfigure(self, 0, weight=1) # ""


     
class TapLocationsMapFrame(MapFrame):
    def __init__(self, *args, **kwargs):
        MapFrame.__init__(self, *args, **kwargs)

        watermap = self.map 

        taps = [] # creating a list of all the taps on the maps

        
        
        f = open('data') # open the file in which the data was written
 
        
        data = json.load(f) # returns JSON object as a dictionary
        
        widgets = {} # creating a list that will hold all widgets

        i = 0 # an index for the loop

        for watertap in data:
           
           taps.append(WaterMapMarker(watermap, watertap['Name'], watertap['X_coord'], watertap['Y_coord'], watertap['Score'])) # each tap containes name, x, y and score
           widgets[taps[i]] = MarkerFrame(watermap, watertap['Name'], watertap["Score"]) # creating a widget for each tap that will hold the name of the tap and the score 

           i += 1 # increase the index

        # when the zoom changes
        def updatezoom(event):
            for tap in taps:
                tap.update_icon_size(watermap.zoom) # update the size of the icons according the amout of zoom 

        watermap.canvas.bind_all('<MouseWheel>', updatezoom) # when Mousewheel is triggered the zoom changes 
        watermap.canvas.bind_all("<Button-1>",updatezoom) # might be that the zoom will be changed with the buttons of the zoom
        
        # every time a left click is happening checking if the click was on an icon
        def show(event):

            for tap in taps:
          
                c = tap.get_marker_polygon().canvas_polygon_positions # area around the marker the if clicked the details of the tap opens

                if event.y > c[1] and event.x < c[2] and event.y < c[5] and event.x > c[6]: # checking if the click was in the area of the tap
                    widgets[tap].grid(row=1,column=0, sticky="nsew") # placing a frame that shows the details of the tap
                    widgets[tap].tkraise()
                    watermap.set_position(tap.get_x(), tap.get_y()) # foucs on the tap

                
        

        watermap.canvas.bind_all('<Button-1>', show) # when left click is triggered



        watermap.grid(row=0, column=0, sticky="nsew") # placing the map

        Grid.rowconfigure(self, 0, weight=1) # adjusting the map so it is spreaded on the frame
        Grid.columnconfigure(self, 0, weight=1) # ""

class AddFrame(Frame):
    def __init__(self,user, app,  *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self['bg'] = 'white' #background color

        # if the enter button is pressed
        def enter_data():
            

            try:
                name = name_entry.get() # retriving the name from the entry box

                location = self.location_entry.get().split() # retriving the location from the entry box and spliting it to two numbers
                location[0] = float(location[0]) # converting to float might fail so in try and except
                location[1] = float(location[1]) # ""

                rating = scale.get() # retriving the rating from the entry box

                call_server('send', user,[name, location[0], location[1], rating]) # sending to the server the data the was entered
            except:
                error_msg = Label(self, text="שגיאה בפרטים", bg = 'white', fg='red', font = TkFont.Font(family="Rubik", size=24)) # error message
                error_msg.place(relx = 1, rely = 0.5, anchor='e')
                error_msg.after(2000 , lambda: error_msg.destroy()) # removing it after two seconds
            
            # cleaning the data
            name_entry.delete(0, END) 
            self.location_entry.delete(0, END)
            scale.set(0)
        
        # map is open for chosing the location for the new tap
        def open_map():
            map = ChooseLocationMap(self, app)
            map.grid(row=0, column=0,padx=1, sticky="nsew")
            
            

        location_frame = Frame(self, bg='white') # frame for the entry and the button of the location

        name_entry = EntryInfo(self) # for enter name
        self.location_entry = EntryInfo(location_frame) # for enter location
        
        Label(self, font=TkFont.Font(family="Rubik", size=36), text=":הוספת ברזייה", bg='white').pack(ipady=40) # main title of the page

        # titles
        name_label = FormLabel(self, text=":שם הברזייה")  
        location_label = FormLabel(self, text=":מיקום")
        rating_label = FormLabel(self, text=":דירוג")


        location_button = Button(location_frame, font=TkFont.Font(family="Rubik", size=10), text="בחר על המפה", bg='light cyan', command= lambda: open_map()) # a button that call f open_map

        scale = Scale(self, font=TkFont.Font(family="Rubik", size=18), bd=0, bg="white",
                       borderwidth=0,digits=2, from_ = 0, to = 5,
                         length = 250,resolution = 0.1, orient = HORIZONTAL, troughcolor = "light cyan") #creating a scale to chose score
        
        
        #placing everything
        name_label.pack(anchor='n')
        name_entry.pack(anchor='n')
        location_label.pack(anchor='n')
        self.location_entry.pack(anchor='n')
        location_button.pack(side="right",anchor='n')
        location_frame.pack(anchor='n')
        rating_label.pack(anchor='n')
        scale.pack(anchor='n')

        Button(self, font=TkFont.Font(family="Rubik", size=24), text="הוספה", bg='light cyan',borderwidth=2,relief="ridge", command = enter_data).pack( anchor='n', pady=40) # button that sends the data

class ReportFrame(Frame):
     def __init__(self, user, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

        self['bg'] = 'white' # background color


        def send(subject):

            try:

                report_subject = subject[len(subject) - 1] # no idea the only way i found to get the selection in the drop menu
                report_text = report_details.get(1.0, END) # getting the text from the report page
               

                call_server("report", user, [report_subject, report_text])

            except:

                error_msg = Label(self, text="לא נבחר נושא", bg = 'white', fg='red', font = TkFont.Font(family="Rubik", size=24)) # error message
                error_msg.place(relx = 1, rely = 0.5, anchor='e')
                error_msg.after(2000 , lambda: error_msg.destroy())  # removing it after two seconds

            #clearing the page
            options.set("בחר")
            report_details.delete('1.0', END)


        Label(self, font=TkFont.Font(family="Rubik", size=36), text="דיווח", bg='white').pack(ipady=10) # main title of the page
        subject_label = FormLabel(self, text = ":נושא") # subject label

        x = [] # the only in could transfer the varible from the function to global
        def callback(selection):
            x.append(selection)

        options = StringVar()
        
        drop = OptionMenu(self, options, "בחר" ,"בעיה בממשק המשתמש", "מיקום ברזייה שגוי", "שם לא נאות לברזייה", "אחר",command=callback) # create a drop menu to choose from
        options.set("בחר")

        text_label = FormLabel(self, text=":פירוט הבעיה") # text label

        report_details = Text(self, height= 15, width=60, bg="ghost white") # text box where the report is written

        send_button = Button(self, font=TkFont.Font(family="Rubik", size=24), text="שליחה", bg="light cyan", borderwidth=2, relief="ridge", command=lambda: send(x)) # send button


        def char_count(event):
            CHAR_LIMIT = 200
            # This function allows typing up to the character limit and allows deletion
            count = len(report_details.get('1.0', 'end-1c'))
            if count >= CHAR_LIMIT and event.keysym not in {'BackSpace', 'Delete'}:
                return 'break'  # dispose of the event, prevent typing
            

        report_details.bind('<KeyPress>', char_count)
        report_details.bind('<KeyRelease>', char_count)


        # placing everything
        subject_label.pack(anchor='n', pady=5)
        drop.pack(anchor='n', pady=5)
        text_label.pack(anchor='n', pady=5)
        report_details.pack(anchor='n', pady=5)
        send_button.pack(anchor='n', pady=5)



class FormLabel(Label):
    def __init__(self, *args, **kwargs):
        Label.__init__(self, *args, **kwargs)
        self['font'] = TkFont.Font(family="Rubik", size=24)   # setting font
        self['bg'] = "white" # set background 

class EntryInfo(Entry):
    def __init__(self, *args, **kwargs):
        Entry.__init__(self, *args, **kwargs)

        self['font'] = TkFont.Font(family="Rubik", size=18)  # font
        self['bg'] = "light cyan"     #background color
        self['borderwidth'] = 1 #borderwidht

class Menu_Button(Button):
     def __init__(self, icon, *args, **kwargs):
        Button.__init__(self, *args, **kwargs)
        
        self['bg'] = 'white' # background color
        self['fg'] = 'black' # text color
        self['image'] = icon # icon of the button
        self['height'] = 60  # size
        #self['width'] = 120
        self['compound'] = RIGHT # compound
        self['font'] = TkFont.Font(family="Rubik", size=18)  #font
        self['relief'] = "flat" # type of the button's border
        self['anchor'] = E # starts from east