import socket
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import threading
import os
import datetime
import requests
import sys
import win32gui
import win32con


current_date = datetime.datetime.now().strftime("%d.%m.%Y")
folder_path = os.path.join(os.getcwd(), current_date)
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
file_path = os.path.join(folder_path, "data.txt")
tempFile = os.path.join(folder_path, "temp.txt")

def start_server():
    host = '192.168.20.155'
    port = 5000
    url = ''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(5)
        print("Waiting for a connection...")
        conn, addr = s.accept()
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            msg = data.decode("utf-8")
           
            
            
            with open(file_path, "a") as f:
                f.write(msg)
            with open(tempFile, "w") as t:
                t.write(msg)
            with open(tempFile, 'r') as file:
                # Loop through each line in the file
                for line in file:
                     if line.startswith('OBR'):
                             parts = line.strip().split('|')
                             print("Patient ID:", parts[3])
                             text_area.insert(tk.END,"Patient ID:"+ parts[3]+'\n')
                             MRI = parts[3]
                     if line.startswith('OBX'):
                             parts = line.strip().split('|')
                             if parts[3] == '718-7^HGB^LN':
                                 print("Hymoglobin:  ", parts[5])
                                 text_area.insert(tk.END,"Hymoglobin:  "+ parts[5]+'\n')
                                 data = {
                                     'mrno': MRI,
                                     'ParameterName': 'HGB',
                                     'Result': parts[5]
                                     }

                                 response = requests.post(url, data=data)

                                 if response.status_code == 200:
                                     print('Data posted successfully!')
                                 else:
                                     print('Failed to post data!')
                             if parts[3] == '6690-2^WBC^LN':
                                 print("WBC:  ", parts[5])
                                 text_area.insert(tk.END,"WBC:  "+ parts[5]+'\n')
                                 data = {
                                     'mrno': MRI,
                                     'ParameterName': 'WBC',
                                     'Result': parts[5]
                                     }

                                 response = requests.post(url, data=data)

                                 if response.status_code == 200:
                                     print('Data posted successfully!')
                                 else:
                                     print('Failed to post data!')
                             if parts[3] == '770-8^NEU%^LN':
                                 print("Neutrophils:  ", parts[5])
                                 text_area.insert(tk.END,"Neutrophils:  "+ parts[5]+'\n')
                                 data = {
                                     'mrno': MRI,
                                     'ParameterName': 'Neu%',
                                     'Result': parts[5]
                                     }

                                 response = requests.post(url, data=data)

                                 if response.status_code == 200:
                                     print('Data posted successfully!')
                                 else:
                                     print('Failed to post data!')
                             if parts[3] == '736-9^LYM%^LN':
                                 print("Lymphocytes:  ", parts[5])
                                 text_area.insert(tk.END,"Lymphocytes:  "+ parts[5]+'\n')
                                 data = {
                                     'mrno': MRI,
                                     'ParameterName': 'Lym%',
                                     'Result': parts[5]
                                     }

                                 response = requests.post(url, data=data)

                                 if response.status_code == 200:
                                     print('Data posted successfully!')
                                 else:
                                     print('Failed to post data!')
                             if parts[3] == '5905-5^MON%^LN':
                                 print("Monocytes:  ", parts[5])
                                 text_area.insert(tk.END,"Monocytes:  "+ parts[5]+'\n')
                                 data = {
                                     'mrno': MRI,
                                     'ParameterName': 'Mon%',
                                     'Result': parts[5]
                                     }

                                 response = requests.post(url, data=data)

                                 if response.status_code == 200:
                                     print('Data posted successfully!')
                                 else:
                                     print('Failed to post data!')
                             if parts[3] == '713-8^EOS%^LN':
                                 print("Eosinophils:  ", parts[5])
                                 text_area.insert(tk.END,"Eosinophils:  "+ parts[5]+'\n')
                                 data = {
                                     'mrno': MRI,
                                     'ParameterName': 'Eos%',
                                     'Result': parts[5]
                                     }

                                 response = requests.post(url, data=data)

                                 if response.status_code == 200:
                                     print('Data posted successfully!')
                                 else:
                                     print('Failed to post data!')
                             if parts[3] == '706-2^BAS%^LN':
                                 print("Basophil:  ", parts[5])
                                 text_area.insert(tk.END,"Basophil:  "+ parts[5]+'\n')
                                 data = {
                                     'mrno': MRI,
                                     'ParameterName': 'Bas%',
                                     'Result': parts[5]
                                     }

                                 response = requests.post(url, data=data)

                                 if response.status_code == 200:
                                     print('Data posted successfully!')
                                 else:
                                     print('Failed to post data!')
                             if parts[3] == '789-8^RBC^LN':
                                 print("RBC:  ", parts[5])
                                 text_area.insert(tk.END,"RBC:  "+ parts[5]+'\n')
                                 data = {
                                     'mrno': MRI,
                                     'ParameterName': 'RBC',
                                     'Result': parts[5]
                                     }

                                 response = requests.post(url, data=data)

                                 if response.status_code == 200:
                                     print('Data posted successfully!')
                                 else:
                                     print('Failed to post data!')
                             if parts[3] == '4544-3^HCT^LN':
                                 print("MCV:  ", parts[5])
                                 text_area.insert(tk.END,"PCV:  "+ parts[5]+'\n')
                                 data = {
                                     'mrno': MRI,
                                     'ParameterName': 'HCT',
                                     'Result': parts[5]
                                     }

                                 response = requests.post(url, data=data)

                                 if response.status_code == 200:
                                     print('Data posted successfully!')
                                 else:
                                     print('Failed to post data!')
                             if parts[3] == '787-2^MCV^LN':
                                 print("MCV:  ", parts[5])
                                 text_area.insert(tk.END,"MCV:  "+ parts[5]+'\n')
                                 data = {
                                     'mrno': MRI,
                                     'ParameterName': 'MCV',
                                     'Result': parts[5]
                                     }

                                 response = requests.post(url, data=data)

                                 if response.status_code == 200:
                                     print('Data posted successfully!')
                                 else:
                                     print('Failed to post data!')
                             if parts[3] == '785-6^MCH^LN':
                                 print("MCH:  ", parts[5])
                                 text_area.insert(tk.END,"MCH:  "+ parts[5]+'\n')
                                 data = {
                                     'mrno': MRI,
                                     'ParameterName': 'MCH',
                                     'Result': parts[5]
                                     }

                                 response = requests.post(url, data=data)

                                 if response.status_code == 200:
                                     print('Data posted successfully!')
                                 else:
                                     print('Failed to post data!')
                             if parts[3] == '786-4^MCHC^LN':
                                 print("MCHC:  ", parts[5])
                                 text_area.insert(tk.END,"MCHC:  "+ parts[5]+'\n')
                                 data = {
                                     'mrno': MRI,
                                     'ParameterName': 'MCHC',
                                     'Result': parts[5]
                                     }

                                 response = requests.post(url, data=data)

                                 if response.status_code == 200:
                                     print('Data posted successfully!')
                                 else:
                                     print('Failed to post data!')
                             if parts[3] == '788-0^RDW-CV^LN':
                                 print("RDW-CV:  ", parts[5])
                                 text_area.insert(tk.END,"RDW-CV:  "+ parts[5]+'\n')
                                 data = {
                                     'mrno': MRI,
                                     'ParameterName': 'RDW-CV',
                                     'Result': parts[5]
                                     }

                                 response = requests.post(url, data=data)

                                 if response.status_code == 200:
                                     print('Data posted successfully!')
                                 else:
                                     print('Failed to post data!')
                             if parts[3] == '21000-5^RDW-SD^LN':
                                 print("RDW-SD:  ", parts[5])
                                 text_area.insert(tk.END,"RDW-SD:  "+ parts[5]+'\n')
                                 data = {
                                     'mrno': MRI,
                                     'ParameterName': 'RDW-SD',
                                     'Result': parts[5]
                                     }

                                 response = requests.post(url, data=data)

                                 if response.status_code == 200:
                                     print('Data posted successfully!')
                                 else:
                                     print('Failed to post data!')
                             if parts[3] == '777-3^PLT^LN':
                                 print("Platelets:  ", parts[5])
                                 text_area.insert(tk.END,"Platelets:  "+ parts[5]+'\n')
                                 data = {
                                     'mrno': MRI,
                                     'ParameterName': 'PLT',
                                     'Result': parts[5]
                                     }

                                 response = requests.post(url, data=data)

                                 if response.status_code == 200:
                                     print('Data posted successfully!')
                                 else:
                                     print('Failed to post data!')
                             if parts[3] == '32623-1^MPV^LN':
                                 print("MPV:  ", parts[5])
                                 text_area.insert(tk.END,"MPV:  "+ parts[5]+'\n')
                                 data = {
                                     'mrno': MRI,
                                     'ParameterName': 'MPV',
                                     'Result': parts[5]
                                     }

                                 response = requests.post(url, data=data)

                                 if response.status_code == 200:
                                     print('Data posted successfully!')
                                 else:
                                     print('Failed to post data!')
                             if parts[3] == '32207-3^PDW^LN':
                                 print("PDW-SD:  ", parts[5])
                                 text_area.insert(tk.END,"PDW-SD:  "+ parts[5]+'\n')
                                 data = {
                                     'mrno': MRI,
                                     'ParameterName': 'PDW',
                                     'Result': parts[5]
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
root = tk.Tk()
root.title('Medonic M5')
icon_path = os.path.join(os.path.dirname(__file__), 'icon.ico')
root.iconbitmap(icon_path)


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
