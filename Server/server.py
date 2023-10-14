
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('10.0.0.25', 6080))

print("server is running...")

server_socket.listen()
conn, address = server_socket.accept()


file = open(r'C:\Users\ravid\OneDrive\מסמכים\GitHub\PythonCyberProject2023\Server\database.json', 'rb')

data = file.read()
conn.sendall(data)
conn.send(b'<END>')

file.close()
server_socket.close()