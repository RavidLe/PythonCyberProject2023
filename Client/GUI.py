from classes import *

# Create the main application window
app = App()

# Set all the buttons in the menu
menu_btns = []
menu_btns_text = ["מפה   ", "הוספה   ", "דיווח   "]  # Titles of buttons
icons = [
    ImageTk.PhotoImage(Image.open("Client\Icons\map.png").resize((30, 30))),
    ImageTk.PhotoImage(Image.open("Client\Icons\more.png").resize((30, 30))),
    ImageTk.PhotoImage(Image.open("Client\Icons\ireport.png").resize((30, 30))),
]  # Icons of buttons

# Create the frames for each section of the application
map_page = TapLocationsMapPage(app)  # A map with the location of taps
add_page = AddPage(connection, app)  # For adding taps
report_page = ReportPage(connection, app )  # For reporting problems
menu_page = Frame(app, bg='white')  # Creating the menu frame

# Create the login frame
login_page = loginPage([map_page, add_page, report_page, menu_page], connection, app)

# Place the login frame
login_page.grid(column=0, row=0, sticky="nwes")

# Define the command for the buttons
def commandbtn(frame):
    frame.tkraise()  # Raise the chosen page

# Set the title of the buttons and configure their commands
for i in range(len(menu_btns_text)):
    menu_btns.append(MenuButton(icons[i], menu_page, text=menu_btns_text[i]))

menu_btns[0].configure(command=lambda: commandbtn(map_page))
menu_btns[1].configure(command=lambda: commandbtn(add_page))
menu_btns[2].configure(command=lambda: commandbtn(report_page))

# Place the buttons in the menu frame
for i in range(len(menu_btns_text)):
    menu_btns[i].grid(row=i, column=0, padx=10, pady=5, sticky="ewsn")

# Adjust the grid for the menu frame and main application window
Grid.columnconfigure(menu_page, 0, weight=1)
Grid.rowconfigure(app, 0, weight=1)
Grid.columnconfigure(app, 0, weight=6)
Grid.columnconfigure(app, 1, weight=1)

# Raise the login frame to be on top initially
login_page.tkraise()

# Start the main loop of the application
app.mainloop()