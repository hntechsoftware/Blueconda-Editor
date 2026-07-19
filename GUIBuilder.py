import tkinter as tk
import ttkbootstrap as tb
from tkinter import ttk
from ttkbootstrap.dialogs.dialogs import FontDialog
from tkinter.colorchooser import askcolor

# ----------------------------------------------------------------------------
# Shared look & feel constants
# ----------------------------------------------------------------------------
BG_PAGE = "#f4f6f9"
BG_CARD = "#ffffff"
FG_HEADER = "#2c3e50"
FONT_HEADER = ("Segoe UI", 18, "bold")
FONT_SECTION = ("Segoe UI", 11, "bold")
FONT_BODY = ("Segoe UI", 10)
FONT_HINT = ("Segoe UI", 9)
FONT_CODE = ("Cascadia Code", 10)

DEFAULT_FONT_DICT = {
    "family": "TkDefaultFont",
    "size": 12,
    "weight": "normal",
    "slant": "roman",
    "underline": 0,
    "overstrike": 0,
}

root = tb.Window(themename="cerculean")
root.title("GUIBuilder")
root.geometry("1500x1000")
root.minsize(1150, 750)

nbk = tb.Notebook(root, bootstyle="success")


# ----------------------------------------------------------------------------
# Small helpers used by every tab so the layout stays consistent everywhere
# ----------------------------------------------------------------------------
def make_font_tuple(font_dict):
    """Turn a font.Font().actual() style dict into a plain tkinter font tuple."""
    family = font_dict.get("family", "TkDefaultFont")
    try:
        size = int(font_dict.get("size", 12))
    except (TypeError, ValueError):
        size = 12
    styles = []
    if str(font_dict.get("weight", "normal")).lower() == "bold":
        styles.append("bold")
    if str(font_dict.get("slant", "roman")).lower() == "italic":
        styles.append("italic")
    if int(font_dict.get("underline", 0) or 0):
        styles.append("underline")
    if int(font_dict.get("overstrike", 0) or 0):
        styles.append("overstrike")
    if styles:
        return (family, size, " ".join(styles))
    return (family, size)


def pick_font(parent_widget, font_state):
    """Open the FontDialog, apply the result to parent_widget and update
    font_state (a dict) in place. Returns True if a font was chosen."""
    fd = FontDialog(parent=root)
    fd.show()
    if fd.result is None:
        return False
    parent_widget.config(font=fd.result)
    font_state.update(fd.result.actual())
    return True


def pick_colors(widget):
    colors = askcolor(title="Change Text Colour")
    if colors[1]:
        widget.configure(foreground=colors[1])
    colors2 = askcolor(title="Change Background Colour")
    if colors2[1]:
        widget.config(background=colors2[1])


def build_tab_shell(parent_frame, title):
    """Creates the common page header + two-column (controls / preview) shell
    that every tab uses, and returns (controls_frame, preview_frame)."""
    container = tk.Frame(parent_frame, bg=BG_PAGE)
    container.pack(fill=tk.BOTH, expand=True)

    tk.Label(container, text=title, font=FONT_HEADER, bg=BG_PAGE, fg=FG_HEADER).pack(
        anchor="w", padx=25, pady=(20, 15)
    )

    body = tk.Frame(container, bg=BG_PAGE)
    body.pack(fill=tk.BOTH, expand=True, padx=25, pady=(0, 25))
    body.columnconfigure(0, weight=3, uniform="col")
    body.columnconfigure(1, weight=2, uniform="col")
    body.rowconfigure(0, weight=1)

    controls = tb.Labelframe(body, text="  Settings  ", bootstyle="primary", padding=20)
    controls.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
    controls.columnconfigure(0, weight=1)

    right = tk.Frame(body, bg=BG_PAGE)
    right.grid(row=0, column=1, sticky="nsew")
    right.rowconfigure(0, weight=3)
    right.rowconfigure(1, weight=2)
    right.columnconfigure(0, weight=1)

    preview = tb.Labelframe(right, text="  Preview  ", bootstyle="success", padding=20)
    preview.grid(row=0, column=0, sticky="nsew", pady=(0, 15))

    code_frame = tb.Labelframe(right, text="  Generated Code  ", bootstyle="secondary", padding=15)
    code_frame.grid(row=1, column=0, sticky="nsew")

    return controls, preview, code_frame


def add_code_box(code_frame, height=10):
    box = tk.Text(code_frame, height=height, autostyle=False, borderwidth=1,
                   relief="solid", font=FONT_CODE, wrap="none")
    box.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

    btn_row = tk.Frame(code_frame, bg=BG_CARD)
    btn_row.pack(fill=tk.X)

    def copy_code():
        root.clipboard_clear()
        root.clipboard_append(box.get(1.0, tk.END).strip())

    return box, btn_row, copy_code


# ----------------------------------------------------------------------------
# create frames (one per tab)
# ----------------------------------------------------------------------------
frame1 = tk.Frame(nbk, bg=BG_PAGE)
frame2 = tk.Frame(nbk, bg=BG_PAGE)
frame3 = tk.Frame(nbk, bg=BG_PAGE)
frame4 = tk.Frame(nbk, bg=BG_PAGE)
frame5 = tk.Frame(nbk, bg=BG_PAGE)
frame6 = tk.Frame(nbk, bg=BG_PAGE)
frame7 = tk.Frame(nbk, bg=BG_PAGE)
frame8 = tk.Frame(nbk, bg=BG_PAGE)

# =============================================================================
# Frame 1: Label
# =============================================================================
controls1, preview1, code_area1 = build_tab_shell(frame1, "Label Builder")

testlabel = tk.Label(preview1, text="Label Looks like This", autostyle=False, font=("TkDefaultFont", 12))
testlabel.pack(expand=True)

currentfont = dict(DEFAULT_FONT_DICT)

r = 0
tk.Label(controls1, text="Text", font=FONT_SECTION).grid(row=r, column=0, sticky="w"); r += 1
text_row = tk.Frame(controls1); text_row.grid(row=r, column=0, sticky="ew", pady=(4, 15)); r += 1
text_row.columnconfigure(0, weight=1)
TextEntry = tk.Entry(text_row)
TextEntry.grid(row=0, column=0, sticky="ew", padx=(0, 8))
TextEntry.insert(0, "Enter Text Here")


def changelabeltext():
    testlabel.config(text=TextEntry.get())


tb.Button(text_row, text="Apply", command=changelabeltext, bootstyle="secondary").grid(row=0, column=1)

tk.Label(controls1, text="Font Size", font=FONT_SECTION).grid(row=r, column=0, sticky="w"); r += 1
tk.Label(controls1, text="Drag to resize live, or pick an exact font below.",
         font=FONT_HINT, fg="#7f8c8d").grid(row=r, column=0, sticky="w", pady=(0, 6)); r += 1

current_value = tk.DoubleVar(value=12)


def slider_changed(event=None):
    currentfont["size"] = round(sizeslider.get())
    testlabel.configure(font=make_font_tuple(currentfont))


sizeslider = ttk.Scale(controls1, from_=8, to=48, orient="horizontal",
                        variable=current_value, command=slider_changed)
sizeslider.grid(row=r, column=0, sticky="ew", pady=(0, 15)); r += 1

btn_row1 = tk.Frame(controls1); btn_row1.grid(row=r, column=0, sticky="ew", pady=(0, 15)); r += 1
btn_row1.columnconfigure((0, 1), weight=1)


def fontforlabel():
    if pick_font(testlabel, currentfont):
        current_value.set(currentfont["size"])


def colorforlabel():
    pick_colors(testlabel)


tb.Button(btn_row1, text="Choose Font", command=fontforlabel).grid(row=0, column=0, sticky="ew", padx=(0, 5))
tb.Button(btn_row1, text="Choose Colors", command=colorforlabel).grid(row=0, column=1, sticky="ew", padx=(5, 0))

codebox1, codebtns1, copy1 = add_code_box(code_area1)


def generatelabelcode():
    labelfont = make_font_tuple(currentfont)
    labelfg = testlabel.cget("foreground") or "black"
    labelbg = testlabel.cget("background") or "SystemButtonFace"
    labeltext = testlabel.cget("text")
    codeforlabel = f'''my_label = tk.Label(
    master=root, text="{labeltext}",
    foreground="{labelfg}", background="{labelbg}",
    font={labelfont})
my_label.pack()'''
    codebox1.delete(1.0, tk.END)
    codebox1.insert(1.0, codeforlabel)


tb.Button(codebtns1, text="Generate Code", command=generatelabelcode, bootstyle="success").pack(side="left")
tb.Button(codebtns1, text="Copy", command=copy1, bootstyle="secondary-outline").pack(side="left", padx=(8, 0))

# =============================================================================
# Frame 2: Button
# =============================================================================
controls2, preview2, code_area2 = build_tab_shell(frame2, "Button Builder")

testbutton = tk.Button(preview2, text="Click Me!", autostyle=False, font=("TkDefaultFont", 12))
testbutton.pack(expand=True)

currentfont_btn = dict(DEFAULT_FONT_DICT)

r = 0
tk.Label(controls2, text="Text", font=FONT_SECTION).grid(row=r, column=0, sticky="w"); r += 1
btn_text_row = tk.Frame(controls2); btn_text_row.grid(row=r, column=0, sticky="ew", pady=(4, 15)); r += 1
btn_text_row.columnconfigure(0, weight=1)
btnTextEntry = tk.Entry(btn_text_row)
btnTextEntry.grid(row=0, column=0, sticky="ew", padx=(0, 8))
btnTextEntry.insert(0, "Enter Text Here")


def changebuttontext():
    testbutton.config(text=btnTextEntry.get())


tb.Button(btn_text_row, text="Apply", command=changebuttontext, bootstyle="secondary").grid(row=0, column=1)

tk.Label(controls2, text="Font Size", font=FONT_SECTION).grid(row=r, column=0, sticky="w"); r += 1
tk.Label(controls2, text="Drag to resize live, or pick an exact font below.",
         font=FONT_HINT, fg="#7f8c8d").grid(row=r, column=0, sticky="w", pady=(0, 6)); r += 1

current_value_btn = tk.DoubleVar(value=12)


def btnslider_changed(event=None):
    currentfont_btn["size"] = round(btnsizeslider.get())
    testbutton.configure(font=make_font_tuple(currentfont_btn))


btnsizeslider = ttk.Scale(controls2, from_=8, to=48, orient="horizontal",
                           variable=current_value_btn, command=btnslider_changed)
btnsizeslider.grid(row=r, column=0, sticky="ew", pady=(0, 15)); r += 1

btn_row2 = tk.Frame(controls2); btn_row2.grid(row=r, column=0, sticky="ew", pady=(0, 15)); r += 1
btn_row2.columnconfigure((0, 1), weight=1)


def fontforbutton():
    if pick_font(testbutton, currentfont_btn):
        current_value_btn.set(currentfont_btn["size"])


def colorforbutton():
    pick_colors(testbutton)


tb.Button(btn_row2, text="Choose Font", command=fontforbutton).grid(row=0, column=0, sticky="ew", padx=(0, 5))
tb.Button(btn_row2, text="Choose Colors", command=colorforbutton).grid(row=0, column=1, sticky="ew", padx=(5, 0))

tk.Label(controls2, text="Dimensions", font=FONT_SECTION).grid(row=r, column=0, sticky="w"); r += 1
dim_row = tk.Frame(controls2); dim_row.grid(row=r, column=0, sticky="ew", pady=(4, 15)); r += 1
tk.Label(dim_row, text="Width").grid(row=0, column=0, sticky="w")
btnWidthEntry = tk.Entry(dim_row, width=6)
btnWidthEntry.grid(row=0, column=1, padx=(6, 20))
btnWidthEntry.insert(0, "10")
tk.Label(dim_row, text="Height").grid(row=0, column=2, sticky="w")
btnHeightEntry = tk.Entry(dim_row, width=6)
btnHeightEntry.grid(row=0, column=3, padx=(6, 20))
btnHeightEntry.insert(0, "2")


def applybtnsize():
    try:
        testbutton.config(width=int(btnWidthEntry.get()), height=int(btnHeightEntry.get()))
    except ValueError:
        pass


tb.Button(dim_row, text="Apply", command=applybtnsize, bootstyle="secondary").grid(row=0, column=4)

codebox2, codebtns2, copy2 = add_code_box(code_area2)


def generatebuttoncode():
    btnfont = make_font_tuple(currentfont_btn)
    btnfg = testbutton.cget("foreground") or "black"
    btnbg = testbutton.cget("background") or "SystemButtonFace"
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


tb.Button(codebtns2, text="Generate Code", command=generatebuttoncode, bootstyle="success").pack(side="left")
tb.Button(codebtns2, text="Copy", command=copy2, bootstyle="secondary-outline").pack(side="left", padx=(8, 0))

# =============================================================================
# Frame 3: Slider
# =============================================================================
controls3, preview3, code_area3 = build_tab_shell(frame3, "Slider Builder")

slider_preview_wrap = tk.Frame(preview3)
slider_preview_wrap.pack(expand=True)
testslider = ttk.Scale(slider_preview_wrap, from_=0, to=100, orient="horizontal", length=250)
testslider.pack(pady=(0, 10))
sliderlabel = tk.Label(slider_preview_wrap, text="Value: 0", font=("Segoe UI", 12))
sliderlabel.pack()


def updateslider(val):
    sliderlabel.config(text=f"Value: {int(float(val))}")


testslider.config(command=updateslider)

slider_orient = tk.StringVar(value="horizontal")
slider_from = tk.DoubleVar(value=0)
slider_to = tk.DoubleVar(value=100)
slider_length = tk.IntVar(value=200)

r = 0
tk.Label(controls3, text="Range", font=FONT_SECTION).grid(row=r, column=0, sticky="w"); r += 1
range_row = tk.Frame(controls3); range_row.grid(row=r, column=0, sticky="ew", pady=(4, 15)); r += 1
tk.Label(range_row, text="From").grid(row=0, column=0, sticky="w")
tk.Entry(range_row, width=8, textvariable=slider_from).grid(row=0, column=1, padx=(6, 20))
tk.Label(range_row, text="To").grid(row=0, column=2, sticky="w")
tk.Entry(range_row, width=8, textvariable=slider_to).grid(row=0, column=3, padx=(6, 0))

tk.Label(controls3, text="Length (px)", font=FONT_SECTION).grid(row=r, column=0, sticky="w"); r += 1
tk.Entry(controls3, width=10, textvariable=slider_length).grid(row=r, column=0, sticky="w", pady=(4, 15)); r += 1

tk.Label(controls3, text="Orientation", font=FONT_SECTION).grid(row=r, column=0, sticky="w"); r += 1
orient_row = tk.Frame(controls3); orient_row.grid(row=r, column=0, sticky="w", pady=(4, 15)); r += 1
tk.Radiobutton(orient_row, text="Horizontal", variable=slider_orient, value="horizontal").pack(side="left")
tk.Radiobutton(orient_row, text="Vertical", variable=slider_orient, value="vertical").pack(side="left", padx=(15, 0))


def applysliderconfig():
    testslider.config(from_=slider_from.get(), to=slider_to.get(),
                       orient=slider_orient.get(), length=slider_length.get())


tb.Button(controls3, text="Apply Config", command=applysliderconfig, bootstyle="secondary").grid(
    row=r, column=0, sticky="w", pady=(0, 15)
); r += 1

codebox3, codebtns3, copy3 = add_code_box(code_area3)


def generateslidercode():
    codeforslder = f'''my_slider = ttk.Scale(
    master=root, from_={slider_from.get()}, to={slider_to.get()},
    orient='{slider_orient.get()}', length={slider_length.get()},
    command=slider_callback)
my_slider.pack()'''
    codebox3.delete(1.0, tk.END)
    codebox3.insert(1.0, codeforslder)


tb.Button(codebtns3, text="Generate Code", command=generateslidercode, bootstyle="success").pack(side="left")
tb.Button(codebtns3, text="Copy", command=copy3, bootstyle="secondary-outline").pack(side="left", padx=(8, 0))

# =============================================================================
# Frame 4: Entry
# =============================================================================
controls4, preview4, code_area4 = build_tab_shell(frame4, "Entry Builder")

testentry = tk.Entry(preview4, autostyle=False, font=("TkDefaultFont", 12))
testentry.insert(0, "Sample Entry")
testentry.pack(expand=True)

currentfont_entry = dict(DEFAULT_FONT_DICT)

r = 0
tk.Label(controls4, text="Placeholder Text", font=FONT_SECTION).grid(row=r, column=0, sticky="w"); r += 1
entry_text_row = tk.Frame(controls4); entry_text_row.grid(row=r, column=0, sticky="ew", pady=(4, 15)); r += 1
entry_text_row.columnconfigure(0, weight=1)
entryTextEntry = tk.Entry(entry_text_row)
entryTextEntry.grid(row=0, column=0, sticky="ew", padx=(0, 8))
entryTextEntry.insert(0, "Placeholder")


def changeentrytext():
    testentry.delete(0, tk.END)
    testentry.insert(0, entryTextEntry.get())


tb.Button(entry_text_row, text="Apply", command=changeentrytext, bootstyle="secondary").grid(row=0, column=1)

tk.Label(controls4, text="Width", font=FONT_SECTION).grid(row=r, column=0, sticky="w"); r += 1
width_row4 = tk.Frame(controls4); width_row4.grid(row=r, column=0, sticky="w", pady=(4, 15)); r += 1
entryWidthEntry = tk.Entry(width_row4, width=8)
entryWidthEntry.pack(side="left")
entryWidthEntry.insert(0, "20")


def applyentrywidth():
    try:
        testentry.config(width=int(entryWidthEntry.get()))
    except ValueError:
        pass


tb.Button(width_row4, text="Apply", command=applyentrywidth, bootstyle="secondary").pack(side="left", padx=(8, 0))

btn_row4 = tk.Frame(controls4); btn_row4.grid(row=r, column=0, sticky="ew", pady=(0, 15)); r += 1
btn_row4.columnconfigure((0, 1), weight=1)


def fontforentry():
    pick_font(testentry, currentfont_entry)


def colorforentry():
    pick_colors(testentry)


tb.Button(btn_row4, text="Choose Font", command=fontforentry).grid(row=0, column=0, sticky="ew", padx=(0, 5))
tb.Button(btn_row4, text="Choose Colors", command=colorforentry).grid(row=0, column=1, sticky="ew", padx=(5, 0))

codebox4, codebtns4, copy4 = add_code_box(code_area4)


def generateentrycode():
    entryfont = make_font_tuple(currentfont_entry)
    entryfg = testentry.cget("foreground") or "black"
    entrybg = testentry.cget("background") or "SystemButtonFace"
    entrywidth = testentry.cget("width")
    codeforentry = f'''my_entry = tk.Entry(
    master=root, width={entrywidth},
    foreground="{entryfg}", background="{entrybg}",
    font={entryfont})
my_entry.pack()'''
    codebox4.delete(1.0, tk.END)
    codebox4.insert(1.0, codeforentry)


tb.Button(codebtns4, text="Generate Code", command=generateentrycode, bootstyle="success").pack(side="left")
tb.Button(codebtns4, text="Copy", command=copy4, bootstyle="secondary-outline").pack(side="left", padx=(8, 0))

# =============================================================================
# Frame 5: Scrollbar
# =============================================================================
controls5, preview5, code_area5 = build_tab_shell(frame5, "Scrollbar Builder")

testscrollbar = tk.Scrollbar(preview5, orient="vertical")
testscrollbar.pack(expand=True, fill="y", pady=20)

scrollbar_orient = tk.StringVar(value="vertical")

r = 0
tk.Label(controls5, text="Orientation", font=FONT_SECTION).grid(row=r, column=0, sticky="w"); r += 1
orient_row5 = tk.Frame(controls5); orient_row5.grid(row=r, column=0, sticky="w", pady=(4, 15)); r += 1
tk.Radiobutton(orient_row5, text="Vertical", variable=scrollbar_orient, value="vertical").pack(side="left")
tk.Radiobutton(orient_row5, text="Horizontal", variable=scrollbar_orient, value="horizontal").pack(
    side="left", padx=(15, 0)
)


def applyscrollbarconfig():
    testscrollbar.config(orient=scrollbar_orient.get())


tb.Button(controls5, text="Apply Config", command=applyscrollbarconfig, bootstyle="secondary").grid(
    row=r, column=0, sticky="w", pady=(0, 15)
); r += 1

codebox5, codebtns5, copy5 = add_code_box(code_area5, height=12)


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


tb.Button(codebtns5, text="Generate Code", command=generatescrollbarcode, bootstyle="success").pack(side="left")
tb.Button(codebtns5, text="Copy", command=copy5, bootstyle="secondary-outline").pack(side="left", padx=(8, 0))

# =============================================================================
# Frame 6: Text
# =============================================================================
controls6, preview6, code_area6 = build_tab_shell(frame6, "Text Widget Builder")

testtext = tk.Text(preview6, width=30, height=10, autostyle=False, font=("TkDefaultFont", 12))
testtext.insert(1.0, "This is a Text widget.\nYou can type multiple lines here.")
testtext.pack(expand=True)

currentfont_text = dict(DEFAULT_FONT_DICT)

r = 0
tk.Label(controls6, text="Dimensions", font=FONT_SECTION).grid(row=r, column=0, sticky="w"); r += 1
dim_row6 = tk.Frame(controls6); dim_row6.grid(row=r, column=0, sticky="ew", pady=(4, 15)); r += 1
tk.Label(dim_row6, text="Width").grid(row=0, column=0, sticky="w")
textWidthEntry = tk.Entry(dim_row6, width=6)
textWidthEntry.grid(row=0, column=1, padx=(6, 20))
textWidthEntry.insert(0, "30")
tk.Label(dim_row6, text="Height").grid(row=0, column=2, sticky="w")
textHeightEntry = tk.Entry(dim_row6, width=6)
textHeightEntry.grid(row=0, column=3, padx=(6, 20))
textHeightEntry.insert(0, "10")


def applytextsize():
    try:
        testtext.config(width=int(textWidthEntry.get()), height=int(textHeightEntry.get()))
    except ValueError:
        pass


tb.Button(dim_row6, text="Apply", command=applytextsize, bootstyle="secondary").grid(row=0, column=4)

btn_row6 = tk.Frame(controls6); btn_row6.grid(row=r, column=0, sticky="ew", pady=(0, 15)); r += 1
btn_row6.columnconfigure((0, 1), weight=1)


def fontfortext():
    pick_font(testtext, currentfont_text)


def colorfortext():
    pick_colors(testtext)


tb.Button(btn_row6, text="Choose Font", command=fontfortext).grid(row=0, column=0, sticky="ew", padx=(0, 5))
tb.Button(btn_row6, text="Choose Colors", command=colorfortext).grid(row=0, column=1, sticky="ew", padx=(5, 0))

codebox6, codebtns6, copy6 = add_code_box(code_area6)


def generatetextcode():
    textfont = make_font_tuple(currentfont_text)
    textfg = testtext.cget("foreground") or "black"
    textbg = testtext.cget("background") or "SystemButtonFace"
    textwidth = testtext.cget("width")
    textheight = testtext.cget("height")
    codefortext = f'''my_text = tk.Text(
    master=root, width={textwidth}, height={textheight},
    foreground="{textfg}", background="{textbg}",
    font={textfont})
my_text.pack()'''
    codebox6.delete(1.0, tk.END)
    codebox6.insert(1.0, codefortext)


tb.Button(codebtns6, text="Generate Code", command=generatetextcode, bootstyle="success").pack(side="left")
tb.Button(codebtns6, text="Copy", command=copy6, bootstyle="secondary-outline").pack(side="left", padx=(8, 0))

# =============================================================================
# Frame 7: Menu
# =============================================================================
controls7, preview7, code_area7 = build_tab_shell(frame7, "Menu Builder")

tk.Label(preview7, text="File   Edit   Help", font=("Segoe UI", 14), bg="#e9ecef",
         relief="raised", padx=25, pady=12).pack(expand=True)

tk.Label(controls7, text="About", font=FONT_SECTION).grid(row=0, column=0, sticky="w")
tk.Label(controls7, text="Menus are created programmatically, not previewed live. "
                          "Click below to generate a ready-to-use File/Edit menu "
                          "structure you can adapt.",
         font=FONT_BODY, wraplength=340, justify="left").grid(row=1, column=0, sticky="w", pady=(6, 20))

codebox7, codebtns7, copy7 = add_code_box(code_area7, height=14)


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


tb.Button(codebtns7, text="Generate Code", command=generatemenucode, bootstyle="success").pack(side="left")
tb.Button(codebtns7, text="Copy", command=copy7, bootstyle="secondary-outline").pack(side="left", padx=(8, 0))

# =============================================================================
# Frame 8: How to use
# =============================================================================
help_container = tk.Frame(frame8, bg=BG_PAGE)
help_container.pack(fill=tk.BOTH, expand=True)

tk.Label(help_container, text="How to Use GUIBuilder", font=FONT_HEADER, bg=BG_PAGE,
         fg=FG_HEADER).pack(anchor="w", padx=25, pady=(20, 15))

help_card = tb.Labelframe(help_container, text="  Guide  ", bootstyle="primary", padding=25)
help_card.pack(fill=tk.BOTH, expand=True, padx=25, pady=(0, 25))

instruction_text = """1. Select a widget tab (Label, Button, Slider, etc.)

2. Customize the widget properties:
   - Change text, font, and colors
   - Adjust size using sliders or the width/height fields
   - Configure widget-specific options

3. Click "Generate Code" to get the Python code

4. Copy the generated code into your tkinter application

5. Make sure to:
   - Import tkinter as tk at the top of your file
   - Create a root window: root = tk.Tk()
   - Place the generated widget code in your application
   - Run root.mainloop() at the end

Tips
-----
- The preview updates live as you make changes
- Font dialogs and color pickers provide visual selection
- Each widget shows the most commonly used properties
- Generated code uses standard tkinter syntax

Example workflow
-----------------
1. Customize a Label with your desired text and style
2. Generate and copy the code
3. Create more widgets in other tabs
4. Combine all generated code in your application
"""

instruction_textbox = tk.Text(help_card, font=FONT_BODY, wrap="word", borderwidth=0,
                               highlightthickness=0, bg=BG_CARD)
instruction_textbox.insert(1.0, instruction_text)
instruction_textbox.config(state="disabled")
instruction_textbox.pack(fill="both", expand=True)

# ----------------------------------------------------------------------------
# add frames to notebook
# ----------------------------------------------------------------------------
nbk.add(frame1, text="  Label  ")
nbk.add(frame2, text="  Button  ")
nbk.add(frame3, text="  Slider  ")
nbk.add(frame4, text="  Entry  ")
nbk.add(frame5, text="  Scrollbar  ")
nbk.add(frame6, text="  Text  ")
nbk.add(frame7, text="  Menu  ")
nbk.add(frame8, text="  How to Use  ")

nbk.select(0)
nbk.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

root.mainloop()