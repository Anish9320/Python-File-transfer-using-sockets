#this program will create an multithreaded Server using python socket server
import socket
import threading
import os
import tkinter as tk
import datetime
from tkinter import messagebox as message
import time
#to handle clients in multithreaded Server
client_log = open("D:/VOID MAIN()/Python-project/MultiServer-Client/ServerFiles/LOG/LOG.txt","a")
client_log_read = open("D:/VOID MAIN()/Python-project/MultiServer-Client/ServerFiles/LOG/LOG.txt","r")
server_running = False
def handle(client_socket, addr):
    global mac
    try:
        while True:
            # this loop will work for msg passing server -> client
            add = client_socket.recv(1024 * 1024 * 1024).decode()
            if add[:3] == "MAC":
                print("\nAddress", add[3:])
                try:
                    filename = client_socket.recv(1024 * 1024 * 1024).decode()
                    print("filename: ", filename)
                    file_contents = client_socket.recv(1024 * 1024 * 1024).decode()
                    print("DATA: ", file_contents)
                    try:
                        with open(f"D:/void main()/Python-project/MultiServer-Client/ServerFiles/{add[3:].replace(':', '')}/{filename}", "w") as file:
                            file.write(file_contents)
                        print("Received: ", filename, " From Client: ", client_socket)
                        # response = "Accepted"
                        # client_socket.send(response.encode())
                    except Exception as a:
                        print("Error: ",a)
                except Exception as e:
                    print("E:- ",e)
                    
            elif add[:3] == "get":
                files = os.listdir("D:/void main()/Python-project/MultiServer-Client/ServerFiles/"+add[3:].replace(":",""))
                files = str(files)
                client_socket.send(files.encode())
                file_status = client_socket.recv(1024 * 1024 * 1024).decode()
                if file_status == "1":  
                    rev_file_name = client_socket.recv(1024 * 1024 * 1024).decode()
                    try:
                        with open(f"D:/void main()/Python-project/MultiServer-Client/ServerFiles/{add[3:].replace(':', '')}/{rev_file_name}", "r") as file:
                            data =  file.read()
                        client_socket.send(rev_file_name.encode())
                        client_socket.send(data.encode())
                        continue
                    except Exception as a:
                            print("Error: ",a)
                else:
                    print("File Not Selected")
            if add.lower() == "close":
                client_socket.send("Closed Server".encode())
                break
    except Exception as e:
        print("error While handling client", e)
    finally:
        client_socket.close()
        print("Closed for: ", addr[0], " ", addr[1])

#creating Server
def My_server():    
    global mac 
    server_ip = "127.0.0.1" #127.0.0.1
    port = 2202
    
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((server_ip,port))
        server.listen()
        print("Server connection started: ",server_ip,",",port)
        while True:
            client_socket,addr = server.accept()
            #getting ip address from client 
            mac = client_socket.recv(1024 * 1024 * 1024).decode()
            print("Connected Client MAC: ",mac)
            #creating log file for all clients
            date = datetime.datetime.now()
            client_log_read = open("D:/VOID MAIN()/Python-project/MultiServer-Client/ServerFiles/LOG/LOG.txt","r+")
            client_log = open("D:/VOID MAIN()/Python-project/MultiServer-Client/ServerFiles/LOG/LOG.txt","a")
            client_log.write("Client Connected MAC Address: "+mac+" Date And Time: "+str(datetime.datetime.now())+"\n")
            lines =client_log_read.readlines(0)
            print(lines)
            count = 1
            
            for line in lines:
                if mac in line:
                    print("found: ",mac)
                    count+=1
                    print("Founded ",count," Times")
                else:
                    print("Not Found")
            client_log_read.close()
            client_log.close()
            client_socket.send(str(count).encode())
            client_info.insert(tk.END,"\nConnected Client MAC: "+mac)
            client_info.pack()
            #create an folder for client
            mac = mac.replace(":","")
            try:
             os.mkdir("D:/void main()/Python-project/MultiServer-Client/ServerFiles/"+mac)
            except:
                pass
            #connection process
            print("Accepted connection request from: ",addr[0],",",addr[1])
            # start a new thread to handle the client
            thread = threading.Thread(target=handle, args=(client_socket, addr,))
            thread.start()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.close()
#start and stop server
def toggle_server():
    global server_running
    if not server_running:
        # Start the server in a new thread
        server_thread = threading.Thread(target=My_server)
        server_thread.daemon = True  # Daemonize the thread so it automatically dies when the main thread exits
        server_thread.start()
        status_label.config(text="Server is running")
        toggle_button.config(text="Stop Server")
        server_running = True
    else:
        # Stop the server
        server_running = False
        status_label.config(text="Server is not running")
        toggle_button.config(text="Start Server")
        exit()
#GUI
root = tk.Tk()
root.title("Server Side")
root.geometry("400x300")
status_label = tk.Label(root, text="Server is not running")
status_label.pack(pady=10)
toggle_button = tk.Button(root, text="Start Server", command=toggle_server)
toggle_button.pack(pady=5)
client_info = tk.Text(root,height=100,width=200)
client_info.pack()
root.mainloop()