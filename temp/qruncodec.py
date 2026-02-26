import os
import tkinter as tk
from tkinter import ttk, messagebox, colorchooser, filedialog

def show_message():
    messagebox.showinfo("Info", "This is a messagebox demo")

def choose_color():
    colorchooser.askcolor(title="Choose a color")

def open_file():
    filedialog.askopenfilename(title="Open File")

def main():
    root = tk.Tk()
    root.title("Comprehensive Tkinter Widgets Demo")
    root.geometry("900x700")

    # ---------------------------
    # Menu Bar
    # ---------------------------
    menubar = tk.Menu(root)
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Open", command=open_file)
    file_menu.add_separator()
    file_menu.add_command(label="Quit", command=root.quit)
    menubar.add_cascade(label="File", menu=file_menu)

    help_menu = tk.Menu(menubar, tearoff=0)
    help_menu.add_command(label="About", command=show_message)
    menubar.add_cascade(label="Help", menu=help_menu)

    root.config(menu=menubar)

    # Main Notebook
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    # ---------------------------
    # Basic Widgets Tab
    # ---------------------------
    tab_basic = ttk.Frame(notebook)
    notebook.add(tab_basic, text="Basic Widgets")

    ttk.Label(tab_basic, text="Label").pack(anchor="w", pady=4)
    ttk.Button(tab_basic, text="Button").pack(anchor="w", pady=4)

    cb_var = tk.BooleanVar()
    ttk.Checkbutton(tab_basic, text="Checkbutton", variable=cb_var).pack(anchor="w", pady=4)

    rb_var = tk.StringVar(value="1")
    ttk.Radiobutton(tab_basic, text="Option 1", variable=rb_var, value="1").pack(anchor="w")
    ttk.Radiobutton(tab_basic, text="Option 2", variable=rb_var, value="2").pack(anchor="w", pady=4)

    ttk.Label(tab_basic, text="Entry").pack(anchor="w")
    ttk.Entry(tab_basic).pack(anchor="w", pady=4)

    ttk.Label(tab_basic, text="Password Entry").pack(anchor="w")
    ttk.Entry(tab_basic, show="*").pack(anchor="w", pady=4)

    ttk.Label(tab_basic, text="Spinbox").pack(anchor="w")
    tk.Spinbox(tab_basic, from_=0, to=100).pack(anchor="w", pady=4)

    ttk.Label(tab_basic, text="Scale").pack(anchor="w")
    ttk.Scale(tab_basic, from_=0, to=100, orient="horizontal").pack(anchor="w", pady=4)

    ttk.Label(tab_basic, text="OptionMenu").pack(anchor="w")
    opt_var = tk.StringVar(value="Option A")
    tk.OptionMenu(tab_basic, opt_var, "Option A", "Option B", "Option C").pack(anchor="w", pady=4)

    ttk.Label(tab_basic, text="Progressbar").pack(anchor="w")
    ttk.Progressbar(tab_basic, length=200, mode="indeterminate").pack(anchor="w", pady=4)

    # ---------------------------
    # Text & List Widgets Tab
    # ---------------------------
    tab_lists = ttk.Frame(notebook)
    notebook.add(tab_lists, text="Text & Lists")

    ttk.Label(tab_lists, text="Text Widget").pack(anchor="w")
    text_widget = tk.Text(tab_lists, height=5, width=50)
    text_widget.pack(anchor="w", pady=4)

    ttk.Label(tab_lists, text="Listbox").pack(anchor="w")
    listbox = tk.Listbox(tab_lists, height=5)
    for item in ["Alpha", "Bravo", "Charlie", "Delta"]:
        listbox.insert(tk.END, item)
    listbox.pack(anchor="w", pady=4)

    ttk.Label(tab_lists, text="Combobox").pack(anchor="w")
    ttk.Combobox(tab_lists, values=["Apple", "Banana", "Cherry"]).pack(anchor="w", pady=4)

    # ---------------------------
    # Canvas & Drawing Tab
    # ---------------------------
    tab_canvas = ttk.Frame(notebook)
    notebook.add(tab_canvas, text="Canvas")

    canvas = tk.Canvas(tab_canvas, width=400, height=300, bg="white")
    canvas.pack(pady=10)

    canvas.create_rectangle(20, 20, 120, 80, outline="black", width=2)
    canvas.create_oval(150, 20, 250, 120, outline="blue", width=2)
    canvas.create_line(20, 150, 250, 150, fill="green", width=3)
    canvas.create_text(200, 200, text="Canvas Text Example", anchor="center")

    # ---------------------------
    # Advanced Widgets Tab
    # ---------------------------
    tab_advanced = ttk.Frame(notebook)
    notebook.add(tab_advanced, text="Advanced Widgets")

    ttk.Label(tab_advanced, text="Treeview").pack(anchor="w")
    tree = ttk.Treeview(tab_advanced, columns=("col1", "col2"), show="headings", height=5)
    tree.heading("col1", text="Column 1")
    tree.heading("col2", text="Column 2")
    tree.insert("", "end", values=("Row1-1", "Row1-2"))
    tree.insert("", "end", values=("Row2-1", "Row2-2"))
    tree.pack(anchor="w", pady=4)

    ttk.Label(tab_advanced, text="PanedWindow").pack(anchor="w", pady=4)
    pw = ttk.PanedWindow(tab_advanced, orient="horizontal")
    pw.pack(fill="x", pady=4)

    left = ttk.Frame(pw, width=150, height=100)
    right = ttk.Frame(pw, width=150, height=100)

    pw.add(left)
    pw.add(right)

    ttk.Label(left, text="Left Pane").pack()
    ttk.Label(right, text="Right Pane").pack()

    ttk.Button(tab_advanced, text="Show MessageBox", command=show_message).pack(anchor="w", pady=4)
    ttk.Button(tab_advanced, text="Choose Color", command=choose_color).pack(anchor="w", pady=4)

    # ---------------------------
    # Scrolled Widgets Tab
    # ---------------------------
    tab_scroll = ttk.Frame(notebook)
    notebook.add(tab_scroll, text="Scrollable Widgets")

    canvas_scroll = tk.Canvas(tab_scroll)
    scrollbar = ttk.Scrollbar(tab_scroll, orient="vertical", command=canvas_scroll.yview)
    scroll_frame = ttk.Frame(canvas_scroll)

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas_scroll.configure(scrollregion=canvas_scroll.bbox("all"))
    )

    canvas_scroll.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas_scroll.configure(yscrollcommand=scrollbar.set)

    canvas_scroll.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    for i in range(40):
        ttk.Label(scroll_frame, text=f"Scrollable Label {i+1}").pack(anchor="w", pady=2)

    root.mainloop()

if __name__ == "__main__":
    main()



os.system('pause')