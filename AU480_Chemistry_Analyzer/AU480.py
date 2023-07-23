

import serial 
import time
import requests
import re
import json
import tkinter as tk
import threading
import sys
from tkinter import ttk
from tkinter import scrolledtext
import os
import datetime
    
try:
    current_date = datetime.datetime.now().strftime("%d.%m.%Y")
    folder_path = os.path.join(os.getcwd(), current_date)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_path = os.path.join(folder_path, "data.txt")
    def start_server():
        #query variable initialized. It is used to identify if a message is query message

        
        #baudrate and port name initialized and serial port created
        baudrate1 = 9600
        port1 = 'com3'
        z1serial = serial.Serial(port=port1, baudrate=baudrate1)
        print(z1serial)
        text_area.insert(tk.END,"Connected"+'\n')
        
        # API to post data
        url = 'https://erp.thelabquest.com/api/parametersaved'
        while True:
                size = z1serial.inWaiting() #Calculate size of incoming data
                if size:
                   data = z1serial.read(size) #read data from serial com
                   text_area.insert(tk.END,"data:"+str(data)+'\n')
                   decoded_data = data.decode('ascii')
                
                   
                   # The first element of the element list indicates the type of message, i.e 'H' = Header message, 'Q' = Query message, 'O' = Test message
                   # Query message identified
                   if len(decoded_data) == 1:
                       print('Ack recieved')
                   elif decoded_data[1] == 'R':
                        text_area.insert(tk.END,"ACK sent: "+str(z1serial.write(b'\x06'))+'\n')
                        value = data.decode('utf-8')
                        value2 = value.split()
                        
                        try:
                            bar = value2[2] #Second element of element list is the barcode
                            #rack=value2[1]
                            print(bar[:-1])
                            url2 = "https://erp.thelabquest.com/api/parameter/"+bar[:-1]+"/2" 
                            response = requests.get(url2) #Getting test information from the API corresponding to the bar code
            
                            if response.status_code == 200: # Success status
                                
                                #Converting and loading the Json acquired from the API
                                json_string = response.content.decode('utf-8').strip(' \t\n\r')
                                json_object = json.loads(json_string) 
                                
                                #Finding test names and displaying
                                name = json_object.split('[')[0].replace('[','')
                                matches = re.findall(r'"InterfaceParameterCode":"([^"]+)"', json_object)
                                text_area.insert(tk.END,"Sending tests:"+str(matches)+'\n')
                                message_str = value.replace('R', 'S')
                                message_str = message_str.replace('\x03', '')
     
                                message = message_str+'    E000000'+name
                                for i in range(20 - len(name)):
                                    message = message + ' '
                                    
                                for i in range(len(matches)):
                                     message=message+matches[i]
                                message =message + '\x03'
                                print(message)
                                message2 = message.encode()
                                print(message2)
                                text_area.insert(tk.END,message)
                                text_area.insert(tk.END,"Message sent"+str(z1serial.write(message2))+'\n')
                                
                        except Exception as e:
                            print("RB")
                            text_area.insert(tk.END,"ACK sent: "+str(z1serial.write(b'\x06'))+'\n')
                     
                    # Test message recieved
                   elif decoded_data[1] == 'D':
                        print (data)
                        text_area.insert(tk.END,"ACK sent: "+str(z1serial.write(b'\x06'))+'\n')
                        if len(decoded_data) > 3:
                            print(decoded_data)
                            value4 = str(decoded_data).split()
                            value5 = []
                            for item in value4:
                                if len(item) >= 11 and item.replace('r', '').replace('.','').isdigit():
                                    value5.append(item)

                            print(value5)
                            for i in range (len(value5)):
                                print(value5[i][7:].replace('r','').lstrip('0'))
                                dat = {
                                    'mrno': value4[2],
                                    'ParameterName': value5[i][:3],
                                    'Result': value5[i][7:].replace('r','').lstrip('0')
                                }
                                with open(file_path, "a") as f:
                                    f.write(f"MRN: {value4[2]}\n")
                                    f.write(f"Parameter: {value5[i][:3]}\n")
                                    f.write(f"Result: {value5[i][7:].replace('r','').lstrip('0')}\n")

                                response = requests.post(url, data=dat) #Posting the data on API
                                if response.status_code == 200:
                                    text_area.insert(tk.END,'Data posted successfully!'+'\n')
                                else:    
                                    text_area.insert(tk.END,'Failed to post data!'+'\n')
                    # While recieving send Ackknowledgement
                   
                else:
                   time.sleep(1)
                
                
    def exit_program():
        root.destroy()
        sys.exit('Exit')
    def clear():
        text_area.delete("1.0", tk.END)
    root = tk.Tk()
    root.title('AU480 interface')
    
    
    # Adding a scrolled text widget
    text_area = scrolledtext.ScrolledText(root, width=50, height=30)
    text_area.grid(column=0, row=0, padx=10, pady=10)
    
    # Adding exit button
    style = ttk.Style()
    style.configure("Custom.TButton", foreground="red", background="white")
    exit_button = ttk.Button(root, text="Exit", command=exit_program,style="Custom.TButton")
    exit_button.grid(column=0, row=2, padx=10, pady=10)
    
    clear_button = ttk.Button(root, text="Clear", command=clear)
    clear_button.grid(column=0, row=1, padx=10, pady=10)
    
    # Starting the server in a separate thread
    t = threading.Thread(target=start_server)
    t.start()
    
    root.mainloop()
except Exception as e:
    while True:
        print(e)
        time.sleep(5)