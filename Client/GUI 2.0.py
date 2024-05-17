from classes import *



app = App() # creating a main window

user = User() # user class

# set all the buttons in the menu
menu_btns = [] 
menu_btns_text = ["מפה   ", "הוספה   ", "דיווח   "] # title of buttons
icons = [
    ImageTk.PhotoImage(Image.open("Client\Icons\map.png").resize((30, 30))),
    ImageTk.PhotoImage(Image.open("Client\Icons\more.png").resize((30, 30))),
    ImageTk.PhotoImage(Image.open("Client\Icons\ireport.png").resize((30, 30))),
    
] # icons of buttons

map_frame = TapLocationsMapFrame(app) # a map with the location of taps
add_frame = AddFrame(user, app) # for adding taps
report_frame = ReportFrame(user, app) # for reporting problems

menu_frame = Frame(app, bg='white') # creating the menu frame 

login_frame = loginFrame([map_frame, add_frame, report_frame, menu_frame], user, app) # to login

# placing login frame
login_frame.grid(column=0, row=0, sticky="nwes")

# command of the buttons
def commandbtn(frame):
    frame.tkraise() # raisng the chosen page
    
    

# setting the title of the buttons
for i in range(len(menu_btns_text)):
    menu_btns.append(Menu_Button(icons[i], menu_frame, text=menu_btns_text[i]))

# setting the commands of the buttons
menu_btns[0].configure(command=lambda: commandbtn(map_frame))
menu_btns[1].configure(command=lambda: commandbtn(add_frame))
menu_btns[2].configure(command=lambda: commandbtn(report_frame))


# placing the buttons
for i in range(len(menu_btns_text)):
  menu_btns[i].grid(row=i, column=0, padx=10, pady=5, sticky="ewsn")


Grid.columnconfigure(menu_frame, 0, weight=1) # adjusting the grid

# adjusting the grid
Grid.rowconfigure(app, 0, weight=1) 
Grid.columnconfigure(app, 0, weight=6)
Grid.columnconfigure(app, 1, weight=1)

login_frame.tkraise()

app.mainloop() # mainloop