import socket
from tkinter import *
import tkinter as tk
from tkinter import messagebox
from  tkinter import ttk
from tkinter.ttk import *

from tkcalendar import*
import datetime
from PIL import Image , ImageTk
import babel.numbers

FORMAT = "utf8"
END='end'
SERVER_PORT = 65432

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# option====================
LOGIN='login'
REGISTER = 'register'
SEARCH_IP='search_ip'
QUERY = 'query'
QUIT = 'quit'

# response ========================
OKE='oke'
FAIL="fail"

def f_recvList(client): # client :socket
    list=[]
    item = client.recv(1024).decode(FORMAT)
    
    while( item != END):
        list.append(item)
        client.sendall(item.encode(FORMAT)) 
        item = client.recv(1024).decode(FORMAT)
        
    return list


def f_client_SendList(client,list):
    
    for temp in list:
        client.sendall(temp.encode(FORMAT))
        # nhan response tu sever
        client.recv(1024)
        
    msg = END 
    client.send(msg.encode(FORMAT))
    

# trang dang nhap / dang ki cua client
class startPage(tk.Frame):
  
    def __init__(self, Parent,appController):
        tk.Frame.__init__(self,Parent) # parent = container chứa cái frame
       
        self.img=ImageTk.PhotoImage(Image.open("image/client.ico"))
        self.img_label = tk.Label(self,image=self.img ,height=250,width=260)
        self.img_label.pack(side=LEFT)
        
        
        self.label_LOGIN = tk.Label(self , text="CLIENT LOGIN / REGISTER ",font=("algerian",15))
        self.label_username = tk.Label(self, text="username",font=("time new roman",10))
        self.label_password = tk.Label(self, text="password",font=("time new roman",10))
        self.label_notice = tk.Label(self,text="",  fg="red")
        self.label_notice_register = tk.Label(self,text="",fg="red")
        
    
        self.entry_user = tk.Entry(self,width=20,bg='white')
        self.entry_pass = tk.Entry(self,width=20,bg='white')
        
        
        self.button_login = tk.Button(self,text="login", font=("time new roman",8),
                                      bg="#994422",fg="white",bd=3,width=7,
                                      command = lambda:appController.login(self,client))
      
        self.button_register = tk.Button(self,text="register", font=("time new roman",8),
                                      bg="#994422",fg="white",bd=3,width=7,
                                      command = lambda:appController.register(self,client))
        
        
        self.label_LOGIN.pack(pady=20)      
        self.label_username.pack()
        self.entry_user.pack()
        self.label_password.pack()
        self.entry_pass.pack()
        self.label_notice.pack()
        self.button_login.pack()
        self.label_notice_register.pack()
        self.button_register.pack()
       
# trang hien thi ti gia vang tra cua             
class homePage(tk.Frame):
    
    def __init__(self,parent, appController): # appcontroller ~ self trong APP() , de goi ham showPage
        tk.Frame.__init__(self,parent)
      
        self.label_Title = tk.Label(self,text="LOOK UP GOLD RATE",font=("algerian",18))
        
        self.label_notice = tk.Label(self,text="" , fg="red",font=("time new roman",10))
        self.label_typeGold= tk.Label(self,text=" GOLD TYPE ",font=("Amasis MT Pro Medium",13))
        self.label_date=tk.Label(self,text="DATE",font=("Amasis MT Pro Medium",13))
         
        self.button_logout = tk.Button(self,text = "log out" ,font=("time new roman",9),
                                      bg="#994422",fg="white",bd=3,width=7,
                                      command= lambda:[self.refresh_data(),appController.showPage(startPage)]
                                      )
        
        self.button_quit = tk.Button(self,text = "quit" ,font=("time new roman",9),
                                      bg="#994422",fg="white",bd=3,width=7,
                                       command= self.quitMSG
                                    )
        self.button_logout.pack(side =BOTTOM , pady=5)
        
        self.button_search = tk.Button(self,text="search",font=("time new roman",10),
                                      bg="#994422",fg="white",bd=3,width=6,
                                      command = self.search_Gold_pr)    
         
        self.button_quit.pack(side=BOTTOM)
        
        self.list_GoldType= ["SJC","AVPL","DOJI","HCM","Lộc Phát Tài","Nữ Trang"]
        
        self.cal = DateEntry(
                        self,takefocus = 0,
                        width=12, background='#994422',
                        foreground='white',
                        borderwidth=0,
                        showweeknumbers= False,
                        date_pattern= "dd/mm/yyyy",
                        )
        
        self.combobox_typeGold = Combobox(self, values= self.list_GoldType , width=20)
        
        #self.combobox_typeGold.set(self.list_GoldType[0])

        self.label_Title.place(x=205,y=5)
        self.label_typeGold.place(x=0,y=50)
        self.combobox_typeGold.place(x=120,y=50)
        self.label_date.place(x=20,y=90)
        self.cal.place(x=120,y = 90)
        self.label_notice.place(x=50,y=110)
        self.button_search.place(x=350,y=90)
        
        
        self.stype = ttk.Style()
        self.stype.theme_use("clam") # setup mau 
        
        self.stype.configure("Treeview",
                            background = "#D3D3D3" ,
                            rowheight = 25)
        
        self.frame_searchGold = tk.Frame(self , bg="black" ,height=100)
       
        self.tree_gold = ttk.Treeview(self.frame_searchGold)
        
        self.tree_gold ["column"] = ("NAME" ,"BUY" , "SELL","PLACE")
        
        self.tree_gold.column("#0", width=0, stretch=tk.NO)
        self.tree_gold.column("NAME" , anchor='c' , width=150)
        self.tree_gold.column("BUY" , anchor='c' , width=125)
        self.tree_gold.column("SELL" , anchor='c' , width=125)
        self.tree_gold.column("PLACE" , anchor='c' , width=180)
        
        self.tree_gold.heading("0", text="", anchor='c')
        self.tree_gold.heading("NAME", text="NAME", anchor='c')
        self.tree_gold.heading("BUY", text="BUY", anchor='c')
        self.tree_gold.heading("SELL", text="SELL", anchor='c')
        self.tree_gold.heading("PLACE", text="PLACE", anchor='c')
                
        self.tree_gold.pack()
        
        
    def recieve_listGold(self): # luu lai o dang list cua list [[],[],...]
        listGold = []
        gold =[]
        data= ''
        
        while (True):
            data = client.recv(1024).decode(FORMAT) # nhan msg tu sever
            client.sendall(data.encode(FORMAT)) # gui phan hoi lai
            
            if(data == "end"): # neu nhan xong r thi thoat
                break
            
            #gold  [TYPE,BUY,SELL,PLACE]
            for i in range(4):
                
                data = client.recv(1024).decode(FORMAT) # nhan cac phan tu trong tuple
                client.sendall(data.encode(FORMAT)) # phan hoi
                gold.append(data)
                       
            listGold.append(gold)    
            gold = [] 
        
        return listGold    
   
    def search_Gold_pr(self):
        date_search = self.cal.get()
        type_gold = self.combobox_typeGold.get()
        
        if( date_search ==""):
            self.label_notice["text"] = "date can not be empty !"
            return
        if( type_gold ==""):
            type_gold =  "noType"
            
            dele = self.tree_gold.get_children()
            for item in dele:
                self.tree_gold.delete(item)
        
        self.label_notice["text"] = ""
        
        try:
            
            client.sendall(QUERY.encode(FORMAT)) # gửi option qua 
            client.recv(1024) # nhan phan hoi 
            client.sendall(date_search.encode(FORMAT)) # gửi ngày qua
            client.recv(1024)  # nhan phan hoi
            client.sendall(type_gold.encode(FORMAT)) # gửi loai vang qua
             
            result = client.recv(1024).decode(FORMAT)  # nhan phan hoi ket qua
            if(result == "NO"):
                
                self.label_notice["text"] = "not found !!"
                dele = self.tree_gold.get_children()
                for item in dele:
                    self.tree_gold.delete(item)
                    
                return
            
            else:
            
                client.sendall(result.encode(FORMAT)) 
                
                # ================ nhan kieu vang ===========
                list_goldType = []
                list_goldType = f_recvList(client)
                client.sendall(type_gold.encode(FORMAT)) 
                self.list_GoldType = list_goldType
                #============================================
                
                listGold = []
                listGold = self.recieve_listGold()
                
                # reset lại trc khi tra ======
                dele = self.tree_gold.get_children()
                for item in dele:
                    self.tree_gold.delete(item)
                    
                # =========== hien thi frame tra gia vang ==========
                for l in listGold:
                    self.tree_gold.insert(parent="", index="end",text = "" , values=(l[0],l[1],l[2],l[3]))  
                
                self.frame_searchGold.place(x=25,y=140)
                
        except:
            print("SERVER ERROR !!!")  
            self.errorMSG()  
            
    def refresh_data(self):
        dele = self.tree_gold.get_children()
        for item in dele:
            self.tree_gold.delete(item)     
        self.frame_searchGold.place_forget()   
                
    def errorMSG(self):
        if messagebox.showwarning('CLIENT' , 'server not responding,quit now ?'):
            self.quit()
    
    def quitMSG(self):
        if  messagebox.askokcancel('CLIENT', 'quit now ?'):
            client.sendall(END.encode(FORMAT))
            self.quit()
        else:
            pass
    
class  PAGE_CONNECT_TO_HOST(tk.Frame):
    
    def __init__(self,parent, appController):
        
        tk.Frame.__init__(self,parent)
        label_namePage=tk.Label(self,text = " CONNECT TO SERVER ",font=("algerian",15))
        label_tap=tk.Label(self,text="",height=1)
        label_INPUT = tk.Label(self,text=" HOST IP : ",font=("algerian",12))
        
        self.entry_INPUT= tk.Entry(self,width=25,bg='white',font=("time new roman",10))
        
        self.label_notice=tk.Label(self,text="",height=2 ,fg="red",font=("time new roman",10))
        
        self.button_search= tk.Button(self,text="connect" ,
                                      font=("time new roman",10),
                                      bg="#994422",fg="white",bd=3,width=7
                                      ,command = lambda:appController.startConn(self))
        
        
        label_namePage.pack()
        label_tap.pack()
        label_INPUT.pack(pady=10)
        self.entry_INPUT.pack()
        self.label_notice.pack()
        self.button_search.pack()
        

class APP(tk.Tk):
    def __init__(self):
        
        tk.Tk.__init__(self) 
        self.protocol("WM_DELETE_WINDOW" , self.handleProtocol)
        self.title("CLIENT") 
        self.geometry("400x250")
        self.resizable(width="False",height="False")  
        
        container = tk.Frame() 
        container.configure(bg="blue")
        container.pack(side="top",fill="both",expand=True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)
    
        self.frames={}
        
        for F in (startPage,homePage,PAGE_CONNECT_TO_HOST):
            frame = F(container,self) 
            
            frame.grid(row=0,column=0,sticky="nsew")
            
            self.frames[F] = frame
        
        self.showPage(PAGE_CONNECT_TO_HOST)
        
    def handleProtocol(self):
        if messagebox.askokcancel("CLIENT", "Are you sure to close the window ? "):
            self.destroy()
            
    def showPage(self,Frameclass):
        if(Frameclass==homePage):
            self.geometry("630x500")
            
        if(Frameclass==startPage):
            self.geometry("520x300") 
               
        self.frames[Frameclass].tkraise()
                 
    def login(self,curframe,sck : socket): # curfram ~ self cua startPage
        try:
            username = curframe.entry_user.get()
            password = curframe.entry_pass.get()
            if username =="" or password == "":
                curframe.label_notice['text'] = "empty password or username !"
                return           
           
            curframe.label_notice['text'] = ""
            curframe.label_notice_register['text'] = ""   
           
            
            sck.sendall(LOGIN.encode(FORMAT)) # gui option login
            
            sck.recv(1024) # nhận phản hồi
            
            list=[]
            list.append(username)
            list.append(password)
            
            f_client_SendList(sck,list) # gui account 
            
            result = sck.recv(1024).decode(FORMAT)
            if(result == OKE):
    
                self.showPage(homePage)
                                
            else:
                curframe.label_notice['text'] = " Login failed, please check your account again !"
                return
        except:
            
            print("server error !!")
            if messagebox.showwarning('CLIENT' , 'server not responding,quit now ?'):
                self.quit()
    
                     
    def register(self,curframe,sck : socket): # curfram ~ self cua startPage
        try:
            username = curframe.entry_user.get()
            password = curframe.entry_pass.get()
            
            if username =="" or password == "":
                curframe.label_notice_register['text'] = "empty password or username !"
                return 
            
            curframe.label_notice_register['text'] = ""   
            curframe.label_notice['text'] = ""       
            
            list=[]
            list.append(username)
            list.append(password)
            
            sck.sendall(REGISTER.encode(FORMAT)) # gui option 
            
            sck.recv(1024) # nhận phản hồi
           
            f_client_SendList(sck,list) # gui account 
            
            result = sck.recv(1024).decode(FORMAT)
            
            if( result == OKE):
                messagebox.showinfo('CLIENT', 'register successfully.')
                curframe.label_notice['text'] = ""
                curframe.label_notice_register['text'] = ""   
                
                return
            else:
                curframe.label_notice_register['text'] = "register failed ,username already exists "
                return   
        except:
            print("server error !!")  
            if messagebox.showwarning('CLIENT' , 'server not responding,quit now ?'):
                self.quit()
      

    def startConn(self,curframe):
        HOST = curframe.entry_INPUT.get()
        if(HOST == ""):
            curframe.label_notice['text'] = "empty! please enter host ip."
        try: 
            
            client.connect((HOST,SERVER_PORT))
            print("CLIENT SIDE")
            curframe.label_notice['text'] = ""
            self.showPage(startPage)
            messagebox.showinfo('CLIENT', 'connected successfully.')
                        
        except:
            if(HOST != ""):
               curframe.label_notice['text'] = " connect failed "
            
       
app = APP()
app.iconbitmap('image/client.ico')
app.mainloop()


