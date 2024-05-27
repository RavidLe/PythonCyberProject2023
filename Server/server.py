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


HOST = '10.0.0.25'
PORT = 9090
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

public_key, private_key = rsa.newkeys(1024)

def check_permission(conn):
    username = rsa.decrypt(conn.recv(1024), private_key).decode(FORMAT)

    password = rsa.decrypt(conn.recv(1024), private_key)

    print(username, password)
    password = hashlib.sha256(password).hexdigest()

    db = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="12345",
                    database="water_taps"
                )
    
    mycursor = db.cursor()

    mycursor.execute("SELECT * FROM userdata WHERE username = %s AND password = %s", (username, password))

    if mycursor.fetchall():
         return True
    else:
         return False  
    


     
def handle_client(conn, addr):
            

            
    print(f"Request from {addr}")
    conn.send(public_key.save_pkcs1("PEM"))

    permission = check_permission(conn)
     
    if permission: # if the data is valid continue
         conn.send("allowed".encode(FORMAT))
         print(f"{addr} allowed!")

    else: # if not valid send an error msg
         conn.send("denied".encode(FORMAT))
         print(f"{addr} denied!")
         conn.close()
         return # exit the function

    command = rsa.decrypt(conn.recv(1024), private_key).decode(FORMAT)
    print(f"command type: {command}")

    if command == '/get':

        client_public = rsa.PublicKey.load_pkcs1(conn.recv(1024))

        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",
            database="water_taps"
        )

        mycursor = db.cursor()

        mycursor.execute("SELECT * FROM Taps")

        columns = [column[0] for column in mycursor.description]
        data = [dict(zip(columns, row)) for row in mycursor.fetchall()]

        json_data = json.dumps(data, indent=4)
        print("sending data...")

        key = os.urandom(16)

        
        conn.send(rsa.encrypt(key, client_public))
        time.sleep(0.1)
    
        encrypted = symetricalEnc.encrypt(json_data.encode(FORMAT), key)
                

        conn.sendall(encrypted.encode(FORMAT))
        conn.send(b"<END>")
        print("Done")

        conn.close()


                
    elif command == '/send':


        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",
            database="water_taps"
        )

        mycursor = db.cursor()

        # the data type might be worng and cause failure
        try:
            sql = "INSERT INTO Taps (Name, X_coord, Y_coord, Score) VALUES (%s, %s, %s, %s)"
            val = (rsa.decrypt(conn.recv(1024), private_key).decode(FORMAT),
                    float(rsa.decrypt(conn.recv(1024), private_key).decode(FORMAT)),
                    float(rsa.decrypt(conn.recv(1024), private_key).decode(FORMAT)),
                    float(rsa.decrypt(conn.recv(1024), private_key).decode(FORMAT)))

            mycursor.execute(sql, val)
                
            db.commit()
            print(f"Adding new data from {addr}")
        except:
             conn.send("ERORR!".encode(FORMAT))
             print(f"ERORR IN THE DATA TYPE FROM {addr}!")
                

        mycursor.execute("SELECT * FROM Taps")

        columns = [column[0] for column in mycursor.description]
        data = [dict(zip(columns, row)) for row in mycursor.fetchall()]

        json_data = json.dumps(data, indent=4)
        print(json_data)
            

    elif command == "/report":

        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",
            database="water_taps"
        )

        mycursor = db.cursor()

        ps = ["בעיה בממשק המשתמש", "מיקום ברזייה שגוי", "שם לא נאות לברזייה", "אחר"] # the possible subjects for the report

        subject = rsa.decrypt(conn.recv(1024), private_key).decode(FORMAT)

        if subject == ps[0] or subject == ps[1] or subject == ps[2] or subject == ps[3]: # checking if the subject that was recived is one of the above
                pass # if true dont do anything
        else:
                subject = ps[3] # if it doesn't match put it under the subject "other"

        details = rsa.decrypt(conn.recv(1024), private_key).decode(FORMAT) # reciving details
        current_time = str(datetime.datetime.now())[:-7] # getting the current time of the report, removing the last seven digits that show the miliseconds

        sql = "INSERT INTO reports (subject, details, Date) VALUES (%s, %s, %s)"
        val = (subject, details, current_time)

        mycursor.execute(sql, val)
                
        db.commit()
        print(f"recived report from {addr}")



def start():
    print("Running...")
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

start()       
