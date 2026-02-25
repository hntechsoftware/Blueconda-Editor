import tkinter as tk
import ttkbootstrap as tb
from tkinter import ttk
from ttkbootstrap.dialogs.dialogs import FontDialog
from tkinter.colorchooser import askcolor

root = tb.Window(themename="cerculean")
root.title("GUIBuilder")
root.geometry("1500x1000")

nbk = tb.Notebook(root, bootstyle="success")

# create frames
frame1 = tk.Frame(nbk, width=300, height=600, bg="white")
frame2 = tk.Frame(nbk, width=300, height=600, bg="white")
frame3 = tk.Frame(nbk, width=300, height=600, bg="white")
frame4 = tk.Frame(nbk, width=300, height=600, bg="white")
frame5 = tk.Frame(nbk, width=300, height=600, bg="white")
frame6 = tk.Frame(nbk, width=300, height=600, bg="white")
frame7 = tk.Frame(nbk, width=300, height=600, bg="white")
frame8 = tk.Frame(nbk, width=300, height=600, bg="white")

# Frame 1: Label
frameforlabel = tk.Frame(frame1, width=600, height=700)
testlabel = tk.Label(frameforlabel, text="Label Looks like This", autostyle=False)
testlabel.grid(row=0, column=2, sticky="E")
frameforlabel.grid(row=0, column=2, sticky="E", rowspan=5)

tk.Label(frame1, text="Size:", font=("Arial", 16)).grid(row=0, column=1)
tk.Label(frame1, text="Note: Size slider and font selection should be used independently.", 
         font=("Arial", 10)).grid(row=2, column=1)

currentfont = ("TkDefaultFont", 12)

def fontforlabel():
    fd = FontDialog()
    fd.show()
    testlabel.config(font=fd.result)
    global currentfont
    currentfont = tuple(fd.result)

tb.Button(frame1, text="     Choose Font     ", command=fontforlabel).grid(row=5, column=1, pady=50)

def colorforlabel():
    colors = askcolor(title="Change Text colour")
    if colors[1]:
        testlabel.configure(foreground=colors[1])
    colors2 = askcolor(title="Change Background colour")
    if colors2[1]:
        testlabel.config(background=colors2[1])

tb.Button(frame1, text="    Choose Colors   ", command=colorforlabel).grid(row=6, column=1, pady=10)

def generatelabelcode():
    labelfont = currentfont
    labelfg = testlabel.cget("foreground")
    labelbg = testlabel.cget("background")
    labeltext = testlabel.cget("text")
    codeforlabel = f'''my_label = tk.Label(
    master=root, text="{labeltext}",
    foreground="{labelfg}", background="{labelbg}",
    font={labelfont})
my_label.pack()'''
    codebox1.delete(1.0, tk.END)
    codebox1.insert(1.0, codeforlabel)

def slider_changed(event):
    global currentfont
    textsize = sizeslider.get()
    size2 = round(textsize)
    if currentfont:
        wefont = currentfont[0] if isinstance(currentfont, tuple) else currentfont
        new_font = (wefont, size2)
        testlabel.configure(font=new_font)

current_value = tk.DoubleVar()
style = ttk.Style()
style.configure('Custom.Horizontal.TScale', background='#c7e5fc')
sizeslider = ttk.Scale(frame1, from_=10, to=30, orient='horizontal',
                       variable=current_value, command=slider_changed, length=200)
sizeslider.grid(row=1, column=1, padx=300)

codebox1 = tk.Text(frame1, width=50, height=12, autostyle=False, borderwidth=2, 
                   font=("Cascadia Code", 10))
codebox1.grid(row=9, column=1, pady=10)
tb.Button(frame1, text="    Generate Code   ", command=generatelabelcode).grid(row=10, column=1, pady=0)

def changelabeltext():
    newtext = TextEntry.get()
    testlabel.config(text=newtext)

tb.Button(frame1, text="     Change Text    ", command=changelabeltext).grid(row=8, column=1, pady=0)
TextEntry = tk.Entry(frame1, width=16)
TextEntry.grid(row=7, column=1)
TextEntry.insert(0, "Enter Text Here")

# Frame 2: Button
frameforbutton = tk.Frame(frame2, width=600, height=700)
testbutton = tk.Button(frameforbutton, text="Click Me!", autostyle=False)
testbutton.grid(row=0, column=2, sticky="E", padx=20, pady=20)
frameforbutton.grid(row=0, column=2, sticky="E", rowspan=5)

tk.Label(frame2, text="Size:", font=("Arial", 16)).grid(row=0, column=1)
tk.Label(frame2, text="Note: Size slider and font selection should be used independently.", 
         font=("Arial", 10)).grid(row=2, column=1)

currentfont_btn = ("TkDefaultFont", 12)

def fontforbutton():
    fd = FontDialog()
    fd.show()
    testbutton.config(font=fd.result)
    global currentfont_btn
    currentfont_btn = tuple(fd.result)

tb.Button(frame2, text="     Choose Font     ", command=fontforbutton).grid(row=5, column=1, pady=50)

def colorforbutton():
    colors = askcolor(title="Change Text colour")
    if colors[1]:
        testbutton.configure(foreground=colors[1])
    colors2 = askcolor(title="Change Background colour")
    if colors2[1]:
        testbutton.config(background=colors2[1])

tb.Button(frame2, text="    Choose Colors   ", command=colorforbutton).grid(row=6, column=1, pady=10)

def generatebuttoncode():
    btnfont = currentfont_btn
    btnfg = testbutton.cget("foreground")
    btnbg = testbutton.cget("background")
    btntext = testbutton.cget("text")
    btnwidth = testbutton.cget("width")
    btnheight = testbutton.cget("height")
    codeforbutton = f'''my_button = tk.Button(
    master=root, text="{btntext}",
    foreground="{btnfg}", background="{btnbg}",
    font={btnfont}, width={btnwidth}, height={btnheight},
    command=my_function)
my_button.pack()'''
    codebox2.delete(1.0, tk.END)
    codebox2.insert(1.0, codeforbutton)

def btnslider_changed(event):
    global currentfont_btn
    textsize = btnsizeslider.get()
    size2 = round(textsize)
    if currentfont_btn:
        wefont = currentfont_btn[0] if isinstance(currentfont_btn, tuple) else currentfont_btn
        new_font = (wefont, size2)
        testbutton.configure(font=new_font)

current_value_btn = tk.DoubleVar()
btnsizeslider = ttk.Scale(frame2, from_=10, to=30, orient='horizontal',
                          variable=current_value_btn, command=btnslider_changed, length=200)
btnsizeslider.grid(row=1, column=1, padx=300)

codebox2 = tk.Text(frame2, width=50, height=12, autostyle=False, borderwidth=2, 
                   font=("Cascadia Code", 10))
codebox2.grid(row=9, column=1, pady=10)
tb.Button(frame2, text="    Generate Code   ", command=generatebuttoncode).grid(row=10, column=1, pady=0)

def changebuttontext():
    newtext = btnTextEntry.get()
    testbutton.config(text=newtext)

tb.Button(frame2, text="     Change Text    ", command=changebuttontext).grid(row=8, column=1, pady=0)
btnTextEntry = tk.Entry(frame2, width=16)
btnTextEntry.grid(row=7, column=1)
btnTextEntry.insert(0, "Enter Text Here")

tk.Label(frame2, text="Width:", font=("Arial", 12)).grid(row=11, column=1)
btnWidthEntry = tk.Entry(frame2, width=10)
btnWidthEntry.grid(row=12, column=1)
btnWidthEntry.insert(0, "10")

tk.Label(frame2, text="Height:", font=("Arial", 12)).grid(row=13, column=1)
btnHeightEntry = tk.Entry(frame2, width=10)
btnHeightEntry.grid(row=14, column=1)
btnHeightEntry.insert(0, "2")

def applybtnsize():
    try:
        w = int(btnWidthEntry.get())
        h = int(btnHeightEntry.get())
        testbutton.config(width=w, height=h)
    except:
        pass

tb.Button(frame2, text="   Apply Size   ", command=applybtnsize).grid(row=15, column=1, pady=10)

# Frame 3: Slider
frameforslider = tk.Frame(frame3, width=600, height=700)
testslider = ttk.Scale(frameforslider, from_=0, to=100, orient='horizontal', length=200)
testslider.grid(row=0, column=2, sticky="E", padx=20, pady=20)
sliderlabel = tk.Label(frameforslider, text="Value: 0", font=("Arial", 12))
sliderlabel.grid(row=1, column=2)
frameforslider.grid(row=0, column=2, sticky="E", rowspan=5)

tk.Label(frame3, text="Slider Configuration", font=("Arial", 16)).grid(row=0, column=1)

slider_orient = tk.StringVar(value="horizontal")
slider_from = tk.DoubleVar(value=0)
slider_to = tk.DoubleVar(value=100)
slider_length = tk.IntVar(value=200)

def updateslider(val):
    sliderlabel.config(text=f"Value: {int(float(val))}")

testslider.config(command=updateslider)

tk.Label(frame3, text="From:", font=("Arial", 12)).grid(row=1, column=1, pady=5)
sliderFromEntry = tk.Entry(frame3, width=10, textvariable=slider_from)
sliderFromEntry.grid(row=2, column=1)

tk.Label(frame3, text="To:", font=("Arial", 12)).grid(row=3, column=1, pady=5)
sliderToEntry = tk.Entry(frame3, width=10, textvariable=slider_to)
sliderToEntry.grid(row=4, column=1)

tk.Label(frame3, text="Length:", font=("Arial", 12)).grid(row=5, column=1, pady=5)
sliderLengthEntry = tk.Entry(frame3, width=10, textvariable=slider_length)
sliderLengthEntry.grid(row=6, column=1)

tk.Label(frame3, text="Orientation:", font=("Arial", 12)).grid(row=7, column=1, pady=5)
tk.Radiobutton(frame3, text="Horizontal", variable=slider_orient, value="horizontal").grid(row=8, column=1)
tk.Radiobutton(frame3, text="Vertical", variable=slider_orient, value="vertical").grid(row=9, column=1)

def applysliderconfig():
    testslider.config(from_=slider_from.get(), to=slider_to.get(), 
                      orient=slider_orient.get(), length=slider_length.get())

tb.Button(frame3, text="  Apply Config  ", command=applysliderconfig).grid(row=10, column=1, pady=20)

def generateslidercode():
    codeforslder = f'''my_slider = ttk.Scale(
    master=root, from_={slider_from.get()}, to={slider_to.get()},
    orient='{slider_orient.get()}', length={slider_length.get()},
    command=slider_callback)
my_slider.pack()'''
    codebox3.delete(1.0, tk.END)
    codebox3.insert(1.0, codeforslder)

codebox3 = tk.Text(frame3, width=50, height=12, autostyle=False, borderwidth=2, 
                   font=("Cascadia Code", 10))
codebox3.grid(row=11, column=1, pady=10)
tb.Button(frame3, text="    Generate Code   ", command=generateslidercode).grid(row=12, column=1, pady=0)

# Frame 4: Entry
frameforentry = tk.Frame(frame4, width=600, height=700)
testentry = tk.Entry(frameforentry, autostyle=False)
testentry.insert(0, "Sample Entry")
testentry.grid(row=0, column=2, sticky="E", padx=20, pady=20)
frameforentry.grid(row=0, column=2, sticky="E", rowspan=5)

tk.Label(frame4, text="Entry Configuration", font=("Arial", 16)).grid(row=0, column=1)

currentfont_entry = ("TkDefaultFont", 12)

def fontforentry():
    fd = FontDialog()
    fd.show()
    testentry.config(font=fd.result)
    global currentfont_entry
    currentfont_entry = tuple(fd.result)

tb.Button(frame4, text="     Choose Font     ", command=fontforentry).grid(row=3, column=1, pady=20)

def colorforentry():
    colors = askcolor(title="Change Text colour")
    if colors[1]:
        testentry.configure(foreground=colors[1])
    colors2 = askcolor(title="Change Background colour")
    if colors2[1]:
        testentry.config(background=colors2[1])

tb.Button(frame4, text="    Choose Colors   ", command=colorforentry).grid(row=4, column=1, pady=10)

tk.Label(frame4, text="Width:", font=("Arial", 12)).grid(row=5, column=1)
entryWidthEntry = tk.Entry(frame4, width=10)
entryWidthEntry.grid(row=6, column=1)
entryWidthEntry.insert(0, "20")

def applyentrywidth():
    try:
        w = int(entryWidthEntry.get())
        testentry.config(width=w)
    except:
        pass

tb.Button(frame4, text="   Apply Width   ", command=applyentrywidth).grid(row=7, column=1, pady=10)

tk.Label(frame4, text="Placeholder Text:", font=("Arial", 12)).grid(row=8, column=1)
entryTextEntry = tk.Entry(frame4, width=20)
entryTextEntry.grid(row=9, column=1)
entryTextEntry.insert(0, "Placeholder")

def changeentrytext():
    newtext = entryTextEntry.get()
    testentry.delete(0, tk.END)
    testentry.insert(0, newtext)

tb.Button(frame4, text="   Change Text   ", command=changeentrytext).grid(row=10, column=1, pady=10)

def generateentrycode():
    entryfont = currentfont_entry
    entryfg = testentry.cget("foreground")
    entrybg = testentry.cget("background")
    entrywidth = testentry.cget("width")
    codeforentry = f'''my_entry = tk.Entry(
    master=root, width={entrywidth},
    foreground="{entryfg}", background="{entrybg}",
    font={entryfont})
my_entry.pack()'''
    codebox4.delete(1.0, tk.END)
    codebox4.insert(1.0, codeforentry)

codebox4 = tk.Text(frame4, width=50, height=12, autostyle=False, borderwidth=2, 
                   font=("Cascadia Code", 10))
codebox4.grid(row=11, column=1, pady=10)
tb.Button(frame4, text="    Generate Code   ", command=generateentrycode).grid(row=12, column=1, pady=0)

# Frame 5: Scrollbar
frameforscrollbar = tk.Frame(frame5, width=600, height=700)
testscrollbar = tk.Scrollbar(frameforscrollbar, orient='vertical')
testscrollbar.grid(row=0, column=2, sticky="NS", padx=20, pady=20)
frameforscrollbar.grid(row=0, column=2, sticky="E", rowspan=5)

tk.Label(frame5, text="Scrollbar Configuration", font=("Arial", 16)).grid(row=0, column=1)

scrollbar_orient = tk.StringVar(value="vertical")

tk.Label(frame5, text="Orientation:", font=("Arial", 12)).grid(row=1, column=1, pady=10)
tk.Radiobutton(frame5, text="Vertical", variable=scrollbar_orient, value="vertical").grid(row=2, column=1)
tk.Radiobutton(frame5, text="Horizontal", variable=scrollbar_orient, value="horizontal").grid(row=3, column=1)

def applyscrollbarconfig():
    testscrollbar.config(orient=scrollbar_orient.get())

tb.Button(frame5, text="  Apply Config  ", command=applyscrollbarconfig).grid(row=4, column=1, pady=20)

def generatescrollbarcode():
    codeforscrollbar = f'''my_scrollbar = tk.Scrollbar(
    master=root, orient='{scrollbar_orient.get()}')
my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Attach to a widget (e.g., Text or Listbox)
my_text = tk.Text(root, yscrollcommand=my_scrollbar.set)
my_text.pack()
my_scrollbar.config(command=my_text.yview)'''
    codebox5.delete(1.0, tk.END)
    codebox5.insert(1.0, codeforscrollbar)

codebox5 = tk.Text(frame5, width=50, height=15, autostyle=False, borderwidth=2, 
                   font=("Cascadia Code", 10))
codebox5.grid(row=5, column=1, pady=10)
tb.Button(frame5, text="    Generate Code   ", command=generatescrollbarcode).grid(row=6, column=1, pady=0)

# Frame 6: Text
framefortext = tk.Frame(frame6, width=600, height=700)
testtext = tk.Text(framefortext, width=30, height=10, autostyle=False)
testtext.insert(1.0, "This is a Text widget.\nYou can type multiple lines here.")
testtext.grid(row=0, column=2, sticky="E", padx=20, pady=20)
framefortext.grid(row=0, column=2, sticky="E", rowspan=5)

tk.Label(frame6, text="Text Widget Configuration", font=("Arial", 16)).grid(row=0, column=1)

currentfont_text = ("TkDefaultFont", 12)

def fontfortext():
    fd = FontDialog()
    fd.show()
    testtext.config(font=fd.result)
    global currentfont_text
    currentfont_text = tuple(fd.result)

tb.Button(frame6, text="     Choose Font     ", command=fontfortext).grid(row=2, column=1, pady=20)

def colorfortext():
    colors = askcolor(title="Change Text colour")
    if colors[1]:
        testtext.configure(foreground=colors[1])
    colors2 = askcolor(title="Change Background colour")
    if colors2[1]:
        testtext.config(background=colors2[1])

tb.Button(frame6, text="    Choose Colors   ", command=colorfortext).grid(row=3, column=1, pady=10)

tk.Label(frame6, text="Width:", font=("Arial", 12)).grid(row=4, column=1)
textWidthEntry = tk.Entry(frame6, width=10)
textWidthEntry.grid(row=5, column=1)
textWidthEntry.insert(0, "30")

tk.Label(frame6, text="Height:", font=("Arial", 12)).grid(row=6, column=1)
textHeightEntry = tk.Entry(frame6, width=10)
textHeightEntry.grid(row=7, column=1)
textHeightEntry.insert(0, "10")

def applytextsize():
    try:
        w = int(textWidthEntry.get())
        h = int(textHeightEntry.get())
        testtext.config(width=w, height=h)
    except:
        pass

tb.Button(frame6, text="   Apply Size   ", command=applytextsize).grid(row=8, column=1, pady=10)

def generatetextcode():
    textfont = currentfont_text
    textfg = testtext.cget("foreground")
    textbg = testtext.cget("background")
    textwidth = testtext.cget("width")
    textheight = testtext.cget("height")
    codefortext = f'''my_text = tk.Text(
    master=root, width={textwidth}, height={textheight},
    foreground="{textfg}", background="{textbg}",
    font={textfont})
my_text.pack()'''
    codebox6.delete(1.0, tk.END)
    codebox6.insert(1.0, codefortext)

codebox6 = tk.Text(frame6, width=50, height=12, autostyle=False, borderwidth=2, 
                   font=("Cascadia Code", 10))
codebox6.grid(row=9, column=1, pady=10)
tb.Button(frame6, text="    Generate Code   ", command=generatetextcode).grid(row=10, column=1, pady=0)

# Frame 7: Menu
frameformenu = tk.Frame(frame7, width=600, height=700)
tk.Label(frameformenu, text="Menu Preview:\nFile | Edit | Help", font=("Arial", 14), 
         bg="lightgray", relief="raised", padx=20, pady=10).grid(row=0, column=2)
frameformenu.grid(row=0, column=2, sticky="E", rowspan=5)

tk.Label(frame7, text="Menu Configuration", font=("Arial", 16)).grid(row=0, column=1)
tk.Label(frame7, text="Menus are created programmatically.\nSee the generated code for structure.", 
         font=("Arial", 11), wraplength=300, justify="left").grid(row=1, column=1, pady=20)

def generatemenucode():
    codeformenu = '''# Create menubar
menubar = tk.Menu(root)
root.config(menu=menubar)

# Create File menu
file_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# Create Edit menu
edit_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut", command=cut)
edit_menu.add_command(label="Copy", command=copy)
edit_menu.add_command(label="Paste", command=paste)'''
    codebox7.delete(1.0, tk.END)
    codebox7.insert(1.0, codeformenu)

codebox7 = tk.Text(frame7, width=60, height=20, autostyle=False, borderwidth=2, 
                   font=("Cascadia Code", 10))
codebox7.grid(row=2, column=1, pady=10)
tb.Button(frame7, text="    Generate Code   ", command=generatemenucode).grid(row=3, column=1, pady=10)

# Frame 8: How to use
instruction_text = """
HOW TO USE GUIBUILDER

1. Select a widget tab (Label, Button, Slider, etc.)

2. Customize the widget properties:
   - Change text, font, colors
   - Adjust size using sliders or input fields
   - Configure widget-specific options

3. Click "Generate Code" to get the Python code

4. Copy the generated code into your tkinter application

5. Make sure to:
   - Import tkinter as tk at the top of your file
   - Create a root window: root = tk.Tk()
   - Place the generated widget code in your application
   - Run root.mainloop() at the end

TIPS:
- The preview updates in real-time as you make changes
- Font dialogs and color pickers provide visual selection
- Each widget shows the most commonly used properties
- Generated code uses standard tkinter syntax

EXAMPLE WORKFLOW:
1. Customize a Label with your desired text and style
2. Generate and copy the code
3. Create more widgets in other tabs
4. Combine all generated code in your application
"""

instruction_textbox = tk.Text(frame8, width=80, height=35, font=("Arial", 11), 
                              wrap="word", padx=20, pady=20)
instruction_textbox.insert(1.0, instruction_text)
instruction_textbox.config(state="disabled")
instruction_textbox.pack(expand=True, fill="both", padx=20, pady=20)

# add frames to nbk
nbk.add(frame1, text='  Label   ')
nbk.add(frame2, text='  Button  ')
nbk.add(frame3, text='  Slider  ')
nbk.add(frame4, text='  Entry   ')
nbk.add(frame5, text='  Scrollbar   ')
nbk.add(frame6, text='  Text    ')
nbk.add(frame7, text='  Menu    ')
nbk.add(frame8, text='How to use Widget Code')

nbk.select(0)
nbk.pack(fill=tk.BOTH, expand=True)

root.mainloop()