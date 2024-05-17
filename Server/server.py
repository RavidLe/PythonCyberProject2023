import threading
import socket
import mysql.connector
import json
import rsa
import os 
from Crypto.Cipher import AES
import time
import datetime
import hashlib


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

    mycursor.execute("SELECT * FROM userdata WHERE username = %s AND %s", (username, password))

    if mycursor.fetchall():
         return True
    else:
         return False  
    


     
def handle_client(conn, addr):
            

            
    print(f"Request from {addr}")
    conn.send(public_key.save_pkcs1("PEM"))

    permission = check_permission(conn) 
    print(permission)
    if permission: # if the data is valid continue
         conn.send("allowed".encode(FORMAT))
         print("OK")

    else: # if not valid send an error msg
         conn.send("denied".encode(FORMAT))
         print("Not OK")
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
        print(json_data.encode(FORMAT))

        key = os.urandom(16)
        nonce = os.urandom(16)
        print(key)
        cipher = AES.new(key, AES.MODE_EAX, nonce)
                

        conn.send(rsa.encrypt(key, client_public))
        time.sleep(0.1)
        conn.send(rsa.encrypt(nonce, client_public))
        time.sleep(0.1)

        encrypted = cipher.encrypt(json_data.encode(FORMAT))
                

        conn.sendall(encrypted)
        conn.send(b"<END>")
        print("END")

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
            print("DONE!")
        except:
             conn.send("ERORR!".encode(FORMAT))
             print("ERORR IN THE DATA TYPE!")
                

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
        print("DONE!")



def start():
    print("Running...")
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

start()       
