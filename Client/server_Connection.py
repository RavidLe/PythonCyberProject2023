import socket
import time
import rsa
import symetricalEnc  # Ensure that this module is properly implemented and available

# Class responsible for the communication with the server
class ServerConnection:
    def __init__(self, HOST, PORT, FORMAT):
        self.host = HOST
        self.port = PORT
        self.format = FORMAT
        # Creating a private and public key for asymmetric encryption
        self.public_key, self.private_key = rsa.newkeys(1024)  

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def set_username(self, username):
        self.username = username

    def set_password(self, password):
        self.password = password

    def load_info(self):
        # Creating a TCP connection with the server
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # trying to connect to server if fails send error message
        try:
            conn.connect((self.host, self.port))
        except:
            return "error" 

        # Receiving the server's public key for asymmetric encryption
        server_public = rsa.PublicKey.load_pkcs1(conn.recv(1024))

        # Sending the username and password to the server
        conn.send(rsa.encrypt(self.get_username().encode(self.format), server_public))
        time.sleep(0.1)
        conn.send(rsa.encrypt(self.get_password().encode(self.format), server_public))
        time.sleep(0.1)

        # Receiving the server's response
        ans = conn.recv(1024).decode(self.format)
        if ans == "denied":
            conn.close()
            return ans
        elif ans != "allowed":
            conn.close()
            return ans

        # Sending a command to the server
        conn.send(rsa.encrypt("/get".encode(self.format), server_public))
        time.sleep(0.1)

        # Sending the client's public key to the server
        conn.send(self.public_key.save_pkcs1("PEM"))

        # All messages from now on will be encrypted using symmetric encryption

        # Receiving the symmetric key for encryption
        key = rsa.decrypt(conn.recv(1024), self.private_key)

        # Receiving the file (database) in chunks and decrypting it
        file_bytes = b""  # Container for the received bytes
        done = False  # Indicates if the transfer is complete

        while not done:
            data = conn.recv(1024)  # Receiving data in packets
            file_bytes += data
            if file_bytes[-5:] == b"<END>":  # Check for end of file marker
                done = True  # Mark as done if end marker is found

        # Save the received data to a file
        file = open("data", "wb")
        file.write(symetricalEnc.decrypt(file_bytes[:-5], key).encode(self.format))  # Decrypt and write to file without the last five bytes (<END>)
        file.close()

        conn.close()  # Close the connection
        return ans

    def send_info(self, info):
        # Creating a TCP connection with the server
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((self.host, self.port)) 

        # Receiving the server's public key for asymmetric encryption
        server_public = rsa.PublicKey.load_pkcs1(conn.recv(1024))

        # Sending the username and password to the server
        conn.send(rsa.encrypt(self.get_username().encode(self.format), server_public))
        time.sleep(0.1)
        conn.send(rsa.encrypt(self.get_password().encode(self.format), server_public))
        time.sleep(0.1)

        # Sending a command to the server
        conn.send(rsa.encrypt("/send".encode(self.format), server_public))
        
        # Sending each piece of info in a separate packet
        for data in info:
            conn.send(rsa.encrypt(str(data).encode(self.format), server_public))
            time.sleep(0.1)  # Delay to prevent packet mixing

        conn.close()  # Close the connection

    def send_report(self, info):
        # Creating a TCP connection with the server
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((self.host, self.port)) 

        # Receiving the server's public key for asymmetric encryption
        server_public = rsa.PublicKey.load_pkcs1(conn.recv(1024))

        # Sending the username and password to the server
        conn.send(rsa.encrypt(self.get_username().encode(self.format), server_public))
        time.sleep(0.1)
        conn.send(rsa.encrypt(self.get_password().encode(self.format), server_public))
        time.sleep(0.1)

        # Sending a command to the server
        conn.send(rsa.encrypt("/report".encode(self.format), server_public))

        # Sending each piece of info in a separate packet
        for data in info:
            conn.send(rsa.encrypt(str(data).encode(self.format), server_public))
            time.sleep(0.1)  # Delay to prevent packet mixing

        conn.close()  # Close the connection
