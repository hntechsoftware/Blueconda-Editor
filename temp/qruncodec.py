import os
import tkinter as tk

calculatorwindow = tk.Tk()
calculatorwindow.title("Calculator 2")

screen = tk.Entry(bg="white",fg="black",font=('Segoe UI Black', 16 , 'bold'), justify=tk.RIGHT)
screen.grid(row=0,column=0,columnspan=15)

fontvar = ('Segoe UI Black', 16 , 'bold')
operator = None

#defFunctions()
def onefunc():
    screen.insert(tk.END,"1")
def twofunc():
    screen.insert(tk.END,"2")
def threefunc():
    screen.insert(tk.END,"3")
def fourfunc():
    screen.insert(tk.END,"4")
def fivefunc():
    screen.insert(tk.END,"5")
def sixfunc():
    screen.insert(tk.END,"6")
def sevenfunc():
    screen.insert(tk.END,"7")
def eightfunc():
    screen.insert(tk.END,"8")
def ninefunc():
    screen.insert(tk.END,"9")
def zerofunc():
    screen.insert(tk.END,"0")
def dpfunc():
    screen.insert(tk.END,".")
def acfunc():
    screen.delete(0,tk.END)
    operator = None
    num1 = None
    num2 = None

def addfunc():
    global operator
    global num1
    operator = "add"
    num1 = float(screen.get())
    screen.delete(0,tk.END)

def minusfunc():
    global operator
    global num1
    operator = "subtract"
    num1 = float(screen.get())
    screen.delete(0,tk.END)

def timesfunc():
    global operator
    global num1
    operator = "multiply"
    num1 = float(screen.get())
    screen.delete(0,tk.END)

def divfunc():
    global operator
    global num1
    operator = "divide"
    num1 = float(screen.get())
    screen.delete(0,tk.END)

#the one function to rule them all
def equals():
    global operator
    global num1
    num2 = float(screen.get())
    if operator == "add":
        final = num1 + num2
        screen.delete(0,tk.END)
        screen.insert(0,final)
    if operator == "subtract":
        final = num1 - num2
        screen.delete(0,tk.END)
        screen.insert(0,final)
    if operator == "multiply":
        final = num1 * num2
        screen.delete(0,tk.END)
        screen.insert(0,final)
    if operator == "divide":
        final = num1 / num2
        screen.delete(0,tk.END)
        screen.insert(0,final)
#Functions
add = tk.Button(text=" + ",font=fontvar,bg="orange",width=3,command=addfunc)
add.grid(row=1,column=0)

minus = tk.Button(text=" - ",font=fontvar,bg="orange",width=3,command=minusfunc)
minus.grid(row=2,column=0)

times = tk.Button(text=" x ",font=fontvar,bg="orange",width=3,command=timesfunc)
times.grid(row=3,column=0)

div = tk.Button(text=" / ",font=fontvar,bg="orange",width=3,command=divfunc)
div.grid(row=4,column=0)

#Numpad
one = tk.Button(text=" 1 ",font=fontvar,bg="light grey",width=3,command=onefunc)
one.grid(row=1,column=1)

two = tk.Button(text=" 2 ",font=fontvar,bg="light grey",width=3,command=twofunc)
two.grid(row=1,column=2)

three = tk.Button(text=" 3 ",font=fontvar,bg="light grey",width=3,command=threefunc)
three.grid(row=1,column=3)

four = tk.Button(text=" 4 ",font=fontvar,bg="light grey",width=3,command=fourfunc)
four.grid(row=2,column=1)

five = tk.Button(text=" 5 ",font=fontvar,bg="light grey",width=3,command=fivefunc)
five.grid(row=2,column=2)

six = tk.Button(text=" 6 ",font=fontvar,bg="light grey",width=3,command=sixfunc)
six.grid(row=2,column=3)

seven = tk.Button(text=" 7 ",font=fontvar,bg="light grey",width=3,command=sevenfunc)
seven.grid(row=3,column=1)

eight = tk.Button(text=" 8 ",font=fontvar,bg="light grey",width=3,command=eightfunc)
eight.grid(row=3,column=2)

nine = tk.Button(text=" 9 ",font=fontvar,bg="light grey",width=3,command=ninefunc)
nine.grid(row=3,column=3)

zero = tk.Button(text=" 0 ",font=fontvar,bg="light grey",width=8,command=zerofunc)
zero.grid(row=4,column=1,columnspan=2)

dp = tk.Button(text=" . ",font=fontvar,bg="light grey",width=3,command=dpfunc)
dp.grid(row=4,column=3)

#Important Functions
equals = tk.Button(text=" = ",font=fontvar,bg="orange",width=3,height=3,command=equals)
equals.grid(row=1,column=4,rowspan=2)

ac = tk.Button(text=" AC ",font=fontvar,bg="orange",width=3,height=3,command=acfunc)
ac.grid(row=3,column=4,rowspan=2)

calculatorwindow.mainloop()












os.system('pause')