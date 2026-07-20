import os
import tkinter as tk
import tkterminal
root = tk.Tk()
terminal = tkterminal.Terminal(pady=5, padx=5)
terminal.pack(expand=True, fill='both')
root.mainloop()

os.system('pause')