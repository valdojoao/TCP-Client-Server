
import unittest, threading, time
from platform import python_version

import threadServer as server
import threadClient as clients
from datetime import datetime


class TestSum(unittest.TestCase): 
  
    #[1] Requirement:  python > 3.5.x
    def test_version(self): 
  
        current_version = float(python_version()[:3])        
        min_version  = 3.5       
        check = False
        
        if (current_version >= min_version):
            check = True
            
        self.assertEqual(True, check,  f'your Python version is = {current_version} while the min requirement is = {min_version} ') 
        
        
    #[2] Requirement:  The server should listen on port 3443
    def test_port(self):
    
      port = server.conn_params()
      port = int( port.split()[-1] )      
      req_port = 3443      
      self.assertEqual(port, req_port,  f'port is = {port} while the required port is = {req_port} ') 
          
            
    def test_send_receive(self):
    
      #[3] Requirement: The server should accept a maximum of 100 connected clients
      with self.subTest():
        test_max_clients(self)           
    
      #put the server ready to receive connections from clients
      t1 = threading.Thread(target = server.connect_clients)
      t1.start()      
      time.sleep(0.2)
      
      #client send a connection request to server
      clients.connect_server()      
      
      #[4] Requirement: The client should connect to the server with a TLS connection
      with self.subTest():      
        test_tls(self)
      
      #[5] Requirement: The client should receive the current date from the server every 10 seconds.
      with self.subTest():      
        test_date(self)  
       
      #[6] Requirement: The client should send a text message to the server, the server should respond with the same string but reversed.
      with self.subTest():
        test_input(self)     
        
      #send q to close connection
      clients.send(string_output = 'q')


 #[3] Requirement: The server should accept a maximum of 100 connected clients
def test_max_clients(max_clients):
  server.connected_clients = 100            #impose that 100 clients are already connected
  message = server.connect_clients()    #ask the server if is still possible to connect
  expected_msg = "can't connect, max number of clients reached"
        
  max_clients.assertEqual(message, expected_msg) 
  
  server.connected_clients = 0              #reset the number of connected clients


#[4] Requirement: The client should connect to the server with a TLS connection
def test_tls(tls):
  tls_version = clients.client.version()
  expected_tls= "TLSv1.3"        
  tls.assertEqual(tls_version, expected_tls)  
 
 
 #[5] Requirement: The client should receive the current date from the server every 10 seconds.
def test_date(date):
  date_1 = clients.receive()  #receive 1st date    
  time.sleep(12)
  date_2 = clients.receive()    #receive 2nd date
   
  #verify if the diff is 10 seconds
  diff = cal_date_diff(date_1, date_2)
  expected_dif = "0:00:10"    #0 days, 0 hours and 10 seconds        
  date.assertEqual(diff, expected_dif)   

# calculate the diff beween two dates
def cal_date_diff(date_1, date_2):
  
  date_1 = date_1.split()[-2:]
  date_1 = "{} {}".format(date_1[0], date_1[1]) 
      
  date_2 = date_2.split()[-2:]
  date_2 = "{} {}".format(date_2[0], date_2[1]) 
  
  date_1 = datetime.strptime(date_1, "%d/%m/%Y %H:%M:%S")
  date_2 = datetime.strptime(date_2, "%d/%m/%Y %H:%M:%S")

  result = str(date_2 - date_1)
  return result
  
  
#[6] Requirement: The client should send a text message to the server, the server should respond with the same string but reversed
def test_input(input):

  input_list = ['roma', 'genova']
  expected_list = ['amor', 'avoneg']

  clients.send(string_output = input_list)

  output_list = []
  prefix = "Reversed input : "

  #remove output prefix and save the result
  for i in range(len(input_list)):
      out = clients.receive().replace(prefix, "")
      output_list.append(out)

  input.assertEqual(output_list, expected_list)

 
if __name__ == "__main__":

  unittest.main() 
