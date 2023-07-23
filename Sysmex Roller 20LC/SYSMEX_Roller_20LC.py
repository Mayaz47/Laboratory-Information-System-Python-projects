try:
    import socket
    import tkinter as tk
    from tkinter import ttk
    from tkinter import scrolledtext
    import threading
    import os
    import datetime
    import requests
    import sys
    import serial
    import serial.tools.list_ports
    import time
    
    port = 'com1'
    baud_rate = 9600
    print('Port:', port)
    print('BaudRate:', baud_rate)
    url = ''
    
        # Use the values in your code as necessary
    root = tk.Tk()
    root.title('Serial Com Machine')
    
    # Set current time, create a folderpath containing a data file and a temp file to store data. The folderpath is named according to current date.
    current_date = datetime.datetime.now().strftime("%d.%m.%Y")
    folder_path = os.path.join(os.getcwd(), current_date)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_path = os.path.join(folder_path, "data.txt")
    tempFile = os.path.join(folder_path, "temp.txt")
    def read_data():
        global z1serial, barcode_text, esr_text
        size = z1serial.inWaiting()
        if size:
            data = z1serial.read(size)
            decoded_str = data.decode('ascii') #Decoding byte data to ascii
            digits_only = ''.join(filter(str.isdigit, decoded_str)) #Taking the digits from the string
            
            # Stripping the ESR and MRI
            last_10_digits = digits_only[-10:]
            rest_of_string = digits_only[:-10]
            
            # Barcode can be achieved by removing initial '01'
            barcode = rest_of_string.lstrip('01') 
            
            # ESR result can be achieved extracting last 3 digits
            esr = last_10_digits[-3:].lstrip('0')
            text_area.insert(tk.END, "BAR CODE: {}\n".format(barcode))
            text_area.insert(tk.END, "ESR: {}\n".format(esr))
            
            # Opening the txt file to store the data
            with open(file_path, "a") as f:
                f.write(barcode)
                f.write(esr)
            dat = {
                'mrno': barcode,
                'ParameterName': 'ESR',
                'Result': esr
                }
            response = requests.post(url, data=dat) # Posting ESR data to API
            if response.status_code == 200:
                print('Data posted successfully!')
            else:
                print('Failed to post data!')
        root.after(100, read_data)
    z1serial = serial.Serial(port=port, baudrate=baud_rate)
    print(z1serial)
    read_data()
    def start_server():
        host = '192.168.20.155'
        port = 5000
        
        
        #binding the socket to the host IP and listening to incoming transmission
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind((host, port))
            except OSError as e:
                print(e)
            try:
                s.listen(5)
            except OSError as e:
                print(e)
            print("Waiting for a connection...")
            conn, addr = s.accept()
            
            #Connected
            print(f"Connected by {addr}")
            
            #Recieving data
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                msg = data.decode("utf-8")
               
                
                # Reading and writing in temp and data file, Clearing out temp file in every read
                with open(file_path, "a") as f:
                    f.write(msg)
                with open(tempFile, "w") as t:
                    t.write(msg)
                with open(tempFile, 'r') as file:
                    # Loop through each line in the file
                    for line in file:
                         if line.startswith('O'): # if line Starts with O it contains patient info
                                 parts = line.strip().split('|')
                                 section= parts[3].strip().split('^')
                                 section2= section[2].replace(" ", "")
                                 print("Patient ID:", section2)
                                 text_area.insert(tk.END,"Patient ID:"+ section2 +'\n')
                                 MRI = section2 # Set the MRI
                         if line.startswith('R'): # If line starts with R it contains test results
                                 parts = line.strip().split('|')
                                 if parts[2] == '^^^^HGB^1': # Checking parameter name
                                     print("Hymoglobin:  ", parts[3]) # Displaying result
                                     text_area.insert(tk.END,"Hymoglobin:  "+ parts[3]+'\n')
                                     data = {
                                         'mrno': MRI,
                                         'ParameterName': 'HGB',
                                         'Result': parts[3]
                                         }
    
                                     response = requests.post(url, data=data) # Sending test results corresponding to the MRI previously extracted over on API
    
                                     if response.status_code == 200:
                                         print('Data posted successfully!')
                                     else:
                                         print('Failed to post data!')
                                 if parts[2] == '^^^^WBC^1':
                                     print("WBC:  ", parts[3])
                                     text_area.insert(tk.END,"WBC:  "+ parts[3]+'\n')
                                     data = {
                                         'mrno': MRI,
                                         'ParameterName': 'WBC',
                                         'Result': parts[3]
                                         }
    
                                     response = requests.post(url, data=data)
    
                                     if response.status_code == 200:
                                         print('Data posted successfully!')
                                     else:
                                         print('Failed to post data!')
                                 if parts[2] == '^^^^NEUT%^1':
                                     print("Neutrophils:  ", parts[3])
                                     text_area.insert(tk.END,"Neutrophils:  "+ parts[3]+'\n')
                                     data = {
                                         'mrno': MRI,
                                         'ParameterName': 'Neu%',
                                         'Result': parts[3]
                                         }
    
                                     response = requests.post(url, data=data)
    
                                     if response.status_code == 200:
                                         print('Data posted successfully!')
                                     else:
                                         print('Failed to post data!')
                                 if parts[2] == '^^^^LYMPH%^1':
                                     print("Lymphocytes:  ", parts[3])
                                     text_area.insert(tk.END,"Lymphocytes:  "+ parts[3]+'\n')
                                     data = {
                                         'mrno': MRI,
                                         'ParameterName': 'Lym%',
                                         'Result': parts[3]
                                         }
    
                                     response = requests.post(url, data=data)
    
                                     if response.status_code == 200:
                                         print('Data posted successfully!')
                                     else:
                                         print('Failed to post data!')
                                 if parts[2] == '^^^^MONO%^1':
                                     print("Monocytes:  ", parts[3])
                                     text_area.insert(tk.END,"Monocytes:  "+ parts[3]+'\n')
                                     data = {
                                         'mrno': MRI,
                                         'ParameterName': 'Mon%',
                                         'Result': parts[3]
                                         }
    
                                     response = requests.post(url, data=data)
    
                                     if response.status_code == 200:
                                         print('Data posted successfully!')
                                     else:
                                         print('Failed to post data!')
                                 if parts[2] == '^^^^EO%^1':
                                     print("Eosinophils:  ", parts[3])
                                     text_area.insert(tk.END,"Eosinophils:  "+ parts[3]+'\n')
                                     data = {
                                         'mrno': MRI,
                                         'ParameterName': 'Eos%',
                                         'Result': parts[3]
                                         }
    
                                     response = requests.post(url, data=data)
    
                                     if response.status_code == 200:
                                         print('Data posted successfully!')
                                     else:
                                         print('Failed to post data!')
                                 if parts[2] == '^^^^BASO%^1':
                                     print("Basophil:  ", parts[3])
                                     text_area.insert(tk.END,"Basophil:  "+ parts[3]+'\n')
                                     data = {
                                         'mrno': MRI,
                                         'ParameterName': 'Bas%',
                                         'Result': parts[3]
                                         }
    
                                     response = requests.post(url, data=data)
    
                                     if response.status_code == 200:
                                         print('Data posted successfully!')
                                     else:
                                         print('Failed to post data!')
                                 if parts[2] == '^^^^RBC^1':
                                     print("RBC:  ", parts[3])
                                     text_area.insert(tk.END,"RBC:  "+ parts[3]+'\n')
                                     data = {
                                         'mrno': MRI,
                                         'ParameterName': 'RBC',
                                         'Result': parts[3]
                                         }
    
                                     response = requests.post(url, data=data)
    
                                     if response.status_code == 200:
                                         print('Data posted successfully!')
                                     else:
                                         print('Failed to post data!')
                                 if parts[2] == '^^^^HCT^1':
                                     print("MCV:  ", parts[3])
                                     text_area.insert(tk.END,"PCV:  "+ parts[3]+'\n')
                                     data = {
                                         'mrno': MRI,
                                         'ParameterName': 'HCT',
                                         'Result': parts[3]
                                         }
    
                                     response = requests.post(url, data=data)
    
                                     if response.status_code == 200:
                                         print('Data posted successfully!')
                                     else:
                                         print('Failed to post data!')
                                 if parts[2] == '^^^^MCV^1':
                                     print("MCV:  ", parts[3])
                                     text_area.insert(tk.END,"MCV:  "+ parts[3]+'\n')
                                     data = {
                                         'mrno': MRI,
                                         'ParameterName': 'MCV',
                                         'Result': parts[3]
                                         }
    
                                     response = requests.post(url, data=data)
    
                                     if response.status_code == 200:
                                         print('Data posted successfully!')
                                     else:
                                         print('Failed to post data!')
                                 if parts[2] == '^^^^MCH^1':
                                     print("MCH:  ", parts[3])
                                     text_area.insert(tk.END,"MCH:  "+ parts[3]+'\n')
                                     data = {
                                         'mrno': MRI,
                                         'ParameterName': 'MCH',
                                         'Result': parts[3]
                                         }
    
                                     response = requests.post(url, data=data)
    
                                     if response.status_code == 200:
                                         print('Data posted successfully!')
                                     else:
                                         print('Failed to post data!')
                                 if parts[2] == '^^^^MCHC^1':
                                     print("MCHC:  ", parts[3])
                                     text_area.insert(tk.END,"MCHC:  "+ parts[3]+'\n')
                                     data = {
                                         'mrno': MRI,
                                         'ParameterName': 'MCHC',
                                         'Result': parts[3]
                                         }
    
                                     response = requests.post(url, data=data)
    
                                     if response.status_code == 200:
                                         print('Data posted successfully!')
                                     else:
                                         print('Failed to post data!')
                                 if parts[2] == '^^^^RDW-CV^1':
                                     print("RDW-CV:  ", parts[3])
                                     text_area.insert(tk.END,"RDW-CV:  "+ parts[3]+'\n')
                                     data = {
                                         'mrno': MRI,
                                         'ParameterName': 'RDW-CV',
                                         'Result': parts[3]
                                         }
    
                                     response = requests.post(url, data=data)
    
                                     if response.status_code == 200:
                                         print('Data posted successfully!')
                                     else:
                                         print('Failed to post data!')
                                 if parts[2] == '^^^^RDW-SD^1':
                                     print("RDW-SD:  ", parts[3])
                                     text_area.insert(tk.END,"RDW-SD:  "+ parts[3]+'\n')
                                     data = {
                                         'mrno': MRI,
                                         'ParameterName': 'RDW-SD',
                                         'Result': parts[3]
                                         }
    
                                     response = requests.post(url, data=data)
    
                                     if response.status_code == 200:
                                         print('Data posted successfully!')
                                     else:
                                         print('Failed to post data!')
                                 if parts[2] == '^^^^PLT^1':
                                     print("Platelets:  ", parts[3])
                                     text_area.insert(tk.END,"Platelets:  "+ parts[3]+'\n')
                                     data = {
                                         'mrno': MRI,
                                         'ParameterName': 'PLT',
                                         'Result': parts[3]
                                         }
    
                                     response = requests.post(url, data=data)
    
                                     if response.status_code == 200:
                                         print('Data posted successfully!')
                                     else:
                                         print('Failed to post data!')
                                 if parts[2] == '^^^^MPV^1':
                                     print("MPV:  ", parts[3])
                                     text_area.insert(tk.END,"MPV:  "+ parts[3]+'\n')
                                     data = {
                                         'mrno': MRI,
                                         'ParameterName': 'MPV',
                                         'Result': parts[3]
                                         }
    
                                     response = requests.post(url, data=data)
    
                                     if response.status_code == 200:
                                         print('Data posted successfully!')
                                     else:
                                         print('Failed to post data!')
                                 if parts[2] == '^^^^PDW^1':
                                     print("PDW-SD:  ", parts[3])
                                     text_area.insert(tk.END,"PDW-SD:  "+ parts[3]+'\n')
                                     data = {
                                         'mrno': MRI,
                                         'ParameterName': 'PDW',
                                         'Result': parts[3]
                                         }
    
                                     response = requests.post(url, data=data)
    
                                     if response.status_code == 200:
                                         print('Data posted successfully!')
                                     else:
                                         print('Failed to post data!')   
                                    
                
                
                
    def exit_program():
        root.destroy()
        sys.exit('Exit')
    def clear():
        text_area.delete("1.0", tk.END)
    
    
    
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
