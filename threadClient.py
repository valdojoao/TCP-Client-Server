

import  threading, os, time, sys 
from socket import create_connection
from ssl import SSLContext, PROTOCOL_TLS_CLIENT


client = None 

#connect to server 
def connect_server():

  global client
  
  HOSTNAME ='example.org'
  SERVER = "127.0.0.1"
  PORT = 3443

  # PROTOCOL_TLS_CLIENT requires valid cert chain and hostname
  context = SSLContext(PROTOCOL_TLS_CLIENT)
  context.load_verify_locations('certificates/cert.pem')
  
  tls = create_connection((SERVER, PORT))  
  client =  context.wrap_socket(tls, server_hostname=HOSTNAME)  

  print("insert the  input  then press ENTER...")
  print("press q + ENTER so exit")
  print()


#send data to server
def send(string_output=None):  

  while True: 
    if(string_output == None): #input from keyboard
      out_data = input()    
      client.sendall(bytes(out_data,'UTF-8'))    
      
    else:
      for out_data in string_output: #input from code
        client.sendall(bytes(out_data,'UTF-8'))    
        
      break
    
    #if q end connection
    if out_data=='q':
        client.close()
        os._exit(0) 
      
#receive data from server
def receive():

    in_data =  client.recv(1024)
    print(in_data.decode())
    return in_data.decode()
    
    
def run_client():

  #do the sending on a different thread
  t1 = threading.Thread(target=send)
  t1.start()
  
  #in the main thread do the receiving
  while True:
    receive()

 
if __name__ == "__main__":

  connect_server()
  run_client()
  
  

