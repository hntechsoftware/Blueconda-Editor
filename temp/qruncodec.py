import os
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from tkinter.ttk import *
from time import strftime
from tkinter import font
import datetime as dt
import psutil
import turtle as t
import random
import time
from tkinter import ttk
from tkinter.filedialog import *
from tkinter.colorchooser import askcolor
import keyword
import re
from tkinter.messagebox import askyesno
import tkinter
import webbrowser


#Initialize the Window
window = tk.Tk()
window.title("MicrOS")
window.geometry("1000x600")
window.resizable(False,False)

#Set BG Image
image = Image.open("src/bgapp.png")  
bg_image = ImageTk.PhotoImage(image)
# Create a label with the image
label = tk.Label(window, image=bg_image)
# Place the label to fill the whole window
label.place(x=0, y=0, relwidth=1, relheight=1)

#Def time
def time():
    string = strftime('%H:%M:%S')
    lbl.config(text=string)
    lbl.after(1000, time)
lbl = tk.Label(window, font=('Arial Rounded MT Bold', 60, 'bold'),foreground='#006eff',background='#02569C')
lbl.place(x=10,y=6)
time()


#def hntechbutton
def hntech():
    webbrowser.open("https://hntechsoftware.github.io")




def calculator():
    
    calculatorwindow = tk.Tk()
    calculatorwindow.title("Calculator 2")

    screen = tk.Entry(calculatorwindow,bg="white",fg="black",font=('Segoe UI Black', 16 , 'bold'))
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
    add = tk.Button(calculatorwindow,text=" + ",font=fontvar,bg="orange",width=3,command=addfunc)
    add.grid(row=1,column=0)

    minus = tk.Button(calculatorwindow,text=" - ",font=fontvar,bg="orange",width=3,command=minusfunc)
    minus.grid(row=2,column=0)

    times = tk.Button(calculatorwindow,text=" x ",font=fontvar,bg="orange",width=3,command=timesfunc)
    times.grid(row=3,column=0)

    div = tk.Button(calculatorwindow,text=" / ",font=fontvar,bg="orange",width=3,command=divfunc)
    div.grid(row=4,column=0)

    #Numpad
    one = tk.Button(calculatorwindow,text=" 1 ",font=fontvar,bg="light grey",width=3,command=onefunc)
    one.grid(row=1,column=1)

    two = tk.Button(calculatorwindow,text=" 2 ",font=fontvar,bg="light grey",width=3,command=twofunc)
    two.grid(row=1,column=2)

    three = tk.Button(calculatorwindow,text=" 3 ",font=fontvar,bg="light grey",width=3,command=threefunc)
    three.grid(row=1,column=3)

    four = tk.Button(calculatorwindow,text=" 4 ",font=fontvar,bg="light grey",width=3,command=fourfunc)
    four.grid(row=2,column=1)

    five = tk.Button(calculatorwindow,text=" 5 ",font=fontvar,bg="light grey",width=3,command=fivefunc)
    five.grid(row=2,column=2)

    six = tk.Button(calculatorwindow,text=" 6 ",font=fontvar,bg="light grey",width=3,command=sixfunc)
    six.grid(row=2,column=3)

    seven = tk.Button(calculatorwindow,text=" 7 ",font=fontvar,bg="light grey",width=3,command=sevenfunc)
    seven.grid(row=3,column=1)

    eight = tk.Button(calculatorwindow,text=" 8 ",font=fontvar,bg="light grey",width=3,command=eightfunc)
    eight.grid(row=3,column=2)

    nine = tk.Button(calculatorwindow,text=" 9 ",font=fontvar,bg="light grey",width=3,command=ninefunc)
    nine.grid(row=3,column=3)

    zero = tk.Button(calculatorwindow,text=" 0 ",font=fontvar,bg="light grey",width=8,command=zerofunc)
    zero.grid(row=4,column=1,columnspan=2)

    dp = tk.Button(calculatorwindow,text=" . ",font=fontvar,bg="light grey",width=3,command=dpfunc)
    dp.grid(row=4,column=3)

    #Important Functions
    equals = tk.Button(calculatorwindow,text=" = ",font=fontvar,bg="orange",width=3,height=3,command=equals)
    equals.grid(row=1,column=4,rowspan=2)

    ac = tk.Button(calculatorwindow,text=" AC ",font=fontvar,bg="orange",width=3,height=3,command=acfunc)
    ac.grid(row=3,column=4,rowspan=2)





def playagame():
    # Create a turtle screen object
    screen = t.Screen()
    t.bgpic("src/bg.png")

    #Initialize Window
    screen.title("XPlane: HNTech")
    screen.bgcolor("#adfffe")
    screen.setup(770,370)

    #Initialize variables
    score = 0

    #Initialize characters

    jet = t.Turtle()
    screen.addshape("src/jetchar.gif")
    jet.shape("src/jetchar.gif")
    jet.penup()
    jet.backward(200)

    def move_up():
        jet.setheading(90)
        jet_y = jet.ycor()
        if jet_y < 140:
            jet.forward(10)
            
    def move_down():
        jet.setheading(270)
        jet_y = jet.ycor()
        if jet_y > -140:
            jet.forward(10)


    # Bind the arrow keys to the functions to move the turtle up and down
    t.onkeypress(move_up, "Up")
    t.onkeypress(move_down, "Down")
    t.onkeypress(move_up, "w")
    t.onkeypress(move_down, "s")
    t.listen()

    #Define missle
    missle = t.Turtle()
    screen.addshape("src/missle.gif")
    missle.shape("src/missle.gif")
    missle.penup()
    missle.setpos(250,0)
    missle.speed(3)
    missle.setheading(180)

    #Define scoreboard
    pen = t.Turtle()
    pen.speed(0)
    pen.shape("square")
    pen.color("white")
    pen.penup()
    pen.hideturtle()
    pen.goto(200,100)
    pen.write("Your score appears here", align="center",font=("candara", 16, "bold"))

    def relocatemissle():
        choices = [1,2,3]
        coinflip = random.choice(choices)
        if coinflip != 1:
            missle.hideturtle()
            ycor = random.randint(-100,100)
            missle.setpos(250,ycor)
            missle.showturtle()
        else:
            missle.hideturtle()
            ycor = jet.ycor()
            missle.setpos(250,ycor)
            missle.showturtle()

    def gameover():
        jet.hideturtle()
        missle.hideturtle()
        pen.clear()
        pen.write("Game Over", align="center",font=("candara", 16, "bold"))
        t.done()


    def check_collision():
        if jet.distance(missle) < 40:
            return True
            
    #Forever loop
    while True:
        missle.forward(10)
        if check_collision():
            gameover()
            break
        if missle.xcor() < -400:
            relocatemissle()
            score = score + 1
            pen.clear()
            pen.write(score, align="center",font=("candara", 16, "bold"))




def noteapp():
    #Initialize scratchpadwindow
    scratchpadwindow = tk.Tk()
    scratchpadwindow.title("ScratchPad")
    scratchpadwindow.geometry("400x400")
    scratchpadwindow['background']='#c7e5fc'
    scratchpadwindow.resizable(True,True)

    global syntax_highlighting_enabled
    global is_on
    #init variables
    syntax_highlighting_enabled = False
    is_on = False

    

    #Define close
    def close():
        scratchpadwindow.destroy()

    #Define Autosave
    def autosave(event=None):
        if is_on is True:
            text_file = open("ScratchPad-Notes.txt", "w")
            filecontent = usertext.get(1.0,tk.END)
            text_file.write(filecontent)
            text_file.close()
    #Define the open function
    def open_file():

        """Open a file for editing."""

        filepath = askopenfilename(

            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]

        )

        if not filepath:

            return

        usertext.delete("1.0", tk.END)

        with open(filepath, mode="r", encoding="utf-8") as input_file:

            text = input_file.read()

            usertext.insert(tk.END, text)

        scratchpadwindow.title(f"ScratchPad - {filepath}")

    #Define save function
    def save_file():

        """Save the current file as a new file."""

        filepath = asksaveasfilename(

            defaultextension=".txt",

            filetypes=[("Text Files", "*.txt"),("Python File", "*.py"), ("All Files", "*.*")],

        )

        if not filepath:

            return

        with open(filepath, mode="w", encoding="utf-8") as output_file:

            text = usertext.get("1.0", tk.END)

            output_file.write(text)

        scratchpadwindow.title(f"ScratchPad - {filepath}")

    #Closecode
    def closecode():
        answer = askyesno(title='Confirmation',message='Do you want to Save before closing?')
        if answer:
            closecode11()
        else:
            scratchpadwindow.destroy()

    def closecode11():
        """Save the current file as a new file."""
        filepath = asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"),("Python File", "*.py"), ("All Files", "*.*")],)
        if not filepath:
            return
        with open(filepath, mode="w", encoding="utf-8") as output_file:
            text = usertext.get("1.0", tk.END)
            output_file.write(text)
        scratchpadwindow.destroy()

    #Define the Customize function
    def customize():
        colors = askcolor(title="Change Textbox colour")
        usertext.configure(bg=colors[1])
        colors2 = askcolor(title="Change Text colour")
        usertext.config(foreground=colors2[1])

    #Define the .grid() sizes
    scratchpadwindow.columnconfigure(0, weight=1)
    scratchpadwindow.rowconfigure(0, weight=1, uniform=1)
    scratchpadwindow.columnconfigure(1, weight=1)
    #Init_Menubar
    menubar = Menu(scratchpadwindow)
    scratchpadwindow.config(menu=menubar)

    #Code for the CodeMode dropdowns
    langs = tk.Menu(menubar, tearoff=False)
    langs.add_command(label="Python (Toggle)",command=lambda: toggle_syntax_highlighting())


    #Add menubar
    menubar.add_command(label="Open",command=open_file)
    menubar.add_command(label="Save",command=save_file)
    menubar.add_cascade(label="CodeMode", menu=langs)
    menubar.add_command(label="Customize",command=customize)
    menubar.add_command(label="Close",command=close)

    #Create Sizegrip
    sg = ttk.Sizegrip(scratchpadwindow)
    sg.grid(row=2,column=3, sticky="SE")

    #Create the tk text
    usertext = tk.Text(scratchpadwindow,undo=True)
    textFont = ("Helvetica", 12)
    usertext.config(font=textFont)
    usertext.grid(row=0, column=0, sticky="nsew",columnspan=3)

    #Add Scrollbar
    sb = tk.Scrollbar(
        scratchpadwindow,
        orient=VERTICAL,
        activebackground="blue",
        troughcolor="blue",
        )
    usertext.config(yscrollcommand=sb.set)
    sb.config(command=usertext.yview)
    sb.grid(row=0,column=3,sticky="NSW")

    #Bind scratchpadwindowclose to savefunction
    scratchpadwindow.protocol("WM_DELETE_scratchpadwindow",closecode)

    #CODE FOR SCALEBAR
    current_value = tk.DoubleVar()
    def slider_changed(event):
        textsize = slider.get()
        size2 = round(textsize)
        usertext.configure(font=("Helvetica", size2))
    style = ttk.Style()
    # Create a new style with a blue background for the slider
    style.configure('Custom.Horizontal.TScale', background='#c7e5fc')
    slider = ttk.Scale(
        scratchpadwindow,
        from_=7,
        to=30,
        orient='horizontal',
        style='Custom.Horizontal.TScale',
        variable=current_value,
        command=slider_changed
    )
    slider.grid(row=2,column=0)
    sliderguide = tk.Label(
        scratchpadwindow,
        text = "Text Size:",
        bg="#c7e5fc",
        fg="grey",
        )
    sliderguide.grid(row=1,column=0)
    #CODE FOR SCALEBAR END

    #CODE FOR FONT DEF FUNCTIONS
    def helvetica():
        helFont = ("Helvetica", round(slider.get()))
        usertext.config(font=helFont)
    def Courier():
        cFont = ("Courier New", round(slider.get()))
        usertext.config(font=cFont)
    def tnr():
        tFont = ("Times New Roman", round(slider.get()))
        usertext.config(font=tFont)

    #CODE FOR FONT ADJUSTMENT
    # Create a new style for the ttk.menubutton
    style = ttk.Style()
    style.configure('Custom.Menubutton', background='#03d3fc', foreground='grey')

    #TEST
    style.map('TMenubutton', background=[('pressed', '#03d3fc'), ('active', '#03d3fc')], foreground=[('pressed', 'white'), ('active', 'white')])
    #TEST

    font = tk.Menu(scratchpadwindow, tearoff=False)
    # Add some items to the menu
    font.add_command(label='Helvetica',command=helvetica )
    font.add_command(label='Courier New',command=Courier )
    font.add_command(label='Times New Roman',command=tnr )
    # Create a menubutton widget
    fontmenu = ttk.Menubutton(scratchpadwindow, menu=font, text='Adjust Font')
    fontmenu.grid(row=2, column=1, sticky="NSEW")


    fontguide = tk.Label(
        scratchpadwindow,
        text = "Font:",
        bg="#c7e5fc",
        fg="grey",
        )
    fontguide.grid(row=1,column=1)
    #CODE FOR FONT ADJUSTMENT END

    #CODE FOR AUTOSAVE
    # Keep track of the button state on/off

    # Define our switch function
    def switch():
        global is_on
        # Determine is on or off
        if is_on:
            on_button.config(text="Disabled")
            on_button.config(bg="#0044b3")
            is_on = False
        else:
            on_button.config(text="Enabled")
            on_button.config(bg="#99c0ff")
            is_on = True

    # Create A Button
    on_button = tk.Button(
        scratchpadwindow,
        bd = 0,
        command = switch,
        text="Disabled",
        bg="#0044b3",
        fg="white",
        )
    on_button.grid(row=2,column=2,padx=5)
    saveguide = tk.Label(
        scratchpadwindow,
        text = "AutoSave:",
        bg="#c7e5fc",
        fg="grey",
        )
    saveguide.grid(row=1,column=2)
    #CODE FOR AUTOSAVE END

    #CODE FOR AUTOSAVE2
    usertext.bind('<Any-KeyRelease>', autosave)
    #CODE FOR AUTOSAVE2 END


    #Bind the CodeEditor
    # Extended the keywords dictionary to include built-in functions.
    keywords = {k: 'orange' for k in keyword.kwlist}
    keywords['print'] = 'orange'
    keywords['input'] = 'orange'
    keywords['int'] = 'orange'
    keywords['bin'] = 'orange'
    keywords['exec'] = 'orange'
    keywords['float'] = 'orange'
    keywords['True'] = 'orange'
    keywords['id'] = 'orange'
    keywords['len'] = 'orange'
    keywords['range'] = 'orange'

    #Define colours
    syntax_colors = {
        'comment': 'grey',
        'string': 'green',
        'keyword': 'orange',
        'number': 'blue',
    }


    #define syntax coloring
    def tag_keywords(event):
        for keyword, color in keywords.items():
            start = "1.0"
            while True:
                pos = usertext.search(r'\m{}\M'.format(keyword), start, stopindex=tk.END, regexp=True)
                if not pos:
                    break
                end = f"{pos}+{len(keyword)}c"
                usertext.tag_add("keyword", pos, end)
                start = end        
            usertext.tag_config("keyword", foreground=syntax_colors['keyword'])

    def tag_comments(event):
        usertext.tag_configure("comment", foreground=syntax_colors['comment'])
        start = "1.0"
        while True:
            start = usertext.search("#", start, stopindex=tk.END)
            if not start:
                break
            end = usertext.search("\n", start, stopindex=tk.END)
            if not end:
                end = tk.END
            usertext.tag_add("comment", start, end)
            start = end

    def tag_strings(event):
        usertext.tag_configure("string", foreground=syntax_colors['string'])
        start = "1.0"
        while True:
            start = usertext.search(r'[rR]?[bB]?"[^"\\]*(\\.[^"\\]*)*"', start, stopindex=tk.END, regexp=True)
            if not start:
                break
            end = usertext.search('"', start+"+1c", stopindex=tk.END, regexp=True)
            if not end:
                end = tk.END
            usertext.tag_add("string", start, end+"+1c")
            start = end

        start = "1.0"
        while True:
            start = usertext.search(r"[rR]?[bB]?'[^'\\]*(\\.[^'\\]*)*'", start, stopindex=tk.END, regexp=True)
            if not start:
                break
            end = usertext.search("'", start+"+1c", stopindex=tk.END, regexp=True)
            if not end:
                end = tk.END
            usertext.tag_add("string", start, end+"+1c")
            start = end

    def tag_numbers(event):
        usertext.tag_configure("number", foreground=syntax_colors['number'])
        text_string = usertext.get("1.0", tk.END)
        for match in re.finditer(r"\b\d+\b", text_string):
            start, end = match.span()
            usertext.tag_add("number", f"1.0 + {start} chars", f"1.0 + {end} chars")


    def tag_all(event=None):
        tag_keywords(event)
        tag_numbers(event)  # tag numbers
        tag_comments(event)  # comments should be tagged middle
        tag_strings(event)



    def toggle_syntax_highlighting():
        global syntax_highlighting_enabled

        # Toggle the state of the syntax highlighting toggle.
        syntax_highlighting_enabled = not syntax_highlighting_enabled

        # If syntax highlighting is enabled, highlight the text in the text box.
        # Otherwise, un-highlight the text in the text box.
        if syntax_highlighting_enabled:
            usertext.bind('<Any-KeyRelease>', tag_all)
        else:
            tags = usertext.tag_names()
            # Remove all the tags from the text box.
            for tag in tags:
                usertext.tag_remove(tag, "1.0", "end")
            usertext.unbind('<Any-KeyRelease>')
    #Mainloop
    scratchpadwindow.mainloop()









#Define HNTech logo
logofile= tk.PhotoImage(file='src/logo3.png')
logofilelabel= Label(image=logofile)

logofilebutton= tk.Button(window, image=logofile, command=hntech,
borderwidth=0,highlightthickness = 0,bd = 0,bg = "#02569C",activebackground = "#02569C")

logofilebutton.place(x=805,y=6)

#Define date
date = dt.datetime.now()
# Create Label to display the Date
label = tk.Label(window, text=f"{date:%A, %B %d, \n %Y}",font=('Arial Rounded MT Bold', 15, 'bold'),
                 foreground='#006eff',background='#02569C')
label.place(x=150,y=100)

#FUNC: BATTERY
def batterypercentage(text="Battery: "):
    # returns a tuple
    battery = psutil.sensors_battery()
    newtext = text + str(battery.percent) + "%"
    batterytext.config(text=newtext)
    batterytext.after(1000, batterypercentage)
#FUNC: BATTERY.END


#Define battery percentage
batterytext = tk.Label(
    fg="white",
    bg="#27B6F5",
    text="Battery:",
    font=('Arial Rounded MT Bold',16, 'bold'),
    )
batterytext.place(x=820,y=570)
batterypercentage()

#Add Canvas
C = tk.Canvas(window, bg="white", height=140, width=1000)
C.place(x=0,y=350)

#define email send
def email():
    emailwin = tk.Toplevel()
    rec = tk.Entry(emailwin,width=30)
    rec.pack()
    rec.insert(0,"Reciever@gmail.com")
    sub = tk.Entry(emailwin,width=30)
    sub.pack()
    sub.insert(0,"Email Subject")
    content = tk.Text(emailwin,width=30,height=15)
    content.pack()

    def sendemail():
        yag = yagmail.SMTP("emailclient.micros@gmail.com", password="QwertyUIOP123", smtp_ssl=False)
        yag.send(
            to= rec.get(),
            subject= sub.get(),
            contents=content.get(1.0,tk.END), 
        )
    
    send = tk.Button(emailwin,text="-------Send-------",command=sendemail)
    send.pack()


    

#Buttons
calcfile= tk.PhotoImage(file='src/calc.png')
calcfilelabel= tk.Label(image=calcfile)
calcfilebutton= tk.Button(window, image=calcfile, command=calculator,
borderwidth=0,highlightthickness = 0,bd = 0,bg = "White",activebackground = "White")
calcfilebutton.place(x=100,y=360)

notefile= tk.PhotoImage(file='src/note.png')
notefilelabel= tk.Label(image=notefile)
notefilebutton= tk.Button(window, image=notefile, command=noteapp,
borderwidth=0,highlightthickness = 0,bd = 0,bg = "White",activebackground = "White")
notefilebutton.place(x=250,y=363)

gamefile= tk.PhotoImage(file='src/game.png')
gamefilelabel= tk.Label(image=gamefile)
gamefilebutton= tk.Button(window, image=gamefile, command=playagame,
borderwidth=0,highlightthickness = 0,bd = 0,bg = "White",activebackground = "White")
gamefilebutton.place(x=400,y=365)

mailfile= tk.PhotoImage(file='src/mail.png')
mailfilelabel= tk.Label(image=mailfile)
mailfilebutton= tk.Button(window, image=mailfile, command=email,
borderwidth=0,highlightthickness = 0,bd = 0,bg = "White",activebackground = "White")
mailfilebutton.place(x=550,y=363)

webfile= tk.PhotoImage(file='src/web.png')
webfilelabel= tk.Label(image=webfile)
webfilebutton= tk.Button(window, image=webfile,
borderwidth=0,highlightthickness = 0,bd = 0,bg = "White",activebackground = "White")
webfilebutton.place(x=700,y=363)


#Mainloop
window.mainloop()



os.system('pause')