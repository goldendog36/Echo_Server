import socket
import select

# Defines port number
ECHO_PORT = 9999
# Defines the buffer size
BUF_SIZE = 4096

# main method of the server
def main():
    print("----- Echo Server -----") # Simple title
    # try except block to create a server socket. If an error is thrown in the creation of the socket,
    # prints a message that the socket failed to be created and the error that occured.
    try:
        serverSock = socket.socket()
    except socket.error as err:
        print ("socket creation failed with error %s" %(err))
        exit(1)
    # defines different aspects of the server socket
    serverSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSock.bind(('0.0.0.0', ECHO_PORT))
    serverSock.listen(5)
    serverSock.setblocking(0)
    # Creates an epoll object and registers the server socket to it
    epoll = select.epoll()
    epoll.register(serverSock.fileno(), select.EPOLLIN)
    # Creates dictionaries to keep track of the connections, requests, and responses of the server
    connections = {}
    requests = {}
    responses = {}
    hasSomething = False

    # Starts an infinite loop to keep the server running and to check for events on the epoll object.
    # If there is an event on the server socket, it accepts the connection and registers it to the epoll object.
    # If there is an event on a client socket, it checks if it's an EPOLLIN event, in which case it receives the
    # data from the client and modifies the event to be an EPOLLOUT event. If it's an EPOLLOUT event, it sends
    # the response back to the client and modifies the event back to an EPOLLIN event. If it's an EPOLLHUP event,
    # it unregisters the socket and closes the connection.
    while True:
        events = epoll.poll(1)
        for fd, event in events:
            if fd == serverSock.fileno():
                connection, addr = serverSock.accept()
                connection.setblocking(0)
                epoll.register(connection.fileno(), select.EPOLLIN)
                connections[connection.fileno()] = connection
                requests[connection.fileno()] = b''
                responses[connection.fileno()] = b''
            elif event & select.EPOLLIN:
                if fd in connections:
                    requests[fd] += connections[fd].recv(BUF_SIZE)
                if requests[fd] == b'':
                    epoll.unregister(fd)
                    connections[fd].close()
                    del connections[fd]
                    del requests[fd]
                    del responses[fd]
                else:
                    responses[fd] = requests[fd]
                    epoll.modify(fd, select.EPOLLOUT)
                    print("Received ", requests[fd].decode('latin-1'))
            elif event & select.EPOLLOUT:
                byteswritten = connections[fd].send(responses[fd])
                responses[fd] = responses[fd][byteswritten:]
                if len(responses[fd]) == 0:
                    epoll.modify(fd, select.EPOLLIN)
                    print("Sent ", requests[fd].decode('latin-1'))
                    requests[fd] = b''
            elif event & select.EPOLLHUP:
                epoll.unregister(fd)
                connections[fd].close()
                del connections[fd]
                del requests[fd]
                del responses[fd]
    epoll.unregister(serverSock.fileno())
    epoll.close()
    serverSock.close()

# runs the main method
if __name__ == '__main__':
    main()
