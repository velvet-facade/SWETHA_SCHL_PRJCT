from tkinter import *
from tkinter import messagebox,ttk
import mysql.connector as sql
from PIL import ImageTk,Image
from random import *
import time
import datetime as dt
conn = sql.connect(host="127.0.0.1",
                   passwd="1234",
                   user="root",
                   database="EBMS")
c=conn.cursor()

#functions

def entry():
    global e1,e2,e3,root1
    try:
        username=e1.get()
        password=e2.get()
        cpswd=e3.get()
    except:
        return
    if len(username)!=0 and len(password)!=0 and len(cpswd)!=0:
        c.execute("select * from user where username ='{}'".format(username))
        x=c.fetchall()
        if len(x)>0:
            messagebox.showerror("INVALID","USERNAME ALREADY EXISTS!..TRY AGAIN")
            root1.lift()
        else:
            if password==cpswd:
                c.execute("insert into user values('{}','{}')".format(username,password))
                conn.commit()
                messagebox.showinfo("DONE","YOU HAVE BEEN REGISTERED!")
            else:
                messagebox.showinfo("ERROR","ENTER SAME CONFIRM PASSWORD")
                root1.lift()

def addcustomer():
    try:
        name=e1.get()
        print(name)
        address=t1.get(1.0,"end-1c")
        print(address)
        phoneno=e3.get()
        print(phoneno)
        email=e4.get()
        print(email)
    except:
        return
    if len(name)!=0 and len(address)!=0 and len(email)!=0 and len(str(phoneno))!=0:
        c.execute('insert into customer values({},"{}","{}","{}",{},"{}")'.format(accountno,username,name,address,phoneno,email))
        conn.commit()
        messagebox.showinfo("DONE","ACCOUNT CREATED SUCCESFULLY")
        root4.destroy()
    else:
        messagebox.showerror("ENTRY","FILL ALL THE BLANKS")
        root2.lift()
        root3.lift()
        root4.lift()

def newcustomer():
    global root4,e1,t1,e3,e4,accountno
    root4=Toplevel()
    root4.geometry('400x400')
    bg=PhotoImage(file='bgimg.png')
    lbg=Label(root4,image=bg).place(x=0,y=1080)
    frame1=Frame(root4).grid(row=0,column=0)
    root4.title('NEW CUSTOMER')
    l1=Label(root4,text='NEW CUSTOMER',bg='blue',font='courier 15').grid(row=0,column=1,columnspan=2,padx=50)
    found=True
    while found:
        accountno=randrange(1000000,9999999,10)
        c.execute("select * from customer where accountno='{}'".format(accountno))
        x=c.fetchall()
        if len(x)==0:
            found=False
    l2=Label(root4,text='ACCOUNTNO:',bg='pink').grid(row=1,column=0,padx=5,pady=5)
    l2=Label(root4,text=accountno,bg='red',font='20').grid(row=2,column=1,padx=5,pady=5)
    l2=Label(root4,text='NAME',bg='pink').grid(row=2,column=0,padx=5,pady=5)
    e1=Entry(root4,bd=5,width=30)
    e1.grid(row=2,column=1,padx=5,pady=5)
    l3=Label(root4,text='ADDRESS',bg='pink').grid(row=3,column=0,padx=5,pady=5)
    t1=Text(root4,bd=5,width=25,height=3)
    t1.grid(row=3,column=1,padx=5,pady=5)
    l4=Label(root4,text='PHONENUMBER',bg='pink').grid(row=4,column=0,padx=5,pady=5)
    e3=Entry(root4,width=25,bd=5)
    e3.grid(row=3,column=1,padx=5,pady=5)
    l5=Label(root4,text='EMAILID',bg='pink').grid(row=5,column=0,padx=5,pady=5)
    e4=Entry(root4,width=25,bd=5)
    e4.grid(row=5,column=1,padx=5,pady=5)
    b1=Button(root4,text='PROCEED',bd=5,command=addcustomer,bg='light green').grid(row=6,column=1,pady=10)
    b2=Button(root4,text='EXIT',bd=5,command=root4.destroy,bg='light green').grid(row=7,column=1,pady=10)
    root4.mainloop()

def delete():
    try:
        accountno=e1.get()
    except:
        return
    if len(accountno)!=0:
        c.execute("select * from customer where accountno = '{}'".format(accountno))
        x=c.fetchall()
        if len(x)!=0:
            c.execute('delete from customer where accountno = {}'.format(accountno))
            conn.commit()
            messagebox.showinfo('DELETED','ACCOUNT HAS BEEN DELETED')
            root4.destroy()
        else:
            messagebox.showinfo("ERROR","ACCOUNT NO. DOESNT EXIST")
            root2.lift()
            root3.lift()
            root4.lift()
    else:
        messagebox.showerror("ENTRY","FILL ALL THE COLOUMNS")
        root2.lift()
        root3.lift()
        root4.lift()

def delaccount(): 
    global e1,root4 
    root4=Toplevel()
    root4.geometry('400x300') 
    bg=PhotoImage(file='bgimg1.png') 
    lbg=Label(root4,image=bg).place(x=0,y=0)
    frame1=Frame(root4).grid(row=0,column=0) 
    root4.title('DELETE ACCOUNT')
    l1=Label(root4,text='DELETE ACCOUNT',bg='blue',font='courier 15').grid(row=0,column=1)
    l2=Label(root4,text='ACCOUNT NO',bg='pink').grid(row=1,column=0,padx=5,pady=5)
    e1=Entry(root4,bd=5,width=30) 
    e1.grid(row=1,column=1,padx=5,pady=5) 
    b1=Button(root4,text='PROCEED',bd=5,command=delete,bg='lightgreen').grid(row=3,column=1,pady=15) 
    b2=Button(root4,text='EXIT',bd=5,command=root4.destroy,bg='lightgreen').grid(row=4,column=1,pady=10) 
    root4.mainloop()

def pay(): 
    global root3
    root5=Toplevel() 
    root5.title('LOADING')
    progress=ttk.Progressbar(root5,orient=HORIZONTAL,length=300,mode='determi nate')
    progress.pack() 
    for i in range(5):
        root5.update() 
        time.sleep(1) 
        progress['value']+=20
    date1=dt.date.today()
    c.execute('update transaction set status ="NO DUE" where accountno={}'.format(accountno))
    conn.commit()
    c.execute('update transaction set date="{}" where accountno={}'.format(date1,accountno))
    conn.commit() 
    root5.destroy() 
    root4.destroy()
    messagebox.showinfo('SUCCESS','PAYMENT SUCCESSFUL')


def payment():
    global root4,accountno 
    try:
        accountno=e1.get()
    except:
        return
    if len(accountno)!=0 :
        c.execute("select * from transaction where accountno='{}'".format(accountno))
        x=c.fetchall()
        c.execute("select * from customer where accountno='{}'".format(accountno)) 
        name=c.fetchall()
        if len(x)!=0:
            if x[0][3].lower()=='due': 
                root3.destroy() 
                root4=Toplevel() 
                root4.geometry('600x300')
                bg=PhotoImage(file='bgimg2.png') 
                lbg=Label(root4,image=bg).place(x=0,y=0) 
                frame1=Frame(root4).grid(row=0,column=0) 
                l1=Label(root4,text='PAYMENT',bg='yellow',font='courier15').grid(row=0,column=2,columnspan=2,padx=50) 
                l2=Label(root4,text='NAME',bg='pink',padx=40).grid(row=2,column=0)
                l3=Label(root4,text='ACCOUNTNO',bg='pink').grid(row=2,column=1,padx=5)
                l4=Label(root4,text='UNIT',bg='pink').grid(row=2,column=2) 
                l5=Label(root4,text='AMOUNT',bg='pink').grid(row=2,column=3) 
                l6=Label(root4,text='STATUS',bg='pink').grid(row=2,column=4) 
                l7=Label(root4,text='PAYMENT',bg='pink').grid(row=2,column=5) 
                l8=Label(root4,text=name[0][2]).grid(row=3,column=0) 
                l9=Label(root4,text=x[0][0]).grid(row=3,column=1,padx=5) 
                l10=Label(root4,text=x[0][1]).grid(row=3,column=2) 
                l11=Label(root4,text=float(x[0][2])).grid(row=3,column=3) 
                l12=Label(root4,text=x[0][3]).grid(row=3,column=4) 
                b1=Button(root4,text="PAY",bd=5,command=pay,bg='lightgreen').grid(row=3,column=5,pady=10,padx=10) 
                b2=Button(root4,text='EXIT',bd=5,command=root4.destroy,bg='lightgreen').grid(row=4,column=3,columnspan=2,pady=10,padx=10)
                root4.mainloop()
            else:
                messagebox.showinfo('INFO',"NO DUE TO BE PAID") 
                root3.destroy()
                root2.lift() 
                root3.lift()
        
        else:
            messagebox.showinfo("ERROR", "ACCOUNT NO. DOESN'T EXIST") 
            root2.lift()
            root3.lift()

    else:
        messagebox.showerror("ENTRY", "FILL THE COLUMN") 
        root2.lift()
        root3.lift()

def accsettings(): 
    global root3 
    root3=Toplevel()
    root3.geometry('350x300') 
    bg=PhotoImage(file='bgimg.png') 
    lbg=Label(root3,image=bg).place(x=0,y=0) 
    frame1=Frame(root3).grid(row=0,column=0) 
    root3.title('SETTINGS')
    l1=Label(root3,text='ACCOUNT SETTINGS',bg='blue',font='courier 15').grid(row=1,column=1,columnspan=3,padx=70,pady=20)
    b1=Button(root3,text='1.NEW CUSTOMER',bd=5,command=newcustomer,bg='light green').grid(row=2,column=2,pady=10,padx=50)
    b2=Button(root3,text='2.DELETE ACCOUNT',bd=5,command=delaccount,bg='light green').grid(row=3,column=2,pady=10,padx=50)
    b3=Button(root3,text='3.EXIT',bd=5,command=root3.destroy,bg='light green').grid(row=4,column=2,pady=10,padx=50)
    root3.mainloop()

def transaction(): 
    global root3,e1 
    root3=Toplevel()
    root3.geometry('400x300') 
    bg=PhotoImage(file='bgimg1.png') 
    lbg=Label(root3,image=bg).place(x=0,y=0) 
    frame1=Frame(root3).grid(row=0,column=0) 
    root3.title('TRANSACTIONS')
    l1=Label(root3,text='TRANSACTIONS',bg='blue',font='courier 15').grid(row=0,column=0,columnspan=2)
    l2=Label(root3,text='ACCOUNTNO :',bg='pink',font='courier 15').grid(row=1,column=0,pady=30)
    e1=Entry(root3,bd=5,width=30) 
    e1.grid(row=1,column=1,padx=5,pady=35) 
    b1=Button(root3,text='PROCEED',bd=5,command=payment,bg='lightgreen').grid(row=2,column=1,pady=10,padx=20) 
    b2=Button(root3,text='EXIT',bd=5,command=root3.destroy,bg='lightgreen').grid(row=3,column=1,padx=20,pady=10) 
    root3.mainloop()

def check():
    global e1,e2,e3,root1,root2,username 
    try:
        username=e1.get() 
        password=e2.get()
    except:
        return
    if len(username)!=0 and len(password)!=0 :
        c.execute("select * from user where username='{}'".format(username)) 
        x=c.fetchall()
        if len(x)>0:
            if x[0][1]==password: 
                root1.destroy() 
                root2=Toplevel() 
                root2.geometry('400x350')
                bg=PhotoImage(file='bgimg.png') 
                lbg=Label(root2,image=bg).place(x=0,y=0) 
                frame1=Frame(root2).grid(row=0,column=0) 
                root2.title('EB SYSTEM') 
                l1=Label(root2,text='WELCOME',bg='blue',font='courier15').grid(row=1,column=2,pady=5)
                l1=Label(root2,text='TO',bg='blue',font='courier 15').grid(row=2,column=2,pady=5)
                l1=Label(root2,text='ELECTRICITY BILLING SYSTEM',bg='blue',font='courier 15').grid(row=3,column=1,pady=5,padx=30,columnspan=3)
                b1=Button(root2,text='1.ACCOUNT SETTINGS',bd=5,command=accsettings,bg='light green').grid(row=4,column=2,pady=10) 
                b2=Button(root2,text='2.TRANSACTION',bd=5,command=transaction,bg='lightgreen').grid(row=5,column=2,pady=10) 
                b3=Button(root2,text='3.EXIT',bd=5,command=root2.destroy,bg='light green').grid(row=7,column=2,pady=10)
                root2.mainloop()
            else:
                messagebox.showerror("ERROR", "USERNAME/PASSWORD IS INCORRECT")
                root1.lift()
        else:
            messagebox.showerror("ENTRY", "FILL ALL THE COLOUMNS")
            root1.lift()

def newuser():
    global e1,e2,e3,root1 
    root1=Toplevel() 
    root1.geometry('400x300') 
    bg=PhotoImage(file='bgimg1.png')
    lbg=Label(root1,image=bg).place(x=0,y=0) 
    frame1=Frame(root1).grid(row=0,column=0) 
    root1.title('NEW USER')
    l1=Label(root1,text='NEW USER',bg='yellow',font='courier 15').grid(row=1,column=2)
    l2=Label(root1,text='ENTER THE USERNAME',bg='pink').grid(row=2,column=1,padx=5,pady=5)
    e1=Entry(root1,bd=5,width=25) 
    e1.grid(row=2,column=2,padx=5,pady=5) 
    l3=Label(root1,text='ENTER THEPASSWORD',bg='pink').grid(row=3,column=1,padx=5,pady=5)  
    e2=Entry(root1,width=25,bd=5,show='*') 
    e2.grid(row=3,column=2,padx=5,pady=5)  
    l4=Label(root1,text='CONFIRMPASSWORD',bg='pink').grid(row=4,column=1,padx=5,pady=5) 
    e3=Entry(root1,width=25,bd=5,show='*') 
    e3.grid(row=4,column=2,padx=5,pady=5) 
    b1=Button(root1,text='PROCEED',bd=5,bg='lightgreen',command=entry).grid(row=5,column=2,pady=15) 
    b2=Button(root1,text='EXIT',bd=5,bg='lightgreen',command=root1.destroy,padx=10).grid(row=6,column=2,pady=5) 
    root1.mainloop()

def existinguser(): 
    global e1,e2,e3,root1 
    root1=Toplevel()
    root1.geometry('400x300') 
    bg=PhotoImage(file='bgimg1.png') 
    lbg=Label(root1,image=bg).place(x=0,y=0) 
    frame1=Frame(root1).grid(row=0,column=0) 
    root1.title('EXISTING USER')
    l1=Label(root1,text='EXISTING USER',bg='yellow',font='courier 15').grid(row=1,column=2)
    l2=Label(root1,text='ENTER THE USERNAME',bg='pink').grid(row=2,column=1,padx=5,pady=5)
    e1=Entry(root1,bd=5,width=25) 
    e1.grid(row=2,column=2,padx=5,pady=5) 
    l3=Label(root1,text='ENTER THEPASSWORD',bg='pink').grid(row=3,column=1,padx=5,pady=5) 
    e2=Entry(root1,width=25,bd=5,show='*') 
    e2.grid(row=3,column=2,padx=5,pady=5) 
    b1=Button(root1,text='PROCEED',bd=5,bg='lightgreen',command=check).grid(row=5,column=2,pady=15)
    b2=Button(root1,text='EXIT',bd=5,bg='light green',command=root1.destroy,padx=10).grid(row=6,column=2,pady=5)
    root1.mainloop()

root=Tk() 
root.geometry('1280x920') 
root.configure(bg='light blue') 
bg=PhotoImage(file='bgimg.png')
lbg=Label(root,image=bg).place(x=400,y=100) 
frame1=Frame(root).grid(row=0,column=0) 
root.title('EB SYSTEM')
l1=Label(root,text='ELECTRICITY BILLING SYSTEM',bg='blue',font='courier 15').place(x=445,y=110) 
l2=Label(root,text='HOME',font='12').place(x=565,y=150) 
b1=Button(root,text='1.NEW USER',bd=5,command=newuser,bg='light green').place(x=555,y=200)
b2=Button(root,text='2.EXISTING USER',bd=5,command=existinguser,bg='light green').place(x=545,y=250) 
b3=Button(root,text='3.EXIT',bd=5,command=root.destroy,bg='light green').place(x=575,y=300)




















