import qrcode as qr
from tkinter import filedialog
import tkinter as tk


def createqr():
    url = entry.get()
    img = qr.make(url)
    saveloc = filedialog.asksavefilename()

window = tk.Tk()
tk.Label(text="Enter Link here: ").pack()
entry = tk.Entry(width=15)
entry.pack()

button = tk.Button(text="Generate QR Code", command=createqr)
button.pack()


window.mainloop()
