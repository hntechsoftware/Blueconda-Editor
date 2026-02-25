import ttkbootstrap as tb
import tkinter as tk


 # create the main window
root = tb.Window()

 # disable the window bar
root.overrideredirect(1)

# set trasparency and make the window stay on top
root.attributes('-transparentcolor', 'white', '-topmost', True)

# set the background image
psg = tk.PhotoImage(file='src/Blueconda.png')
tk.Label(root, bg='white', image=psg).pack()

# move the window to center
root.eval('tk::PlaceWindow . Center')

# schedule the window to close after 4 seconds
root.after(2000, root.destroy)

root.mainloop()

