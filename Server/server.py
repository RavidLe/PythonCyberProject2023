import threading
import socket

def get_data():
    print('wating for data')
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('10.0.0.25', 6081))
    server_socket.listen()
   

    

    
    while True:
        conn, address = server_socket.accept()

        print("server is getting data from "+ address)

        data = conn.recv(1024)

        print(data)

        conn.close()
    
def send_data():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('10.0.0.25', 6080))
    server_socket.listen()
    

    

    
    while True:
        try:
            conn, address = server_socket.accept()
            print("server is sending data to "+ str(address))

            file = open(r'C:\Users\ravid\OneDrive\מסמכים\GitHub\PythonCyberProject2023\Server\database.json', 'rb')

            data = file.read()
            conn.sendall(data)
            conn.send(b'<END>')
            print('data send!')

            file.close()
            conn.close()
        except:
            pass

threading.Thread(target=send_data).start()
get_data()
