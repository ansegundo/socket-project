from tkinter import *
import tkinter.font as tkfont
import socket
import threading


class Reader:

    def start_server_socket(self):
        self.connected = True
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('localhost', 9999))  # Bind to the port
        self.s.listen(10)  # Now wait for client connection.
        print('server listening....')

        try:
            conn, address = self.s.accept()  # Establish connection with client.
            print(address)
        except:
            print('cliente nao conectado')

        while self.connected:
            try:
                data = conn.recv(1024)
                if bytes.decode(data) == '':
                    self.connected = False
                    self.close_server_socket()
                    self.start_server_socket()
            except:
                print('disconnected')
                self.connected = False

        self.get_files(conn, data)

    def close_server_socket(self):
        if not self.connected:
            self.s.close()
            print('connection closed function')

    def get_files(self, conn, data):
        with open('received_file.txt', 'wb') as file:
            print('file opened')
            while data:
                # write data to a file
                file.write(data)
                print('receiving data...')
                data = conn.recv(1024)
                # print('data=%s', (data))
                if not data:
                    break

        file.close()
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

    def btn_refresh_files(self):
        print('refresh')
        with open('received_file.txt', 'wb') as f:
            print('file opened')
            while True:
                print('receiving data...')
                data = self.s.recv(1024)
                # print('data=%s', (data))
                if not data:
                    break
                # write data to a file
                f.write(data)

        f.close()
        print('Successfully get the file')
        self.s.close()
        print('connection closed')

    def __init__(self, root):
        self.root = root
        self.s = ''
        self.connected = False

        root.title("DataReader - Server")
        root.geometry("800x500")
        root.resizable(width=False, height=False)

        self.customFont = tkfont.Font(family="Helvetica", size=10)

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

        self.btn_refresh = Button(self.lbf_two, text="Refresh", fg='white', bg='grey',
                              command=self.btn_refresh_files, font=self.customFont)
        self.btn_refresh.grid(row=1, column=0)



root = Tk()
root.columnconfigure(0, weight=0)
reader = Reader(root)
root.mainloop()

