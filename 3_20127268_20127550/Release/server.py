from socket import*
import json
import threading
from tkinter.constants import W
import requests
import os.path
import datetime
from tkinter import Label, Tk, messagebox
import tkinter
from os import path
from _thread import *
from typing import Counter
from threading import*
import socket
from threading import Timer

#HOST = '127.0.0.1'
SERVER_NAME = socket.gethostname()
SERVER = socket.gethostbyname(SERVER_NAME) #lay ip từ máy host vd: 192.168.1.1
global PORT
PORT = 123
ADDR = (SERVER, PORT) ## tương ứng ('127.0.0.1', random(port))
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

clientsConn=[]
clientsAddr=[]
clientsAccount=[]
def infomation():
    print("[SERVER IFOMATION]")
    print("---------------------------------------")
    print(f"  Server name.....: {SERVER_NAME}")
    print(f"  Server address..: {SERVER}")
    print(f"  Port............: {PORT}")
    print("---------------------------------------")

def read_file(file_name):
    with open(file_name, 'r') as f:
        result=[]
        line = f.readline()
        while line != '':
            if '\n' in line:
                line = line[:len(line) - 1]
            result.append(line)
            line = f.readline()
    return result

def write_file(file_name, username, password):
    f = open(file_name, 'a')
    f.write('\n' + username)
    f.write('\n' + password)

def login_check(username, password):
    i = 0
    list = read_file("account.txt")
    while i < len(list):
        if list[i] == username and list[i+1] == password:
            return True
        i += 2
    return False

def signUp_check(username):
    i = 0
    list = read_file("account.txt")
    while i < len(list):
        if list[i] == username:
            return True

        i += 2
    return False

def readInfoCovid(temp):
    temp_list=temp.split('+')
    if path.exists(temp_list[1]+'.json') ==True:
        f= open(temp_list[1]+'.json',)
        data=json.load(f)
        for i in data:
            if(i['country']==temp_list[0]):
                info=str(i['cases'])+' '+str(i['todayCases'])+' '+str(i['deaths'])+' '+str(i['todayDeaths'])+' '+str(i['recovered'])+' '+str(i['active'])+' '+str(i['critical'])+' '+str(i['casesPerOneMillion'])+' '+str(i['deathsPerOneMillion']) + ' ' + str(i['totalTests'])+' '+str(i['testsPerOneMillion'])
                return info
    else:
        return 'none'



def client_thread(conn, addr):
    print(f'{addr} connected')
    GUI()
    try:
        while True:
            account = conn.recv(1024).decode(FORMAT)
            if account == "Exit":
                conn.sendall('OK'.encode(FORMAT))
                break
            
            account_list = account.split(' ')
            #print(account_list)
            option = account_list[2]
            #print(option)

            if option == 'LOGIN':
                status = login_check(account_list[0], account_list[1])
                if status == True:
                    conn.sendall('Login success'.encode(FORMAT))
                    conn.recv(1024).decode(FORMAT)
                    conn.sendall('Login success'.encode(FORMAT))
                    clientsAccount.append(account_list[0])
                    GUI()
                    print(f'{addr} Account {account_list[0]} is logged')
                    while True:
                        
                        temp = conn.recv(1024).decode(FORMAT)
                        if(temp=='Exit'):
                            break
                        temp=readInfoCovid(temp)
                        conn.sendall(temp.encode(FORMAT))
                    break                 
                elif status == False:
                    conn.sendall('Login failed'.encode(FORMAT))
            
            elif option == "REGIS":
                status = signUp_check(account_list[0])
                if status == False:
                    conn.sendall('Regis success'.encode(FORMAT))
                    write_file('account.txt',account_list[0], account_list[1])
                    print(f'{addr} Account {account_list[0]} is registered')
                elif status == True:
                    conn.sendall('Regis failed'.encode(FORMAT))
    except:
        print(f'{addr} is interrupted suddenly!!')
        conn.close()
    finally:
        print(f'{addr} disconnect!!')
        clientsConn.remove(conn)
        clientsAddr.remove(addr)
        GUI()
        i=0
        while i< len(clientsAccount):
            if account_list[0]==clientsAccount[i]:
                clientsAccount.remove(account_list[0])
                break
        GUI()
        conn.close()
def uppdateInfoPerOneHour():
    x=datetime.datetime.now()
    present=x.strftime(f'%d')+x.strftime(f'%m')+x.strftime(f'%y')
    r=requests.get('https://coronavirus-19-api.herokuapp.com/countries')

    if path.exists(present+'.json') ==True:
        f= open(present+'.json','w')
        f.write(r.text)
    else:
        f= open(present+'.json','x')
        f.write(r.text)
    t=threading.Timer(3600,uppdateInfoPerOneHour)

def closeAllClient():
    #data.delete(0,tkinter.END)
    i=0
    while i<len(clientsConn):
        clientsConn[i].close()
        i+=1
def GUI():
    data.delete(0,tkinter.END)
    i=0
    while i<len(clientsAccount):
        data.insert(tkinter.END,str(clientsAddr[i])+' -- '+str(clientsAccount[i]))
        i+=1
    while i<len(clientsAddr):
        data.insert(tkinter.END,str(clientsAddr[i]))
        i+=1
    data.pack()

window=Tk()
window.geometry('300x300')
window.title('server covid 19')
label_Sever= tkinter.Label(window,text='Active Account On Sever',font=('Arial',15))
label_Sever.pack()
button_closeAllClient=tkinter.Button(window,text='Close all client',command=closeAllClient)
button_closeAllClient.place(x=210,y=275)
data = tkinter.Listbox(window, height = 10,width = 100)   
scroll= tkinter.Scrollbar(window)
scroll.pack(side = tkinter.RIGHT, fill= tkinter.BOTH)
data.config(yscrollcommand = scroll.set)
    
scroll.config(command = data.yview)
data.pack()
uppdateInfoPerOneHour()
infomation()
server.bind(ADDR)
server.listen()
print("\n[SERVER DISPLAY]")
print(f"[LISTEN] Server is listenning to client on {SERVER}")

def run():
    while True:
        conn, addr = server.accept()
        clientsConn.append(conn)
        clientsAddr.append(addr)
        thread=Thread(target=client_thread,args=(conn,addr))
        thread.start()

thread=Thread(target=run)
thread.daemon=True
thread.start()

window.mainloop()
