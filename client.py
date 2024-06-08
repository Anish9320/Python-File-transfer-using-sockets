import socket
import os
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as message
from tkinter import simpledialog as sd
import time
try:
    from getmac import getmac
except:
    import subprocess 
    import sys
    subprocess.check_call([sys.executable,"-m","pip","install","getmac"]) 
    from getmac import getmac

MAX_CHUNK_SIZE = 1024 * 1024 * 1024
def default():
    print("Error")
def select_file():
    #to send the files to the Server 
    filetypes = (('Text files', '*.txt'),('All files', '*.*'))
    filename = fd.askopenfilename(title='Open a file',initialdir='/',filetypes=filetypes)
    if filename == '':
        print("Please select a file.")
    else:
        client_socket.send(b"MAC"+address.encode()[:MAX_CHUNK_SIZE])
        file_name = os.path.basename(filename)
        client_socket.send(file_name.encode()[:1024 * 1024 * 1024])
        time.sleep(1)
        with open(filename,"r") as file:
            data = file.read()
        client_socket.send(data.encode()[:1024 * 1024 * 1024])

def get_files():
    file_status = "0"    #false hai ye
    #this function will work to get the files from the server
    client_socket.send(b"get"+address.encode()[:1024 * 1024 * 1024])
    files = client_socket.recv(MAX_CHUNK_SIZE).decode()
    files_lable.config(text="Files Name: "+files)
    files_lable.pack()
    fileName = sd.askstring("Input", "Enter File Name Here: ", parent=root)
    if fileName == None:
        print("Please give file name")
        default()
        files_lable.config(text="")
        client_socket.send(file_status.encode()[:MAX_CHUNK_SIZE])   #send status (false)
    else:
        file_status = "1"
        client_socket.send(file_status.encode()[:MAX_CHUNK_SIZE])   #send status (true)
        time.sleep(1)
        client_socket.send(fileName.encode()[:MAX_CHUNK_SIZE])
        rev_name = client_socket.recv(MAX_CHUNK_SIZE).decode()
        print("fileName", rev_name)
        index = rev_name.find(".")
        file_content = client_socket.recv(MAX_CHUNK_SIZE).decode()
        print("Data", file_content)
        save_file = fd.asksaveasfilename(initialfile=rev_name[:index], defaultextension=rev_name[index:], initialdir="/")
        if save_file:
            with open(save_file,"w") as file:
                file.write(file_content)
def exit_program():
    #to close the connection with server
    global server_ip, server_port, address ,client_socket
    client_socket.send("close".encode()[:1024 * 1024 * 1024])
    client_socket.close()
    root.quit()
    exit(0)

def connect_to_server():
    global server_ip, server_port, address ,client_socket
    server_ip = ip_entry.get()
    server_port = int(port_entry.get())
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip,server_port))
    select_button.config(state="active")
    get_button.config(state="active")
    address = getmac.get_mac_address()
    client_socket.send(address.encode()[:1024 * 1024 * 1024])
    count =client_socket.recv(MAX_CHUNK_SIZE).decode()
    if count == "1":
        message.askokcancel("Welcome!!!","Welcome Back You Are Visiting The Server For "+count+"st Time")
    elif count == "2":
        message.askokcancel("Welcome!!!","Welcome Back You Are Visiting The Server For "+count+"nd Time")
    elif count == "3":
        message.askokcancel("Welcome!!!","Welcome Back You Are Visiting The Server For "+count+"rd Time")
    else:
        message.askokcancel("Welcome!!!","Welcome Back You Are Visiting The Server For "+count+"th Time")
        
        

#gui for client side
root = tk.Tk()
root.title("Client GUI")
root.geometry("600x300")  

# input fields
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

ip_label = tk.Label(input_frame, text="Server IP:")
ip_label.grid(row=0, column=0, padx=5, pady=5)

ip_entry = tk.Entry(input_frame)
ip_entry.grid(row=0, column=1, padx=5, pady=5)

port_label = tk.Label(input_frame, text="Server Port:")
port_label.grid(row=1, column=0, padx=5, pady=5)

port_entry = tk.Entry(input_frame)
port_entry.grid(row=1, column=1, padx=5, pady=5)

# Button frame
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

connect_button = tk.Button(button_frame, text="Connect to Server", command=connect_to_server)
connect_button.grid(row=0, column=0, padx=5, pady=5)

select_button = tk.Button(button_frame, text="Select File", command=select_file, state="disabled")
select_button.grid(row=0, column=1, padx=5, pady=5)

get_button = tk.Button(button_frame, text="Get Files", command=get_files, state="disabled")
get_button.grid(row=0, column=2, padx=5, pady=5)

exit_button = tk.Button(button_frame, text="Exit", command=exit_program)
exit_button.grid(row=0, column=3, padx=5, pady=5)

# Files label
files_lable = tk.Label(root)
files_lable.pack(pady=10)

root.mainloop()