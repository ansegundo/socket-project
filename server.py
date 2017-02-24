    # pylint: disable-all

from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showerror
from tkinter.messagebox import showinfo
import tkinter.font as tkfont
import socket
import threading
import os
import glob
import re


class Reader:

    def start_server_socket(self):
        self.connected = True                                       # Connection verifier          
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Estabilish a TCP/IP socket
        self.s.bind(('localhost', 9999))                            # Bind to the port
        self.s.listen(10)                                           # Now wait for client connection.
        print('server listening....')

        try:
            conn, address = self.s.accept()                         # Establish connection with client.
            print(address)
            print('cliente se conectou')
        except:
            print('nao foi possível se comunicar com o cliente')

        try:
            data = conn.recv(1024)
            print(bytes.decode(data))
            if bytes.decode(data) == '1':
                self.lb_status = Label(self.lbf_one, text='Cliente Conectado', font=self.customFont)
                self.lb_status.grid(row=1, column=1, columnspan=2, sticky=W)
                print('command handler')
                self.command_handler(conn)
        except:
            print('disconnected')
            self.connected = False

    def close_server_socket(self):
        if not self.connected:
            self.s.close()
            print('connection closed function')

    def command_handler(self, conn):
        try:
            data = conn.recv(1024)
            data = bytes.decode(data)
            print(data)
        except: 
            print('no data to read')
        if data == '2':
            self.get_files(conn)
        if data == '3':
            self.get_csv(conn)

    def get_csv(self, conn):
        nome = conn.recv(1024)
        print(nome.decode("utf-8"))
        nome = nome.decode("utf-8")
        with open (self.path + '/' +nome, 'wb') as csvfile:
            print('csv opened')
            while True:
                # print('receiving data...')
                self.text.insert(END, 'receiving data\n')
                data = conn.recv(1024)
                if not data:
                    break
                csvfile.write(data)
            csvfile.close()
            print('Successfully get the file')
            self.s.close()
            print('connection closed')
            self.update_files()
    
    def update_files(self):
        print('got here')
        for filename in glob.iglob(self.path+'/**/*.csv', recursive=True):
            print(filename)
            fname_split = filename.split('/')
            print(fname_split)
            self.treeview.insert('', 'end', text=fname_split[-1].split('\\')[-1], values=(filename, os.path.getsize
            (filename)))
        return    

    def get_files(self, conn):
        nome = conn.recv(1024)
        print(nome)
        with open('received_file.txt', 'wb') as file:
            print('txt opened')
            while True:

                print('receiving data...')
                data = conn.recv(1024)
                # print('data=%s', (data))
                if not data:
                    break
                # write data to a file
                file.write(data)
        file.close()
        self.update_files()
        print('Successfully get the file')
        self.s.close()
        print('connection closed')
       
    def btn_on_click(self):
        print("\tbutton ON pressed")
        self.btn_on.configure(state='disabled', bg='grey')
        self.btn_off.config(state='normal', bg='red')
        t = threading.Thread(target=self.start_server_socket)
        t.start()

    def btn_off_click(self):
        print("\tbutton OFF pressed")
        self.btn_on.config(state='normal', bg='green')
        self.btn_off.config(state='disabled', bg='grey')
        self.connected = False
        self.close_server_socket()

    def preview_files(self):
        self.text.delete('1.0', END)
        print('hello')
    
    def select_directory(self):
        self.path = askdirectory()
        print(self.path)

    def __init__(self, root):
        self.root = root
        self.s = ''
        self.connected = False
        self.path = 'C:/'

        root.title("Projeto de Redes I")
        # root.geometry("800x500")
        root.resizable(width=False, height=False)

        self.customFont = tkfont.Font(family="Helvetica", size=10)


        self.lbf_one = LabelFrame(root)
        self.lbf_one.grid(row=0, columnspan=7, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)
        self.lbf_one.grid_columnconfigure(2, weight=1)
        self.lbf_one.grid_rowconfigure(1, weight=1)

        self.lb_app = Label(self.lbf_one, text='Servidor: ', font=self.customFont)
        self.lb_app.grid(row=0, column=0, sticky=W)

        self.btn_on = Button(self.lbf_one, text="ON", width=4, fg='white', bg='green', state='normal',
                             command=self.btn_on_click, font=self.customFont)
        self.btn_on.grid(row=0,  column=1, sticky=W, padx=0)

        self.btn_off = Button(self.lbf_one, text="OFF", width=4, fg='white', bg='grey', state='disabled',
                              command=self.btn_off_click, font=self.customFont)
        self.btn_off.grid(row=0, column=2, sticky=W, padx=0)

        self.lb_status = Label(self.lbf_one, text='Estado: ', font=self.customFont)
        self.lb_status.grid(row=1, column=0, sticky=W)

        self.lbf_two = LabelFrame(root, text="Arquivos Recebidos", width=500, height=150)
        self.lbf_two.grid(row=2, columnspan=4, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)
        self.lbf_two.grid_columnconfigure(2, weight=1)
        self.lbf_two.grid_rowconfigure(0, weight=1)
        self.lbf_two.grid_propagate(False)

        self.btn_refresh = Button(self.lbf_two, text="Preview", fg='white', bg='grey', command=self.preview_files, font=self.customFont)
        self.btn_refresh.grid(row=1, column=0)
        self.btn_directory = Button(self.lbf_two, text="Diretório", fg='white', bg='grey', command=self.select_directory, font=self.customFont)
        self.btn_directory.grid(row=1, column=1)

        # Set the treeview
        self.tree = ttk.Treeview(self.lbf_two, columns=('Files', 'Path'))
        self.tree.heading('#0', text='Files')
        self.tree.column('#0', width=100, stretch=YES)
        self.tree.heading('#1', text='Path')
        self.tree.column('#1', width=200, stretch=YES)
        self.tree.heading('#2', text='Size (bytes)')
        self.tree.column('#2', width=50, stretch=YES)
        self.tree.grid(row=0, columnspan=4, sticky='WE')
        self.treeview = self.tree
        # Initialize the counter
        self.i = 0

        self.lbf_three = LabelFrame(root, text="Preview Tab", width=500, height=200)
        self.lbf_three.grid(row=1, columnspan=4, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)
        self.lbf_three.grid_columnconfigure(0, weight=1)
        self.lbf_three.grid_rowconfigure(0, weight=1)
        self.lbf_three.grid_propagate(False)

        self.text = Text(self.lbf_three)
        self.text.grid(row=0, column=0)

        showinfo('AVISO','O endereço de armazenamento padrão é C:\ \nPara mudar, clique em Diretório')
        

root = Tk()
root.columnconfigure(0, weight=0)
root.config(background='#007BA7')
reader = Reader(root)
root.mainloop()

