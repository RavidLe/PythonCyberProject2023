


# Import necessary modules
from tkinter import *
import tkintermapview
import tkinter.font as TkFont
from PIL import Image, ImageTk
import json


marker_icon = Image.open('client\Icons\icon5806.png')



# Define the login frame class
class loginPage(Frame):
    def __init__(self, frames, connection, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self['bg'] = 'white'

        # Function to handle login
        def login():
            

            username = self.username_entry.get()
            password = self.password_entry.get()

             # set the username and password to the connection
            connection.set_username(username)
            connection.set_password(password)


            # trying to get data and reciving answer from the server
            login_status = connection.load_info()

            # if the answer is positive
            if login_status == "allowed":
                self.destroy() # destroy the login page
                # set the frames for the UI
                for i, frame in enumerate(frames[:-1]):
                    frame.grid(row=0, column=0, padx=1, sticky="nsew")
                frames[i + 1].grid(row=0, column=1, padx=1, sticky="nsew")
                frames[0].tkraise()
                frames[0].set_map() # setting the map with the data that was just sent from the server
            
            # if the answer is negative or other answer send a error msg
            else:
                error_msg = Label(
                    self,
                    text="שגיאה בפרטים" if login_status == "denied" else "בעיית תקשרות",
                    bg='white', fg='red', font=TkFont.Font(family="Rubik", size=24)
                )
                error_msg.place(relx=1, rely=0.5, anchor='e')
                error_msg.after(2000, lambda: error_msg.destroy()) # destroying the msg after 2 sec
                # clear the entry boxes
                self.username_entry.delete(0, END)
                self.password_entry.delete(0, END)

        # UI components for login frame
        self.title = Label(self, text="!TAPMAPברוכים הבאים ל", bg='white', font=TkFont.Font(family="Rubik", size=36))
        self.username_label = FormLabel(self, text=":שם משתמש")
        self.password_label = FormLabel(self, text=":סיסמא")

        self.username_entry = EntryInfo(self)
        self.password_entry = EntryInfo(self, show="*")

        self.login_button = Button(self, text="התחברות", bg="light cyan", font=TkFont.Font(family="Rubik", size=36), command=login)

        # Place UI components
        self.title.pack(anchor="n", pady=50)
        self.username_label.pack(anchor="n")
        self.username_entry.pack(anchor="n")
        self.password_label.pack(anchor="n")
        self.password_entry.pack(anchor="n")
        self.login_button.pack(pady=40, anchor="n")

# Define the main application class
class App(Tk):
    def __init__(self):
        super().__init__()
        self["bg"] = "white"
        self.geometry('1120x630')
        self.minsize(1120, 630)
        self.iconbitmap('Client\Icons\iconapp.ico')
        iconphoto = PhotoImage(file='Client\Icons\iconphoto.png')
        self.iconphoto(True, iconphoto)
        self.title("TapMap")

# Define the class for water map markers
class WaterMapMarker:
    def __init__(self, watermap, watertap):
        self.name = watertap['Name']
        self.score = watertap['Score']
        self.x = watertap['X_coord']
        self.y = watertap['Y_coord']
        self.watermap = watermap

        self.icon = ImageTk.PhotoImage(marker_icon.resize((12, 12))) # loading the icon of the marker
        self.marker = watermap.set_marker(self.x, self.y, icon=self.icon) # create a marker
        # create the polygon around the marker
        self.marker_polygon = watermap.set_polygon(
            [(self.x + 0.005, self.y), (self.x, self.y + 0.005), (self.x - 0.005, self.y), (self.x, self.y - 0.005)],
            border_width=0, outline_color=None, fill_color=None
        )

    # Get methods for marker properties
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

    # Update marker size based on zoom level
    def update_size(self, zoom):
        zoom = max(zoom, 8) # minimun is 8
        newsize = int((zoom - 7) ** 1.5) + 10 # the new size of the icons
        # updating the new size
        self.icon = ImageTk.PhotoImage(marker_icon.resize((newsize, newsize))) 
        self.marker.change_icon(self.icon)

        # update the size of the polygon according to zoom
        update_size = pow(0.005, float(zoom) / 10) # update size = 0.005^zoom/10 
        # set the new ploygon
        self.marker_polygon = self.watermap.set_polygon(
            [(self.x + update_size, self.y), (self.x, self.y + update_size), (self.x - update_size, self.y), (self.x, self.y - update_size)],
            border_width=0, outline_color=None, fill_color=None
        )

# Define the frame for displaying marker information
class MarkerFrame(Frame):
    def __init__(self, container, name, score):
        super().__init__(container)
        self.score = score
        self.name = name

        # choosing the color according to the score
        if score < 1:
            backgroundcolor = "saddle brown"
        elif score < 2:
            backgroundcolor = "red"
        elif score < 3:
            backgroundcolor = "orange"
        elif score < 4:
            backgroundcolor = "yellow green"
        elif score < 4.7:
            backgroundcolor = "dark green"
        else:
            backgroundcolor = "blue2"

        if len(name) > 25:
            textsize = 20
        else:
            textsize = 25

        Label(self, text=f"שם הברזייה: {self.name}", bg="white", font=TkFont.Font(family="Rubik", size=textsize)).pack(ipadx=20, side="right")
        Label(self, text=":דירוג", bg="white", font=TkFont.Font(family="Rubik", size=textsize)).pack(ipadx=20, side="right")
        Label(self, text=str(self.score), bg=backgroundcolor, fg='white', font=TkFont.Font(family="Rubik", size=30)).pack(ipadx=20, side="right")
        self['bg'] = 'white'

# Define the map class
class Map(tkintermapview.TkinterMapView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_zoom = 18
        self.set_address("32.0852937, 34.7816499")
        self.set_zoom(10)
        self.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga")

# Define the class for choosing a location on the map
class ChooseLocationMap(Frame):
    def __init__(self, entry_box, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.map = Map(self)

        # Handle left click events on the map
        def left_click_event(coordinates_tuple):
            self.map.delete_all_marker()
            def Send():
                entry_box.location_entry.insert(0, coordinates_tuple)
                self.destroy()

            self.x_pos, self.y_pos = coordinates_tuple
            self.map.set_marker(self.x_pos, self.y_pos, text="")
            if self.map.zoom < 15:
                self.map.set_zoom(15)
            self.map.set_position(self.x_pos, self.y_pos)

            self.ChooseBtn = Button(self, text="בחר", bg="light green",
                               font=TkFont.Font(family="Rubik", size=24), relief="ridge", borderwidth=1, command=Send)
            self.ChooseBtn.place(relx=0.5, rely=1, anchor="s")

        self.map.add_left_click_map_command(left_click_event)
        self.map.grid(row=0, column=0, sticky="nsew")

        Grid.rowconfigure(self, 0, weight=1)
        Grid.columnconfigure(self, 0, weight=1)

# Define the frame for displaying the tap locations on the map
class TapLocationsMapPage(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

    # Set the map with tap locations
    def set_map(self):
        self.watermap = Map(self)
        self.taps = []
        self.widgets = {}

        with open('data') as f:
            self.data = json.load(f)

        for watertap in self.data:
            tap = WaterMapMarker(self.watermap, watertap)
            self.taps.append(tap)
            self.widgets[tap] = MarkerFrame(self.watermap, watertap['Name'], watertap["Score"])

        # Update zoom level
        def updatezoom(event):
            for tap in self.taps:
                tap.update_size(self.watermap.zoom)

        self.watermap.canvas.bind_all('<MouseWheel>', updatezoom)
        self.watermap.canvas.bind_all("<Button-1>", updatezoom)

        # when left clicked check if on tap
        def show(event):
            # check for every tap on the map
            for tap in self.taps:
                c = tap.get_marker_polygon().canvas_polygon_positions # the position of the tap
                # checking if the mouse was inside the polygon of the tap when clicked
                if c[1] < event.y < c[5] and c[6] < event.x < c[2]:
                    # if yes show the frame with the details about the taps
                    self.widgets[tap].grid(row=1, column=0, sticky="nsew")
                    self.widgets[tap].tkraise()
                    self.watermap.set_position(tap.get_x(), tap.get_y()) # center the map around the tap that was clicked

        self.watermap.canvas.bind_all("<Button-1>", show)
        self.watermap.grid(row=0, column=0, sticky='nsew')
        Grid.rowconfigure(self, 0, weight=1)
        Grid.columnconfigure(self, 0, weight=1)

# Define the frame for adding a new tap location
class AddPage(Frame):
    def __init__(self, connection, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self['bg'] = 'white'

        # Function to enter data
        def enter_data():
            try:
                name = self.name_entry.get()
                x, y = self.location_entry.get().split()
                score = float(self.scale.get())
                connection.send_info([name, x, y, score])

                success = Label(self, text="הברזייה נוספה בהצלחה", fg="green", font=TkFont.Font(family="Rubik", size=20), bg="white")
                success.pack()
                success.after(2000, success.destroy)

                self.name_entry.delete(0, END)
                self.location_entry.delete(0, END)
                self.scale.set(0)
                
            except:
                fail = Label(self, text="חסרים פרטים", fg="red", font=TkFont.Font(family="Rubik", size=20), bg="white")
                fail.pack()
                fail.after(2000, fail.destroy)

        # UI components for adding a new tap
        self.title = Label(self, text="הוספת ברזייה", bg='white', font=TkFont.Font(family="Rubik", size=36))
        self.name_label = FormLabel(self, text=":שם הברזייה")
        self.location_label = FormLabel(self, text=":מיקום הברזייה")
        self.score_label = FormLabel(self, text=":דירוג הברזייה")

        self.name_entry = EntryInfo(self)
        self.location_entry = EntryInfo(self)
        def set_color(score):
            score = float(score)
            # choosing the color according to the score
            if score == 0:
                self.scale.config(bg="white", troughcolor="light cyan")
                return
            if score < 1:
                backgroundcolor = "chocolate4"
                throughcolor = "saddle brown"
            elif score < 2:
                backgroundcolor = "firebrick2"
                throughcolor = "firebrick4"
            elif score < 3:
                backgroundcolor = "orange"
                throughcolor = "orange2"
            elif score < 4:
                backgroundcolor = "chartreuse2"
                throughcolor = "chartreuse4"
            elif score < 4.7:
                backgroundcolor = "green2"
                throughcolor = "green4"
            else:
                backgroundcolor = "blue2"
                throughcolor = "blue4"
            
            if score >= 4:
                foregroundcolor = 'white'
            else:
                foregroundcolor = 'black'

            self.scale.config(bg = backgroundcolor,troughcolor = throughcolor, fg=foregroundcolor)

        self.scale = Scale(self, font=TkFont.Font(family="Rubik", size=18), bd=0, bg="white",
                       borderwidth=0,digits=2, from_ = 0, to = 5,
                         length = 250,resolution = 0.1, orient = HORIZONTAL, troughcolor = "light cyan", command=set_color) #creating a scale to chose score

        self.submit_button = Button(self, text="הוספה", bg="light cyan", font=TkFont.Font(family="Rubik", size=36), command=enter_data)
        self.location_button = Button(self, text="בחר מיקום", bg="light cyan", font=TkFont.Font(family="Rubik", size=10),
                                 command=lambda: ChooseLocationMap(self).grid(row=0, column=0, sticky='nsew', padx=1))
       
        

        # Place UI components
        self.title.pack(anchor = 'n', pady = 20)
        self.name_label.pack(anchor = 'n', pady = (10,0))
        self.name_entry.pack(anchor = 'n', pady = (0,10))
        self.location_label.pack(anchor = 'n', pady = (10,0))
        self.location_entry.pack(anchor = 'n')
        self.location_button.pack(anchor = 'n', pady = (0,10))
        self.score_label.pack(anchor = 'n', pady = (10,0))
        self.scale.pack(anchor = 'n', pady = (0,10))
        self.submit_button.pack(anchor = 'n', pady = 10)


        # Function to submit report
class ReportPage(Frame):
    def __init__(self, connection, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

        self['bg'] = 'white'  # Set the background color to white

        # Function to send the report
        def send(subject):
            try:
                # Get the selected subject from the drop-down menu
                report_subject = subject  # This line retrieves the last character from the selected subject
                # Get the report text from the text box
                report_text = self.report_details.get(1.0, END)
                # Send the report using the connection object
                connection.send_report([report_subject, report_text])
                
                # Display a confirmation message
                confirm_msg = Label(self, text="!דיווח נשלח בהצלחה", bg='white', fg='green', font=TkFont.Font(family="Rubik", size=24))
                confirm_msg.pack()
                confirm_msg.after(2000, lambda: confirm_msg.destroy())  # Remove the message after 2 seconds

            except:
                # Display an error message if no subject is selected
                error_msg = Label(self, text="לא נבחר נושא", bg='white', fg='red', font=TkFont.Font(family="Rubik", size=24))
                error_msg.pack()
                error_msg.after(500, lambda: error_msg.destroy())  # Remove the message after 2 seconds

            # Clear the input fields
            options.set("בחר")
            self.report_details.delete('1.0', END)

        # Main title of the page
        Label(self, font=TkFont.Font(family="Rubik", size=36), text="דיווח", bg='white').pack(ipady=10)

        # Subject label
        self.subject_label = FormLabel(self, text=":נושא")

        # Variable to hold the selected option from the drop-down menu
        options = StringVar(self)

        # List of options for the drop-down menu
        options_list = ["בחר", "בעיה בממשק המשתמש", "מיקום ברזייה שגוי", "שם לא נאות לברזייה", "אחר"]

        # Create a drop-down menu for selecting the report subject
        self.drop = OptionMenu(self, options, *options_list)
        options.set("בחר")  # Set the default value of the drop-down menu

        # Text label for the report details
        self.text_label = FormLabel(self, text=":פירוט הבעיה")

        # Text box for writing the report details
        self.report_details = Text(self, height=15, width=60, bg="ghost white")

        # Send button to submit the report
        self.send_button = Button(self, font=TkFont.Font(family="Rubik", size=24), text="שליחה", bg="light cyan", borderwidth=2, relief="ridge", command=lambda: send(options.get()))

        # Function to limit the number of characters in the text box
        def char_count(event):
            CHAR_LIMIT = 200
            # This function allows typing up to the character limit and allows deletion
            count = len(self.report_details.get('1.0', 'end-1c'))
            if count >= CHAR_LIMIT and event.keysym not in {'BackSpace', 'Delete'}:
                return 'break'  # Prevent further typing

        # Bind the character count function to key press and release events
        self.report_details.bind('<KeyPress>', char_count)
        self.report_details.bind('<KeyRelease>', char_count)

        # Place all the widgets in the frame
        self.subject_label.pack(anchor='n', pady=5)
        self.drop.pack(anchor='n', pady=5)
        self.text_label.pack(anchor='n', pady=5)
        self.report_details.pack(anchor='n', pady=5)
        self.send_button.pack(anchor='n', pady=5)

# Define a custom label class for form labels
class FormLabel(Label):
    def __init__(self, *args, **kwargs):
        Label.__init__(self, *args, **kwargs)
        self.config(bg="white", font=TkFont.Font(family="Rubik", size=24), anchor="e")

# Define a custom entry class for form inputs
class EntryInfo(Entry):
    def __init__(self, *args, **kwargs):
        Entry.__init__(self, *args, **kwargs)
        self.config(justify='right', relief="ridge", borderwidth=1, font=TkFont.Font(family="Rubik", size=20), bg="light cyan")

# Define the menu bar class
class MenuButton(Button):
    def __init__(self, icon, *args, **kwargs):
        Button.__init__(self, *args, **kwargs)
        
        self['bg'] = 'white'  # Set the background color to white
        self['fg'] = 'black'  # Set the text color to black
        self['image'] = icon  # Set the icon image for the button
        self['height'] = 60  # Set the height of the button
        # self['width'] = 120  # Set the width of the button (commented out)
        self['compound'] = RIGHT  # Position the icon to the right of the text
        self['font'] = TkFont.Font(family="Rubik", size=18)  # Set the font family and size
        self['relief'] = "flat"  # Set the button border to flat
        self['anchor'] = E  # Anchor the content to the east (right side)


