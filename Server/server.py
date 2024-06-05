import threading
import socket
import mysql.connector
import json
import rsa
import time
import datetime
import hashlib
import os
import symetricalEnc

# Open the JSON file with database details
f = open("specs.json")
db_connect = json.load(f)

# Server details
HOST = '10.0.0.25'
PORT = 9090
FORMAT = 'utf-8'

# Create the server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

# Create RSA keys
public_key, private_key = rsa.newkeys(1024)

def check_permission(conn):
    # Get and decrypt the username from the client
    username = rsa.decrypt(conn.recv(1024), private_key).decode(FORMAT)
    
    # Get and decrypt the password from the client
    password = rsa.decrypt(conn.recv(1024), private_key)
    print(username, password)
    
    # Hash the password
    password = hashlib.sha256(password).hexdigest()
    
    # Connect to the database
    db = mysql.connector.connect(
        host=db_connect["host"],
        user=db_connect["user"],
        password=db_connect["password"],
        database=db_connect["database"]
    )
    
    mycursor = db.cursor()
    
    # Check if the username and password are in the database
    mycursor.execute("SELECT * FROM userdata WHERE username = %s AND password = %s", (username, password))
    
    # Return True if they are, False if not
    if mycursor.fetchall():
        return True
    else:
        return False

def handle_client(conn, addr):
    print(f"Request from {addr}")
    
    # Send the public key to the client
    conn.send(public_key.save_pkcs1("PEM"))
    
    # Check if the client has permission
    permission = check_permission(conn)
    
    if permission:  # If they do, send "allowed"
        conn.send("allowed".encode(FORMAT))
        print(f"{addr} allowed!")
    else:  # If they don't, send "denied" and close the connection
        conn.send("denied".encode(FORMAT))
        print(f"{addr} denied!")
        conn.close()
        return  # Exit the function
    
    # Get and decrypt the command from the client
    command = rsa.decrypt(conn.recv(1024), private_key).decode(FORMAT)
    print(f"command type: {command}")
    
    if command == '/get':  # If the command is '/get'
        # Get the client's public key
        client_public = rsa.PublicKey.load_pkcs1(conn.recv(1024))
        
        # Connect to the database
        db = mysql.connector.connect(
            host=db_connect["host"],
            user=db_connect["user"],
            password=db_connect["password"],
            database=db_connect["database"]
        )
        
        mycursor = db.cursor()
        
        # Get data from the Taps table
        mycursor.execute("SELECT * FROM Taps")
        
        # Convert the data to JSON
        columns = [column[0] for column in mycursor.description]
        data = [dict(zip(columns, row)) for row in mycursor.fetchall()]
        json_data = json.dumps(data, indent=4)
        print("sending data...")
        
        # Create a random key for encryption
        key = os.urandom(16)
        
        # Encrypt the key with the client's public key and send it
        conn.send(rsa.encrypt(key, client_public))
        time.sleep(0.1)
        
        # Encrypt the JSON data and send it
        encrypted = symetricalEnc.encrypt(json_data.encode(FORMAT), key)
        conn.sendall(encrypted.encode(FORMAT))
        conn.send(b"<END>")
        print("Done")
        conn.close()
    
    elif command == '/send':  # If the command is '/send'
        # Connect to the database
        db = mysql.connector.connect(
            host=db_connect["host"],
            user=db_connect["user"],
            password=db_connect["password"],
            database=db_connect["database"]
        )
        
        mycursor = db.cursor()
        
        # Try to insert new data into the Taps table
        try:
            sql = "INSERT INTO Taps (Name, X_coord, Y_coord, Score) VALUES (%s, %s, %s, %s)"
            val = (
                rsa.decrypt(conn.recv(1024), private_key).decode(FORMAT),
                float(rsa.decrypt(conn.recv(1024), private_key).decode(FORMAT)),
                float(rsa.decrypt(conn.recv(1024), private_key).decode(FORMAT)),
                float(rsa.decrypt(conn.recv(1024), private_key).decode(FORMAT))
            )
            mycursor.execute(sql, val)
            db.commit()
            print(f"Adding new data from {addr}")
        except:
            conn.send("ERROR!".encode(FORMAT))
            print(f"ERROR IN THE DATA TYPE FROM {addr}!")
        
        # Get data from the Taps table and print it
        mycursor.execute("SELECT * FROM Taps")
        columns = [column[0] for column in mycursor.description]
        data = [dict(zip(columns, row)) for row in mycursor.fetchall()]
        json_data = json.dumps(data, indent=4)
        print(json_data)
    
    elif command == "/report":  # If the command is '/report'
        # Connect to the database
        db = mysql.connector.connect(
            host=db_connect["host"],
            user=db_connect["user"],
            password=db_connect["password"],
            database=db_connect["database"]
        )
        
        mycursor = db.cursor()
        
        # Possible subjects for the report
        ps = ["בעיה בממשק המשתמש", "מיקום ברזייה שגוי", "שם לא נאות לברזייה", "אחר"]
        
        # Get and decrypt the subject from the client
        subject = rsa.decrypt(conn.recv(1024), private_key).decode(FORMAT)
        
        # Check if the subject is valid
        if subject not in ps:
            subject = ps[3]  # If not, set it to "אחר" (Other)
        
        # Get and decrypt the details from the client
        details = rsa.decrypt(conn.recv(1024), private_key).decode(FORMAT)
        
        # Get the current time (without milliseconds)
        current_time = str(datetime.datetime.now())[:-7]
        
        # Insert the report into the database
        sql = "INSERT INTO reports (subject, details, Date) VALUES (%s, %s, %s)"
        val = (subject, details, current_time)
        
        mycursor.execute(sql, val)
        db.commit()
        print(f"Received report from {addr}")

def start():
    print("Running...")
    server.listen()
    while True:
        # Accept new connections
        conn, addr = server.accept()
        # Handle each client connection in a new thread
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

start()
