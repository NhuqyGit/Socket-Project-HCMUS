import socket
import os
from tkinter import messagebox
import tkinter
from getpass import getpass
from msvcrt import getch
import json
import datetime
import threading
from tkinter import ttk
from tkinter import *
#HOST = '127.0.0.1'
global PORT, SERVER
SERVER = input('Server address: ')
PORT = 123
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def checkChar(strTemp):
    char=['/','>','<','|','\\',':','*','?','\'','\"']
    i=0
    while i <len(strTemp):
        j=0
        while j<len(char):
            if strTemp[i]==char[j]:
                return False  
            j+=1   
        i+=1
    return True
def checkUserPass(strTemp):
    i=0
    #strTemp=str(strTemp)
    if len(strTemp)<8:
        return False
    if len(strTemp)>=16:
        return False
    while i<len(strTemp):
        if strTemp[i]==' ':
            return False
        i+=1
    if checkChar(strTemp)==False:
        return False
    return True

def login():
    account=entry_Account.get()
    password=entry_password.get()
    if checkUserPass(account) == False:
        messagebox.showerror('Error','account or password with less than 8 characters or more than 16 characters or with special character')
        return
    if checkUserPass(password) == False:
        messagebox.showerror('Error','account or password with less than 8 characters or more than 16 characters or with a special character')
        return
    Login = account + ' ' + password + ' ' + 'LOGIN'
    client.sendall(Login.encode(FORMAT))
    report = client.recv(1024).decode(FORMAT)
    if report == "Login failed":
        messagebox.showerror('Error','Account is not exist or password is wrong')
    elif report== "Login success":
        window.destroy()          
    return

def register():
    account=entry_Account.get()
    password=entry_password.get()
    if checkUserPass(account) == False:
        messagebox.showerror('Error','account or password with less than 8 characters or more than 16 characters or with a space character')
        return
    if checkUserPass(password) == False:
        messagebox.showerror('Error','account or password with less than 8 characters or more than 16 characters or with a space character')
        return
    Register = account + ' ' + password + ' ' + 'REGIS'
    client.sendall(Register.encode(FORMAT))
    report = client.recv(1024).decode(FORMAT)
    if report == "Regis failed":
        messagebox.showerror('Error','Account already exists')
    elif report=="Regis success":
        messagebox.showinfo('Congratulations','Account was registered, login again to get inside')
    return

try:
    window=tkinter.Tk()
    window.title('covid 19')
    window.geometry('300x200')
    label_Covid19=tkinter.Label(window,text='Covid 19',font=('Arial',30))
    label_Covid19.grid(column=1,row=0)       
    button_Login = tkinter.Button(window,text='LOGIN',command=login)
    button_Login.grid(column=2,row=2,sticky='snwe')        
    button_Register=tkinter.Button(window,text='REIISTER',command=register)
    button_Register.grid(column=2,row=3,sticky='snwe') 
    label_Account = tkinter.Label(window,text='Account')
    label_Account.grid(column=0,row=2)
    label_Password = tkinter.Label(window,text='Password')
    label_Password.grid(column=0,row=3)
        
    entry_Account=tkinter.Entry(window)
    entry_Account.grid(column=1,row=2)
        
    entry_password=tkinter.Entry(window)
    entry_password.grid(column=1,row=3)

    def Exit():
        client.sendall('Exit'.encode(FORMAT))
        window.destroy()
        return
            
    button_Exit=tkinter.Button(window,text='Exit',command=Exit)
    button_Exit.place(x=270,y=175)

    window.mainloop()  
    client.sendall('1a'.encode(FORMAT))
    if client.recv(1024).decode(FORMAT)!='OK':            
        window1=tkinter.Tk()
        window1.title('Covid 19')
        window1.geometry('350x425')
        label_Covid19 =tkinter.Label(window1,text='Covid 19',font=('Arial',30))
        label_Covid19.grid(column=1,row=0)

        f = open('country.txt',)
        country=[]
        line=f.readline()
        while line!='':
            if '\n' in line:
                line=line[:len(line)-1]
            country.append(line)
            line=f.readline()


        label_Country =tkinter.Label(window1,text='Country',width=12)
        label_Country.grid(column=0,row=1)

        cb_Country=ttk.Combobox(window1)
        cb_Country['value']=country
        cb_Country.grid(column=1,row=1)
        cb_Country.current(0)

        label_Date =tkinter.Label(window1,text='Date')
        label_Date.grid(column=0,row=2)
        x=datetime.datetime.now()
        date=x.strftime(f'%d')+'/'+x.strftime(f'%m')+'/'+x.strftime(f'%y')
        entry_Date=tkinter.Entry(window1)
        entry_Date.grid(column=1,row=2)
        entry_Date.insert(0,date)

        def handleBuuton():
            i=0
            while i<len(country):
                if cb_Country.get()==country[i]:
                    
                    date_list=entry_Date.get().split('/')
                    date=date_list[0]+date_list[1]+date_list[2]                  

                    temp=cb_Country.get()+'+'+date
                    client.sendall(temp.encode(FORMAT))
                    temp=client.recv(1024).decode(FORMAT)
                    if temp=='none':
                        messagebox.showerror('error','country or date is not exist')
                    else:
                        info_list=temp.split(' ')

                        label_country.configure(text=cb_Country.get())
                        label_date.configure(text=entry_Date.get())
                        label_cases.configure(text=info_list[0])
                        label_todayCases.configure(text=info_list[1])
                        label_deaths.configure(text=info_list[2])
                        label_todayDeaths.configure(text=info_list[3])
                        label_recovered.configure(text=info_list[4])
                        label_active.configure(text=info_list[5])
                        label_critical.configure(text=info_list[6])
                        label_casesPerOneMillion.configure(text=info_list[7])
                        label_deathsPerOneMillion.configure(text=info_list[8])
                        label_todayTests.configure(text=info_list[9])
                        label_testsPerOneMillion.configure(text=info_list[10])
                    return
                i+=1
            messagebox.showinfo('error','country not exist')
            return

        button_Find=tkinter.Button(window1,text=('Find'),command=handleBuuton)
        button_Find.grid(column=2,row=1)
        
        label_country=tkinter.Label(window1,text=cb_Country.get(),font=('Arial',15))
        label_country.grid(column=1,row=4)
        label_date=tkinter.Label(window1,text=date)
        label_date.grid(column=1,row=5)

        label_cases=tkinter.Label(window1,text='Cases')
        label_cases.place(x=30,y=150)
        label_todayCases=tkinter.Label(window1,text='Today Cases')
        label_todayCases.place(x=30,y=175)
        label_deaths=tkinter.Label(window1,text='Deaths')
        label_deaths.place(x=30,y=200)
        label_todayDeaths=tkinter.Label(window1,text='Today Deaths')
        label_todayDeaths.place(x=30,y=225)
        label_recovered=tkinter.Label(window1,text='Recovered')
        label_recovered.place(x=30,y=250)
        label_active=tkinter.Label(window1,text='Active')
        label_active.place(x=30,y=275)
        label_critical=tkinter.Label(window1,text='Critical')
        label_critical.place(x=30,y=300)
        label_casesPerOneMillion=tkinter.Label(window1,text='Cases per one million')
        label_casesPerOneMillion.place(x=30,y=325)
        label_deathsPerOneMillion=tkinter.Label(window1,text='Deaths per one million')
        label_deathsPerOneMillion.place(x=30,y=350)
        label_todayTests=tkinter.Label(window1,text='Today tests')
        label_todayTests.place(x=30,y=375)
        label_testsPerOneMillion=tkinter.Label(window1,text='Tests per one million')
        label_testsPerOneMillion.place(x=30,y=400)
        
        tempDate=date.split('/')
        tempDate=tempDate[0]+tempDate[1]+tempDate[2]
        temp=cb_Country.get()+'+'+tempDate
        client.sendall(temp.encode(FORMAT))
        temp=client.recv(1024).decode(FORMAT)

        info_list=temp.split(' ')

        label_cases=tkinter.Label(window1,text=info_list[0])
        label_cases.place(x=200,y=150)
        label_todayCases=tkinter.Label(window1,text=info_list[1])
        label_todayCases.place(x=200,y=175)
        label_deaths=tkinter.Label(window1,text=info_list[2])
        label_deaths.place(x=200,y=200)
        label_todayDeaths=tkinter.Label(window1,text=info_list[3])
        label_todayDeaths.place(x=200,y=225)
        label_recovered=tkinter.Label(window1,text=info_list[4])
        label_recovered.place(x=200,y=250)
        label_active=tkinter.Label(window1,text=info_list[5])
        label_active.place(x=200,y=275)
        label_critical=tkinter.Label(window1,text=info_list[6])
        label_critical.place(x=200,y=300)
        label_casesPerOneMillion=tkinter.Label(window1,text=info_list[7])
        label_casesPerOneMillion.place(x=200,y=325)
        label_deathsPerOneMillion=tkinter.Label(window1,text=info_list[8])
        label_deathsPerOneMillion.place(x=200,y=350)
        label_todayTests=tkinter.Label(window1,text=info_list[9])
        label_todayTests.place(x=200,y=375)
        label_testsPerOneMillion=tkinter.Label(window1,text=info_list[10])
        label_testsPerOneMillion.place(x=200,y=400)
    

        def Exit1():
            client.sendall('Exit'.encode(FORMAT))
            window1.destroy()
            return
            
        button_Exit=tkinter.Button(window1,text='Exit',command=Exit1)
        button_Exit.place(x=320,y=400)
        window1.mainloop()
                      
except:
    client.close()

finally:
    client.close()
    