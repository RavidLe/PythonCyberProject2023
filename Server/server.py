import threading
import socket
import mysql.connector
import json

HOST = '10.0.0.25'
PORT = 9090
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

def handle_client(conn, addr):
            print(f"Request from {addr}")
            command = conn.recv(1024).decode(FORMAT)
            print(f"command type: {command}")

            if command == 'get':

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

                conn.send(json_data.encode('utf-8'))

                
            elif command == 'send':

                name = conn.recv(1024).decode(FORMAT)
                coord_X = float(conn.recv(1024).decode(FORMAT))
                coord_Y = float(conn.recv(1024).decode(FORMAT))
                score = float(conn.recv(1024).decode(FORMAT))

                print("added:" + name + str(coord_X) + str(coord_Y) + str(score))

                db = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="12345",
                    database="water_taps"
                )

                mycursor = db.cursor()
                mycursor.execute(f"INSERT INTO Taps (Name, X_coord, Y_coord, Score) VALUES ('{name}', {coord_X}, {coord_Y}, {score})")
                db.commit()
                print("DONE!")
                

                mycursor.execute("SELECT * FROM Taps")

                columns = [column[0] for column in mycursor.description]
                data = [dict(zip(columns, row)) for row in mycursor.fetchall()]

                json_data = json.dumps(data, indent=4)
                print(json_data)


def start():
    print("Running...")
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

start()       
