import  socket
import sqlite3
from socket import error
import  threading

import tkinter as tk
from tkinter import messagebox
from  tkinter import ttk
from tkinter.constants import BOTH, BOTTOM, LEFT, RIGHT
from tkinter.font import BOLD
from tkinter.ttk import *

from PIL import Image , ImageTk
from datetime import date ,timedelta
import time

#============== thu vien ho tro lay gia vang ================
import requests
import json


#HOST_IP = '127.0.0.1'
SERVER_PORT = 65432
FORMAT ="utf8"
END = 'end'
SERVER_DATABASE = 'database\severdatabse.db'
conxSQL = sqlite3.connect(SERVER_DATABASE)
ERROR = 'error'
LOGIN = 'login'
REGISTER = 'register'
OKE = 'oke'
FAIL = "fail"
SEARCH_IP='search_ip'
QUERY = 'query'
QUIT = 'quit'

today = date.today()
dateNow = today.strftime("%d/%m/%Y") # ngày hôm nay

# ============  SERVER account =========
SERVER_USERNAME = 'server'
SERVER_PASS = '123'
#====================

CLIENT_CONNECTED=[]
CLIENT_CONNECTED.append("=>...server has started , waiting for client .....")

#=--------------------------------------- khởi tạo socket
HOST_IP = socket.gethostbyname(socket.gethostname()) # địa chỉ máy mở server


s = socket.socket(socket.AF_INET , socket.SOCK_STREAM) # SOCK_STREAM Là giao thức TCP
s.bind((HOST_IP,SERVER_PORT)) 
s.listen()


#print(HOST_IP)
#---------------------------------------------
def f_SendList(conn,list):
    for temp in list:
        conn.sendall(temp.encode(FORMAT))
        conn.recv(1024) # nhan response tu sever
        
    msg = END 
    conn.send(msg.encode(FORMAT))
    
def f_recvList(conn): 
    list=[]
    item = conn.recv(1024).decode(FORMAT)
    while( item != END):
        list.append(item) # thêm vào list
        #response lai cho client
        conn.sendall(item.encode(FORMAT)) 
        item = conn.recv(1024).decode(FORMAT)
    return list
 
# tim infor voi username
def f_find_userInfo(username):  
    conxSQL = sqlite3.connect(SERVER_DATABASE) 
    cursor = conxSQL.cursor()
    cursor.execute("SELECT * FROM account WHERE username = ?",[username])
    data =  cursor.fetchone() # lưu vào biến data , tra ve kieu tuple // nếu ,fetchall => trả về 1 list [(..,...)..]
    return data # [data se la tuple neu tim thay]


# chen infor ng dung vao database
def f_inser_User_Info (username,password):
    conxSQL = sqlite3.connect(SERVER_DATABASE)
    cursor = conxSQL.cursor()
    cursor.execute("INSERT INTO account (username,password) VALUES (?,?)",[(username),(password)])   
    conxSQL.commit()
  
    
# DANG KY TAI KHOAN
def f_client_SignUp(conn):
    try:
        info_User = f_recvList(conn) # [username,password]
        username = info_User[0]
        password = info_User[1]
        check = f_find_userInfo(username) #kiem tra username
        if check:
            LOGN_UP_FAIL= "sign up failed , Account already exists "
            
            print(LOGN_UP_FAIL)
            # gui thong bao den client username da ton tai , sign up that bai
            conn.sendall(LOGN_UP_FAIL.encode(FORMAT))
           
        else:
            # neu chua ton tai thi dk thanh cong
            LOGN_UP= "signUp successfully"
            f_inser_User_Info(username,password)
            print(LOGN_UP)
            conn.sendall(LOGN_UP.encode(FORMAT))
      
    except:
        print(ERROR)
           
                
def f_check_Client_login(userAccount):# conn la socket ket noi voi client
    try:
        username = userAccount[0]
        password = userAccount[1]
        
        data = f_find_userInfo(username) # tim TK , data là kiểu Tuple
        if data: # co tai khoan 
            if data[1] == password:  # kiem tra pass 
                                     
                LOGN_IN_SUCCESS= "login successfully" 
                #print(LOGN_IN_SUCCESS)
                
                return True
            else:
                LOGN_IN_FAILED= "login failed"
                #print(LOGN_IN_FAILED)
               
                return False
        else:    
            LOGN_IN_FAILED= "login failed"
            #print(LOGN_IN_FAILED)
            return False
               
    except :
        print(ERROR)      

# hàm lấy giá vàng
def get_Golds_info():
    
    url = 'https://tygia.com/json.php?ran=0&rate=0&gold=1&bank=VIETCOM&date=now'
    resp = requests.get(url)
    resp.encoding='utf-8-sig'
    content = resp.text.encode().decode('utf-8-sig')
    return json.loads(content)

# hàm tạo bảng và chèn ti gia vang neu chưa ton tai

def create_Table_Data(): # lay gia vang cua hom nay
   
    tablename = dateNow
    conn = sqlite3.connect("database\Golds.db") 
    cursor = conn.cursor()
    try: 
        cursor.execute("SELECT * FROM '"+tablename+"'")
        return
    except:
        
        # chua ton tai vang hom nay
        print("chua ton tai bang gia vang hom nay ")
        a = get_Golds_info()
        b = a["golds"]
        c = b[0]
        d = c['value']
       
        cursor.execute(f"""CREATE TABLE '{tablename}'(
                                        TYPE VARCHAR(30) PRIMARY KEY,
                                        BUY VARCHAR(30),
                                        SELL VARCHAR(30),
                                        PLACE VARCHAR(30))
                                        """)
    
        for i in d :
            type =  "{0}".format(i['type'])
            buy = "{0}".format(i['buy'])
            sell = "{0}".format(i['sell'])
            place = "{0}".format(i['brand'])
            cursor.execute("INSERT OR IGNORE INTO '"+tablename+"' VALUES(?,?,?,?)",[type,buy,sell,place])
        
        conn.commit()
        
                   
# hàm truy vấn vàng với ngày và kiểu vàng 
def query_Gold_DATE_TYPE(tablename:str , goldType : str): 
    
    if tablename == dateNow:  # neu tra hom nay thi kiem tra da co chưa , chưa thì tạo bang và chen veo
        create_Table_Data() 
    
    list = []
    connGold = sqlite3.connect('database\Golds.db')
    cursor = connGold.cursor()
    try:
        if(goldType ==""):
            try:
               cursor.execute("SELECT * FROM '"+ tablename + "'   ")
            except:
                return list;

        else:
            try:
                type = '%'+goldType+'%'
                cursor.execute("SELECT * FROM '"+ tablename + "' WHERE TYPE LIKE '"+type+"' COLLATE NOCASE ")
            
            except:
                return list; 

        for row in cursor.fetchall():
            list.append(row)        
                
        return list    
    
    except:
        list = []
        return list
    
    
# ham gui thong tin vang tu sever 
def send_listGold(conn , tablename , goldType):
    listGold =[]
    listGold = query_Gold_DATE_TYPE(tablename,goldType) # thong tin vang [(ten,ban,mua),(ten,ban,mua)....]
        
    for gold in listGold: # duyet theo cac pt trong list , moi phan tu la kieu tuple
        msg = "next"
        conn.sendall(msg.encode(FORMAT))
        
        conn.recv(1024) 
        
        for item in gold: # duyet theo cac phan tu cua tuple
            if(item == ''): 
                item = "N/A"  # không thể gửi nhận với một string rỗng , cần gán trc khi gửi
            item = str(item)
                       
            conn.sendall(item.encode(FORMAT))
            conn.recv(1024) 
    
    msg = "end"
    conn.sendall(msg.encode(FORMAT))
    conn.recv(1024)
 
# lay ten cac loai vang 
def query_type_of_gold(tablename):
    list = []
    connGold = sqlite3.connect('database\Golds.db')
    cursor = connGold.cursor()
    cursor.execute("SELECT * FROM '"+ tablename + "'  ")
    for row in cursor.fetchall():
        list.append(row[0]) 
        
    return list
 
 
# xử lý yêu cầu từ client
def handleClient(conn:socket,addr):
    
    try:  
        while (True):
            # LOGIN
            option = conn.recv(1024).decode(FORMAT) # nhan option tu client login/sign up
            if(option == LOGIN):
                
                conn.sendall(option.encode(FORMAT)) # gui phan hoi cho client
                account = f_recvList(conn)
                
                check_login = f_check_Client_login(account)
                
                if(check_login == True):
                    conn.sendall(OKE.encode(FORMAT))
                    
                    LOGN_IN_RESULT= "login successfully" 
                    #print(LOGN_IN_RESULT)
                    
                else:
                    conn.sendall(FAIL.encode(FORMAT))
                        
            # REGISTER   
            elif (option == REGISTER):
                
                conn.sendall(option.encode(FORMAT)) # gui phan hoi cho client
                account = f_recvList(conn)
                
                print("register tk : " ,account[0] , account[1])
                check = f_find_userInfo(account[0])
                
                if check: # nếu tồn tại tài username rồi thì fail, và gửi về client
                    print("register: da ton tai ")
                    conn.sendall(FAIL.encode(FORMAT))                     
                else:
                    print("register thanh cong ")
                    # nếu chưa thì inssert tài khoảng vào database
                    f_inser_User_Info(account[0] , account[1])
                    # gửi phản hồi lại 
                    conn.sendall(OKE.encode(FORMAT))   
                   
            elif(option == QUERY):
                
                conn.sendall(option.encode(FORMAT)) # gui phan hoi 
                table_name = conn.recv(1024).decode(FORMAT) #nhan ngay tra cung la ten bang
                conn.sendall(option.encode(FORMAT)) # gui phan hoi 
                goldType = conn.recv(1024).decode(FORMAT) # nhan loai vang
                
                if(goldType =="noType"):
                    goldType = ''
                    
                list_gold = []
                list_gold = query_Gold_DATE_TYPE(table_name ,goldType)
                 
                if(list_gold):
                    
                    msg = "OKE"
                    conn.sendall(msg.encode(FORMAT)) # gui phan hoi tim thay cho client
                    conn.recv(1024)
                    f_SendList(conn,query_type_of_gold(table_name)) # gui ten loai vang qua
                    conn.recv(1024)
                    send_listGold(conn, table_name , goldType)  # gửi list vàng qua cho client
               
                else:
                    print("tra vang khong thanh cong ")
                    msg = "NO"
                    conn.sendall(msg.encode(FORMAT)) # gui phan hoi ko tim thay
          
            else:
                print("client ",addr , " disconnected ")  
                temp = "=>  client: "+ str(addr) + " disconnected "
                CLIENT_CONNECTED.append(temp)   
                conn.close()   
                    
    except:
        print("conn (xxxx): ",addr, " disconnetced ")  
        conn.close()
        
# ===============   giao dien sever ================================


# trang dang nhap cua server
class startPage(tk.Frame): # kế thừa tk.frame
  
    def __init__(self, Parent,appController):
        tk.Frame.__init__(self,Parent)
        
        self.label_LOGIN = tk.Label(self , text="SERVER LOGIN" ,font=("algerian",15))
        self.label_username = tk.Label(self, text="username",font=("time new roman",10))
        self.label_password = tk.Label(self, text="password",font=("time new roman",10))
        self.label_notice = tk.Label(self,text="", fg="red")
        
        self.entry_user = tk.Entry(self,width=20,bg='white',font=("time new roman",10))
        self.entry_pass = tk.Entry(self,width=20,bg='white',font=("time new roman",10))
        
        self.button_login = tk.Button(self,text="login" ,
                                      font=("time new roman",9),
                                      bg="#994422",fg="white",bd=3,width=7,
                                      command = lambda:appController.server_LOGIN(self)
                                      )
        
        self.label_LOGIN.pack(pady=8)      
        self.label_username.pack(pady=5)
        self.entry_user.pack()
        self.label_password.pack(pady=5)
        self.entry_pass.pack()
        self.label_notice.pack()
        self.button_login.pack()
        
# trang quan li , hien thi thong tin client
class homePage(tk.Frame):
    def __init__(self,parent,appcontroller):
        tk.Frame.__init__(self,parent)
        self.configure(bg="#003e53")
        
        label_homePage = tk.Label(self, text= "client information on server" ,
                                  font=("algerian",15),
                                  bg="#003e53" , fg="white")
        
        label_homePage.pack(pady=10)
        
        self.frame_client = tk.Frame(self)
        self.list_client_connected = tk.Listbox(self.frame_client , height=20 , width= 50 , bg = "white")

        button_logout = tk.Button(self, text = "quit" ,
                                        font=("time new roman",10),
                                        command= self.quitMSG,
                                        width=10,height=1,bd=3)
        
        button_logout.pack(side=BOTTOM , pady=5)
        button_logout = tk.Button(
                                self, text = "refresh",
                                font=("time new roman",10)
                                ,command= self.refresh_info,width=10,height=1,bd=3
                                 )
        
        button_logout.pack(side=BOTTOM , pady=5)
       
      
      
        self.frame_client.pack_configure()
        self.scorollbar_list = tk.Scrollbar(self.frame_client)
        self.scorollbar_list.pack(side=RIGHT , fill= BOTH)
        self.list_client_connected.config(yscrollcommand=self.scorollbar_list.set)
        self.scorollbar_list.config(command=self.list_client_connected.yview)
        self.list_client_connected.pack()
        
        
        # them vao list box thong tin ket noi cua client
    def refresh_info(self):
        self.list_client_connected.delete(0,END)
        for i in range(len(CLIENT_CONNECTED)):
            self.list_client_connected.insert(i,CLIENT_CONNECTED[i])
            
    def quitMSG(self):
        if  messagebox.askokcancel('notice', 'quit now ?'):
            self.quit()
        else:
            pass
        
class APP(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        
        self.title("SERVER")
        self.geometry("350x210")
        self.resizable(width = "False" , height = "False")
        self.protocol("WM_DELETE_WINDOW" , self.handleProtocol)
        container = tk.Frame()
        container.configure()
        container.pack(side="top",fill="both",expand=True)# cho cai container tran het
        
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)
        self.frames={}
        
        for F in (startPage,homePage):
            frame = F(container,self) # nhu khoi tao homepage va startPage
            
            frame.grid(row=0,column=0,sticky="nsew")
            
            self.frames[F] = frame
        
        self.showPage(startPage)
        
        
    def handleProtocol(self):
        if messagebox.askokcancel("Notice", "Are you sure to close the window ?"):
            self.destroy()   
            
            
    def showPage(self,Frameclass):
        if(Frameclass==homePage):
            self.geometry("410x360")
        if(Frameclass==startPage):
            self.geometry("400x250")
        self.frames[Frameclass].tkraise()
    
    def server_LOGIN(self,curframe):
        username = curframe.entry_user.get()
        password = curframe.entry_pass.get()
        
        if( password =="" or username ==""):
            curframe.label_notice['text'] = "empty password or username !"
            return

        if ( username == SERVER_USERNAME and password == SERVER_PASS):
            
            self.showPage(homePage)
            curframe.label_notice['text'] = ""         
            self.threadingStart()
            
        else:
            curframe.label_notice['text'] = "Login failed !!"


    def serverStart(self):
   
        try: 
            print(HOST_IP)
            print("waiting for client")
            
            while True:
             
                conn,addr = s.accept()
                chuoi = "=>  client "+ str(addr) + " connected"
                CLIENT_CONNECTED.append(chuoi)
                print("======================")
                print("conn: ",conn.getsockname())
                print(addr)
                print("======================")
                clientThread = threading.Thread(target=handleClient, args=(conn,addr))
                clientThread.daemon = True 
                clientThread.start()
                
      
        except KeyboardInterrupt:
            print("error")
            s.close()
            
        finally:
            s.close()
            print("end")

    def threadingStart(self):
        sThread = threading.Thread(target=self.serverStart)
        sThread.daemon = True 
        sThread.start()


app= APP()
app.iconbitmap('image/server.ico')
app.mainloop()

