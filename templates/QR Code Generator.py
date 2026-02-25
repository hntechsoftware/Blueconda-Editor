import qrcode as qr
from tkinter import filedialog
import tkinter as tk
import ttkbootstrap as tb


def createqr():
    url = entry.get()
    img = qr.make(url)
    saveloc = filedialog.asksaveasfilename(filetypes=[("Image File", "*.png")])
    savelocation = str(saveloc) + ".png"
    img.save(savelocation)


window = tb.Window(themename="cyborg")
window.resizable(False, False)
window.title("QR")
tk.Label(text="Enter Link here: ").pack()
entry = tk.Entry(width=30)
entry.pack()

button = tk.Button(text="Generate QR Code", command=createqr, width=30)
button.pack()


window.mainloop()

