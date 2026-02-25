# Note: MDEditor Python file uses ttkbootstrap for GUI rendering
# The exe uses pure Tkinter
# I was too lazy to recompile the Py file!

# Update: I have recompiled EXE, old version of MDEditor is lost forever :( {tbh no one is sad lol}

from tkinter import *
from tkinter import font, filedialog
from tkinter import messagebox as mbox
from markdown2 import Markdown
from tkhtmlview import HTMLLabel
import ttkbootstrap as tb

def closewindow():
        leave = mbox.askyesno("Confirmation","Are you sure you want to quit?")
        if leave:
            root.destroy()
        else:
            pass
        
message ='''
Welcome to the Markdown Editor. This is used to write documentation for
your programs in an .md file. .md files have formatting options such as
the examples above. You can therefore write easy to follow documentation
for your users. \n\n
'''
class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.myfont = font.Font(family="Helvetica", size=14)
        self.init_window()

    def init_window(self):
        self.master.title("Markdown (.md) Editor")
        self.pack(fill=BOTH, expand=1)
        self.inputeditor = Text(self, width="1", font=self.myfont,wrap=WORD)
        self.inputeditor.pack(fill=BOTH, expand=1, side=LEFT)
        self.outputbox = HTMLLabel(
            self, width="1", background="white", html="<h3>Markdown preview appears here</h3>")
        self.outputbox.pack(fill=BOTH, expand=1, side=RIGHT)
        self.outputbox.fit_height()
        self.inputeditor.bind("<<Modified>>", self.onInputChange)
        self.mainmenu = Menu(self,tearoff=False)
        self.filemenu = Menu(self.mainmenu,tearoff=False)
        self.filemenu.add_command(label="Open", command=self.openfile)
        self.filemenu.add_command(label="Save as", command=self.savefile)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=closewindow)
        self.mainmenu.add_cascade(label="Options", menu=self.filemenu)
        self.master.config(menu=self.mainmenu)

        self.inputeditor.insert(END,"## Heading\n\n")
        self.inputeditor.insert(END,"**Bold**\n\n")
        self.inputeditor.insert(END,"*Italic*\n\n")
        self.inputeditor.insert(END,"`Code`\n\n")
        self.inputeditor.insert(END,"[Link](https://hntechsoftware.github.io)\n\n")
        self.inputeditor.insert(END,message)
        
        
    def onInputChange(self, event):
        self.inputeditor.edit_modified(0)
        md2html = Markdown()
        # self.outputbox.set_html(md2html.convert(self.inputeditor.get("1.0" , END)))
        markdownText = self.inputeditor.get("1.0", END)
        html = md2html.convert(markdownText)
        self.outputbox.set_html(html)

    def openfile(self):
        openfilename = filedialog.askopenfilename(filetypes=(("Markdown File", "*.md , *.mdown , *.markdown"),
                                                            ("Text File", "*.txt"),
                                                            ("All Files", "*.*")))
        if openfilename:
            try:
                self.inputeditor.delete(1.0, END)
                self.inputeditor.insert(END, open(openfilename).read())
            except:
                # print("Cannot Open File!")
                mbox.showerror("Error Opening Selected File" , "Oops!, The file you selected : {} can not be opened!".format(openfilename))
    
    def savefile(self):
        filedata = self.inputeditor.get("1.0" , END)
        savefilename = filedialog.asksaveasfilename(filetypes = (("Markdown File", "*.md"),
                                                                  ("Text File", "*.txt")) , title="Save Markdown File")
        if savefilename:
            try:
                f = open(savefilename , "w")
                f.write(filedata)
            except:
                mbox.showerror("Error Saving File" , "Oops!, The File : {} can not be saved!".format(savefilename))

root = tb.Window()
root.geometry("1400x1200")
app = Window(root)
app.mainloop()
