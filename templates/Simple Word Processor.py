import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askopenfilename, asksaveasfilename
root = tk.Tk()

greeting = tk.Label(
    root,
    text="Simple Word Processor",
    foreground="white",
    background="black"
    )
root.minsize(800,500)

Font = ("Arial",10)

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

    root.title(f"WordWrapper by HNTech - {filepath}")

def save_file():

    title = doctitle.get()

    """Save the current file as a new file."""

    filepath = asksaveasfilename(

        defaultextension=".txt",

        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],

        initialfile = title

    )

    if not filepath:

        return

    with open(filepath, mode="w", encoding="utf-8") as output_file:

        text = usertext.get("1.0", tk.END)

        output_file.write(text)

    root.title(f"Simple Text Editor - {filepath}")

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=6)
root.rowconfigure(1, weight=1)
doctitle = tk.Entry(root,width=100)
root.title('WordWrapper by HNTech')
greeting.grid(row=0,column=1)
usertext = tk.Text(root)
usertext.configure(font = Font)
usertext.grid(column=1,row=2)
doctitle.grid(column=1,row=1)

doctitle.insert(0,"Untitled Document")

savefile = tk.Button(
    root,
    text="Save As",
    width=9,
    height=2,
    bg="white",
    fg="black",
    command=save_file
)
savefile.grid(row=1,column=0)

openfile = tk.Button(
    root,
    text="Open New",
    width=9,
    height=2,
    bg="white",
    fg="black",
    command=open_file
)
openfile.grid(row=2,column=0)






root.mainloop()
