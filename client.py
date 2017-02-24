# pylint: disable-all

from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
import tkinter.font as tkfont
import socket
import threading
import os


class Reader:

    def start_client_socket(self):
        self.connected = True
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
        try:
            self.s.connect(('localhost', 9999))
            self.s.send(b'1')
        except ConnectionRefusedError as e:
            print(e)
        
        # while self.connected:
        #     data = self.s.recv(1024)
        #     print(data)
        #
        # print('Successfully get the file')

    def close_client_socket(self):
        if not self.connected:
            self.s.close()
            print('client connection closed func')

    def btn_on_click(self):
        print("BTN ON")
        self.btn_on.configure(state='disabled', bg='grey')
        self.btn_off.config(state='normal', bg='red')
        t = threading.Thread(target=self.start_client_socket)
        t.start()

    def btn_off_click(self):
        print("BTN OFF")
        self.btn_on.config(state='normal', bg='green')
        self.btn_off.config(state='disabled', bg='grey')
        self.connected = False
        self.close_client_socket()

    def load_file(self):
        fname = askopenfilename(filetypes=(("CSV Files", "*.csv"), ("PDF Files", "*.pdf"), ("TEXT files", "*.txt"), ("All files", "*.*")))
        if fname:
            try:
                print(fname)
                fname_split = fname.split('/')
                print(fname_split)
                self.treeview.insert('', 'end', text=fname_split[-1], values=(fname, os.path.getsize(fname)))
            except:  # <- naked except is a bad idea
                showerror("Open Source File", "Failed to read file\n'%s'" % fname)
            return

    def select_item(self):
        cur_item = self.tree.focus()
        print(self.tree.item(cur_item))
        print(self.tree.item(cur_item).get('values')[0])
        # s.send(b'item enviado')
        file = open(self.tree.item(cur_item).get('values')[0], 'rb')
        self.send_file(file)

    def send_file(self, file):
        self.s.send(b'2')
        l = file.read(1024)
        while l:
            print('Sending...')
            self.s.send(l)
            l = file.read(1024)
        file.close()
        print('Done Sending')
        self.s.close()
        return

    def __init__(self, root):
        self.root = root
        self.s = ''
        self.connected = False

        root.title("Projeto de Redes I")
        #root.geometry("800x500")
        root.resizable(width=False, height=False)
        self.customFont = tkfont.Font(family="Helvetica", size=10)

        self.lbf_one = LabelFrame(root)
        self.lbf_one.grid(row=0, columnspan=7, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)

        self.lb_app = Label(self.lbf_one, text='Client: ', font=self.customFont)
        self.lb_app.grid(row=0, column=0, sticky=W)

        self.btn_on = Button(self.lbf_one, text="ON", fg='white', bg='green', state='normal',
                             command=self.btn_on_click, font=self.customFont)
        self.btn_on.grid(row=0,  column=1, sticky=W, padx=0)

        self.btn_off = Button(self.lbf_one, text="OFF", fg='white', bg='grey', state='disabled',
                              command=self.btn_off_click, font=self.customFont)
        self.btn_off.grid(row=0, column=2, sticky=W, padx=0)

        self.lb_status = Label(self.lbf_one, text='Status', font=self.customFont)
        self.lb_status.grid(row=1, column=0, sticky=W)

        self.lbf_two = LabelFrame(root, width=500, height=200)
        self.lbf_two.grid(row=1, columnspan=7, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)

        # self.text = Text(self.lbf_two)
        # self.text.grid(row=0, column=0)

        # Set the treeview
        self.tree = ttk.Treeview(self.lbf_two, columns=('Files', 'Path'))
        self.tree.heading('#0', text='Files')
        self.tree.column('#0', width=200, stretch=YES)
        self.tree.heading('#1', text='Path')
        self.tree.column('#1', width=300, stretch=YES)
        self.tree.heading('#2', text='Size (bytes)')
        self.tree.column('#2', width=100, stretch=YES)
        self.tree.grid(row=4, columnspan=4, sticky='nsew')
        self.treeview = self.tree
        # Initialize the counter
        self.i = 0

        self.btn_browser = Button(self.lbf_two, text="Browse", command=self.load_file, width=10)
        self.btn_browser.grid(row=0,  column=0, sticky=W, padx=0)

        self.btn_sendfile = Button(self.lbf_two, text="Send", command=self.select_item, width=10)
        self.btn_sendfile.grid(row=0, column=1, sticky=W, padx=0)

root = Tk()
root.columnconfigure(0, weight=0)
root.config(background='#007BA7')
reader = Reader(root)
root.mainloop()
