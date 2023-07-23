#!/usr/bin/env python
# coding: utf-8

# In[10]:


import tkinter as tk
import serial

z1serial = serial.Serial(port='com4', baudrate=9600)

class SerialGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Serial Communication")
        self.master.geometry("400x300")
        
        
        
        # Create the GUI elements
        self.label1 = tk.Label(self.master, text="Enter command:")
        self.label1.pack()
        self.entry1 = tk.Entry(self.master, width=40)
        self.entry1.pack()
        self.send_button = tk.Button(self.master, text="Send", command=self.send_command)
        self.send_button.pack()
        self.disconnect_button = tk.Button(self.master, text="Disconnect", command=self.disconnect)
        self.disconnect_button.pack()
        self.textbox = tk.Text(self.master)
        self.textbox.pack(fill="both", expand=True)
        
        # Start the serial communication loop
        self.master.after(100, self.receive_data)
    
    def send_command(self):
        command = self.entry1.get()
        print("Command sent: ",z1serial.write(bytes(command.replace('<STX>', '\x02').replace('<CR>', '\r').replace('<LF>', '\n').replace('<ETX>','\x03').replace('<ENQ>','\x05').replace('<EOT>','\x04').replace('<ACK>','\x06'), 'utf-8')))
    
    def receive_data(self):
        # Check if there is data available to read from the serial port
        if z1serial.in_waiting > 0:
            data = z1serial.read(z1serial.in_waiting)
            self.textbox.insert("end", data.decode())
            print(data)
        
        # Schedule the next data reception
        self.master.after(100, self.receive_data)
    
    def connect(self):
        # Create the serial port object
        
        print(z1serial)
    
    def disconnect(self):
        z1serial.close()

# Create the root window and start the program
root = tk.Tk()
app = SerialGUI(root)
root.mainloop()


# In[11]:


z1serial.close()


# In[ ]:




