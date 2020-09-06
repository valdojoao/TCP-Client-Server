
from socket import socket, AF_INET, SOCK_STREAM
from ssl import SSLContext, PROTOCOL_TLS_SERVER

import threading, time
from datetime import datetime


class ServerThread():

    def __init__(self, clientAddress, clientsocket):
        
        self.csocket = clientsocket
        self.time_sleep = 10
        self.break_loop = False
        self.clientAddress = clientAddress
        
        print("New connection added:", self.clientAddress)
        

    def get_current_date(self):

        # datetime object containing current date and time
        now = datetime.now()        
        # dd/mm/YY H:M:S
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")        
        result = "{} {}".format("Date sent From Server :" , dt_string) 
        return result
        
            
    # The server should send the current date to each client every 10 seconds  
    def send_date(self):
    
      while True:    
        if self.break_loop:
          break
          
        date_to_send = self.get_current_date()
        self.csocket.send(bytes(date_to_send,'UTF-8'))
        time.sleep(self.time_sleep)
  

    def reverse_input(self, input):
    
      reversed =  "{} {}".format("Reversed input :" , input[::-1]) 
      return reversed
      
    
    #receive message, manage connections, send messages
    def process_input(self):

        msg = ''
        while True:
            data = self.csocket.recv(2048)            
            msg = data.decode()
            
            #if q, close connection from client, adjust number of connected clients, stop sending date every 10s to this client
            if msg=='q':        
            
              global connected_clients
              
              #protect with semaphores
              with lock:
                connected_clients -=1
                
              self.break_loop = True              
              break              
            
            #else, process input then send the result to client
            ms = self.reverse_input(msg)
            self.csocket.send(bytes(ms,'UTF-8'))

        process_output = "{} {}".format("One client disconnected, currently connected clients: ", connected_clients) 
        print(process_output)
        return process_output


def conn_params():
    conn_output = "{} {}{} {}".format("Listening on host:", LOCALHOST, " port:", PORT)
    print(conn_output)
    return conn_output


#accept connection request from clients, start threads
def connect_clients():

    global connected_clients
    
    if connected_clients < MAX_CLIENTS:

        clientsock, clientAddress = tls.accept()

        newthread = ServerThread(clientAddress, clientsock)
        
        t1 = threading.Thread(target = newthread.send_date)
        t2 = threading.Thread(target = newthread.process_input)
        
        t1.start()
        t2.start()
        
        #protect with semaphores
        with lock:
            connected_clients += 1

        conn_output = "{} {}".format("Number of clients connected : ", connected_clients) 
        print(conn_output)
        
    else:
        conn_output = "can't connect, max number of clients reached"
    
    return conn_output
        
    
#global variables
LOCALHOST = "127.0.0.1"
PORT = 3443
MAX_CLIENTS = 100

connected_clients = 0

# PROTOCOL_TLS_CLIENT requires valid cert chain and hostname
# SSLContext helps manage settings and certificates which can be inherited by SSL sockets created through SSLContext.wrap_socket()
context = SSLContext(PROTOCOL_TLS_SERVER)
context.load_cert_chain('certificates/cert.pem', 'certificates/key.pem')

#AF_INET means ipv4, as opposed to ipv6 with AF_INET6
#SOCK_STREAM means it will be a TCP socket
server = socket(AF_INET, SOCK_STREAM)
server.bind((LOCALHOST, PORT))

#listen for incoming connections. We can only handle one connection at a given time, 
#allows for some sort of a queue. If someone attempts to connect while the queue is full, they will be denied.
server.listen(5)

tls = context.wrap_socket(server, server_side = True)

print("Server started")
print("Waiting for client request")

lock = threading.Lock()

if __name__ == "__main__":

    conn_params()
    
    while True:
        connect_clients()



    