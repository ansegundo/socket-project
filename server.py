from tkinter import *
import tkinter.font as tkFont
import socket
import threading
from threading import Thread
import queue
import time


def teste_server_socket():
    print('teste server socket')
    port = 60000  # Reserve a port for your service.
    s = socket.socket()  # Create a socket object
    host = socket.gethostname()  # Get local machine name
    s.bind((host, port))  # Bind to the port
    s.listen(5)  # Now wait for client connection.

    print(b'Server listening....')

    while True:
        conn, addr = s.accept()  # Establish connection with client.
        print(str(addr))
        data = conn.recv(1024)
        print(repr(data))

        filename = 'mytext.txt'
        f = open(filename, 'rb')
        l = f.read(1024)
        while (l):
            conn.send(l)
            print('Sent ', repr(l))
            l = f.read(1024)
        f.close()

        if print(b'Done sending'):
            return
        conn.send(b'Thank you for connecting')
        conn.close()


class Reader:
    status = False

    def btn_on_click(self):
        print("BTN ON")
        self.btn_on.configure(state='disabled', bg='grey')
        self.btn_off.config(state='normal', bg='red')
        self.status = True
        print(self.status)
        # teste_server_socket()
        self.queue = queue.Queue()
        ThreadedTask(self.queue).start()
        self.root.after(100, self.process_queue)

    def btn_off_click(self):
        print("BTN OFF")
        self.btn_on.config(state='normal', bg='green')
        self.btn_off.config(state='disabled', bg='grey')

    def __init__(self, root):
        self.root = root
        # Define title for the app
        root.title("DataReader - Server")
        # Defines the width and height of the window
        root.geometry("800x500")
        # Block resizing of Window
        root.resizable(width=False, height=False)
        # Customize the styling for the buttons and entry
        self.customFont = tkFont.Font(family="Helvetica", size=10)

        self.lbf_one = LabelFrame(root)
        self.lbf_one.grid(row=0, columnspan=7, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)

        self.lb_app = Label(self.lbf_one, text='Servidor: ', font=self.customFont)
        self.lb_app.grid(row=0, column=0, sticky=W)

        self.btn_on = Button(self.lbf_one, text="ON", fg='white', bg='green', state='normal',
                             command=self.btn_on_click, font=self.customFont)
        self.btn_on.grid(row=0,  column=1, sticky=W, padx=0)

        self.btn_off = Button(self.lbf_one, text="OFF", fg='white', bg='grey', state='disabled',
                              command=self.btn_off_click, font=self.customFont)
        self.btn_off.grid(row=0, column=2, sticky=W, padx=0)

        self.lb_status = Label(self.lbf_one, text='Status', font=self.customFont)
        self.lb_status.grid(row=1, column=0, sticky=W)

        self.lbf_two = LabelFrame(root)
        self.lbf_two.grid(row=1, columnspan=7, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)

        self.text = Text(self.lbf_two)
        self.text.grid(row=0, column=0)

    def process_queue(self):
        try:
            msg = self.queue.get(0)
            # Show result of the task if needed
            teste_server_socket().stop()
        except queue.Empty:
            self.root.after(100, self.process_queue)


class ThreadedTask(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        teste_server_socket()  # Simulate long running process
        self.queue.put("Task finished")

root = Tk()
root.columnconfigure(0, weight=0)
# Get font data
# label = Label(root, text="Hello, world")
# font = tkFont.Font(font=label['font'])
# print(font.actual())

reader = Reader(root)
root.mainloop()

