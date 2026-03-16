import socket
import argparse

# Defines port number
ECHO_PORT = 9999
# Defines the buffer size
BUF_SIZE = 4096

# main method of the client
def main():
    # creates a parser to find the arguments to be used for the rest of the method
    parser = argparse.ArgumentParser()
    parser.add_argument(dest="server_ip",action='store', help='server ip')
    parser.add_argument(dest="server_port",action='store', help='server port')
    args = parser.parse_args()
    # Defines the server IP address
    serverIP = args.server_ip
    # Try except block to define the server port. If an error is thrown because the port is not a valid number,
    # prints a message saying that the port needs to be a valid number and exits
    try: 
        serverPort = int(args.server_port)
    except ValueError as e:
        print("port number needs to be a valid number")
        exit(1)
    # Try except block to define the client socket. If an error is thrown in the creation of the socket,
    # prints a message that the socket failed to be created and the error that occured
    try: 
        clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    except socket.error as err: 
        print ("socket creation failed with error %s" %(err))
    # Connects the client socket to the port of the server
    clientSock.connect((serverIP, serverPort))
    # Sets the socket to be non-blocking
    clientSock.setblocking(0)
    # Starts sending the data
    data = input("Please enter the message: ")
    print("Sending ", data)
    clientSock.send(data.encode())
    # Recieves the data was sent back
    while True:
        try:
            recvData = clientSock.recv(BUF_SIZE)
            if recvData:
                break
        except BlockingIOError:
            continue
    # If it didn't recieve the data back, prints an error message and exits
    if not recvData:
        print("Error reading from client socket")
        exit(1)
    # Otherwise, prints that it's recieving and then closes the socket
    print("Receiving ", recvData.decode())
    clientSock.close()

# Runs the main method
if __name__ == '__main__':
    main()
