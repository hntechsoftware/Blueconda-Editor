# Blueconda Source Code - Made with Love by HNTech
# For queries, contact m.hamza.naveed@outlook.com
# (Yes, this code is very ugly I know)



# Import all needed modules (this is a HEFTY list)
import tkinter as tk
from googlesearch import search
import platform
from BCLineNumbers import TkLineNumbers
from tkinter import ttk
from ttkbootstrap.dialogs.colorchooser import ColorChooserDialog
import keyword
import re
from pathlib import Path
import sys
import ast
import builtins
import subprocess
from io import StringIO
from tempfile import NamedTemporaryFile
import threading
from ttkbootstrap.constants import *
from tkinter import filedialog
import time
from tkinter import simpledialog
import os
from tktooltip import ToolTip
from  tkinter import messagebox
import webbrowser
import ttkbootstrap as tb
import psutil
import ast
import random
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import extractbuiltins # Self made file, not a library 
import send2trash
from ttkbootstrap.toast import ToastNotification
import toml
from json import loads
import pywinstyles
import inspect
from markdown import Markdown
from io import StringIO
import google.generativeai as genai
from screeninfo import get_monitors
from autopep8 import fix_code
from chlorophyll import CodeView
import pygments.lexers
from hPyT import maximize_minimize_button
from datetime import date, datetime
import tkinter.font as tkfont
import types
import builtins
import shutil
import tkchart
from importlib import metadata
from urllib.parse import urlparse
import traceback

# Define theme for app
themeblueconda = { # This was redacted later
    "type": "light",
    "colors": {
        "primary": "#4bb1ea",
        "secondary": "#a9b4be",
        "success": "#62b5e6",
        "info": "#225384",
        "warning": "#ff0606",
        "danger": "#17acf4",
        "light": "#eceef1",
        "dark": "#33383e",
        "bg": "#ffffff",
        "fg": "#2ea4e7",
        "selectbg": "#adb5bd",
        "selectfg": "#eeeeee",
        "border": "#a9b4be",
        "inputfg": "#495057",
        "inputbg": "#ffffff",
        "active": "#e5e5e5"
        }
}

def get_diagnostics_info():
    """Gathers environment/system info useful for debugging crash reports."""
    import platform
    import datetime

    lines = []
    lines.append("=== Diagnostics ===")
    lines.append(f"Date/Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"OS: {platform.system()} {platform.release()} ({platform.version()})")
    lines.append(f"Machine: {platform.machine()}")
    lines.append(f"Python Version: {platform.python_version()}")
    lines.append(f"Python Implementation: {platform.python_implementation()}")
    lines.append(f"Tkinter Version: {tk.TkVersion}")

    try:
        import ttkbootstrap
        lines.append(f"ttkbootstrap Version: {ttkbootstrap.__version__}")
    except Exception:
        lines.append("ttkbootstrap Version: Not found / not installed")

    try:
        import friendly_traceback
        lines.append(f"Friendly Version: {friendly_traceback.__version__}")
    except Exception:
        lines.append("Friendly Version: Not found / not installed")

    lines.append(f"Working Directory: {os.getcwd()}")
    lines.append(f"Executable: {sys.executable}")
    lines.append("===================")

    return "\n".join(lines)

def show_fatal_error(exc_type, exc_value, exc_traceback):
    """Displays a Toplevel with the fatal error instead of letting the
    app crash/close silently. Hooked into globally - see setup_crash_handler()."""

    error_text = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    print(error_text)  # still log it to console/terminal for debugging

    error_para = ''' \n\nPlease help us make Blueconda better for everyone by posting an issue on github. Click the button below to do so, and in your issue statement, copy the error message and diagnostics info.\n\n\n If the errors persist, reinstall Blueconda Editor. If you are on a Beta release, revert to a Stable one.\n\n
    '''

    win = tk.Toplevel()
    win.attributes('-topmost', True)
    win.attributes("-alpha", 0.9)
    win.configure(bg=config_data["background"])
    win.title("Fatal Error")
    win.minsize(700, 450)

    label = tk.Label(
        win, text="A Fatal Error Occurred :(",
        font=fontnew, bg=config_data['background'], fg=config_data['textforeground']
    )
    label.pack(pady=10)

    output_text = tb.ScrolledText(win, wrap="word")
    output_text.pack(fill=tk.BOTH, expand=True, padx=10)
    output_text.insert(tk.END, error_text)
    output_text.insert(tk.END, error_para) # Insert helpful info
    output_text.insert(tk.END, get_diagnostics_info() + "\n\n")
    output_text.config(state="disabled")

    btn_frame = tk.Frame(win, bg=config_data['background'])
    btn_frame.pack(fill=tk.BOTH, pady=8)

    tb.Button(
        btn_frame, text="Open Issue on GitHub", style='Link.TButton',
        command=lambda: webbrowser.open_new_tab("https://github.com/hntechsoftware/Blueconda-Editor/issues/new")
    ).pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5)

    tb.Button(
        btn_frame, text="Close App", style='Outline.TButton',
        command=lambda: os._exit(1)  # force-quits immediately, bypassing normal shutdown
    ).pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5)

    pywinstyles.change_header_color(win, color=config_data['background'])
    maximize_minimize_button.hide(win)


def _tk_callback_exception_handler(self, exc_type, exc_value, exc_traceback):
    # Overrides Tk's default report_callback_exception, which normally
    # just prints to console and silently continues. This routes it to
    # our fatal error window instead.
    show_fatal_error(exc_type, exc_value, exc_traceback)


def _sys_exception_handler(exc_type, exc_value, exc_traceback):
    # Catches anything NOT inside a Tkinter callback (e.g. startup code,
    # code running directly in the main thread outside the event loop)
    show_fatal_error(exc_type, exc_value, exc_traceback)


def _thread_exception_handler(args):
    # Catches errors inside threading.Thread targets (e.g. your
    # install_dependencies() background thread) - these are invisible
    # to both of the hooks above.
    show_fatal_error(args.exc_type, args.exc_value, args.exc_traceback)


def setup_crash_handler(root):
    """Call this once, right after creating your main Tk() root window,
    to route all uncaught exceptions app-wide into the fatal error window."""
    tk.Tk.report_callback_exception = _tk_callback_exception_handler
    sys.excepthook = _sys_exception_handler
    threading.excepthook = _thread_exception_handler


# Important vars
file_loaded = False
unsaved_label = None

# Get current theme needed
def extract_toml_table(file_path, table_name):
  """Extracts a specified table from a TOML file and assigns variables.

  Args:
    file_path: The path to the TOML file.
    table_name: The name of the table to extract.

  Returns:
    A dictionary containing the table's key-value pairs.
  """

  with open(file_path, 'r') as f:
    config = toml.load(f)

  if table_name not in config:
    raise ValueError(f"Table '{table_name}' not found in TOML file.")

  table_data = config[table_name]

  # Optionally assign variables here:
  # for key, value in table_data.items():
  #   globals()[key] = value  # Use with caution!

  return table_data

# TOML data stored here
file_path = 'settings/themes.toml'


with open("settings/currenttheme.txt", "r") as t:
    table_name = t.read() # Obtain the necessary theme

global config_data # Dictionary for theme applying
# Only extract the TOML table needed using function above
config_data = extract_toml_table(file_path, table_name) # Used to load themes
# print(config_data) # For debugging purposes

__version__ = "1.0 (Beta)" # Blueconda Version

# Variable to manage Show Welcome Message
is_on = True

textandlineborder = 0 # For UI debugging purposes

#if platform.system() == "Windows":
#    ctypes.windll.shcore.SetProcessDpiAwareness(3)
#else:
#    pass


def build_exe(script_path, AppToLaunch, EnableWait:bool):
    # 1. Setup the Toplevel
    popup = tk.Toplevel()
    popup.title("Install Manager")
    #popup.geometry("600x450")
    
    # This makes the Toplevel "Modal" - it locks the main window
    popup.grab_set() 
    
    label = tk.Label(popup, text="Install Manager", font=("Arial", 10, "bold"))
    label.pack(pady=5)
    label2 = tk.Label(popup, text="Please wait whilst Blueconda does some maintenance (Do not close this window!)", font=("Arial", 6, "bold"))
    label2.pack(pady=5)

    progress = ttk.Progressbar(popup, mode='indeterminate', length=300)
    progress.pack()
    progress.start(10)

    output_text = tk.Text(popup, bg="#1e1e1e", fg="#00ff00", font=("Consolas", 10))
    output_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def run_and_stream(cmd):
        process = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            text=True, 
            shell=True
        )
        
        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
            if line:
                output_text.insert(tk.END, line)
                output_text.see(tk.END)
                
                # CRITICAL: This updates the Toplevel only.
                # The main window is technically 'waiting' for this function to finish.
                popup.update() 
        
        return process.poll()

    # 2. Check for PyInstaller
    output_text.insert(tk.END, "Verifying PyInstaller...\n")
    popup.update()
    
    # Try to get version
    check = subprocess.run([sys.executable, "-m", "PyInstaller", "--version"], 
                           capture_output=True, shell=True)

    if check.returncode != 0:
        output_text.insert(tk.END, "PyInstaller not found. Installing...\n")
        run_and_stream([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 3. Build the EXE
    script_dir = os.path.dirname(os.path.abspath(script_path))
    build_cmd = [
        sys.executable, "-m", "PyInstaller", 
        "--onefile", 
        "--clean",
        "--noconsole",
        "--distpath", script_dir, 
        script_path,
    ]
    
    output_text.insert(tk.END, f"\nStarting Build...\n")
    result = run_and_stream(build_cmd)

    if result == 0: # Success
        
        def close_exe_routine():
            output_text.insert(tk.END, "\nSUCCESS: EXE created in script directory.")
            # Re-enable the main window once closed
            btn = tk.Button(popup, bg="red",fg="white", text="CLOSE", command=popup.destroy)
            btn.pack(pady=5)
            progress.stop()
            # Launch the sript after the exe build finished
            newprocess = subprocess.Popen([f"{AppToLaunch}"])
            if EnableWait:
                newprocess.wait()
        # Using a wrapper function bc of common Race Hazard issues
        # with both compiler and exe trying to access same file at once
        popup.after(1200, close_exe_routine)
        # Edit, I found the race hazard was a wasted rabbit hole, the bug was elsewhere
    else:
        output_text.insert(tk.END, "\nERROR: Build failed.")



# Declare the theme
window = tb.Window(themename=f"{config_data['themename']}")
window.state("zoomed")
window.title(f"Blueconda Editor {__version__}")

# Setup crash handler
setup_crash_handler(window)

for m in get_monitors():
    if m.is_primary:
        screen_width = m.width
        screen_height = m.height

window.geometry(f"{screen_width}x{screen_height}")
# make the title bar the same color as window
pywinstyles.change_header_color(window, color=config_data['background'])  

window.attributes("-alpha", 1) # Set default window opacity (Can be changed in settings menu)

# function for toplevel scaling
def scalewindow(width, height):
    return str(round((width/2560)*screen_width)) + "x" + str(round((height/1440)*screen_height))

# Get main icon
window.iconbitmap("src/Bluecondaicon.ico")
window.iconphoto(True, tk.PhotoImage(file="src/Bluecondalogo2.png"))

window.configure(bg=config_data['background'])
sys.setrecursionlimit(10000) # Prevent errors

# Define grid geometry manager row/column weightage
window.rowconfigure(0,weight=0)
window.rowconfigure(1,weight=1)
window.columnconfigure(0,weight=0)
window.columnconfigure(1,weight=1)
window.columnconfigure(2,weight=0)
window.rowconfigure(2,weight=0)

# menubar Frame
C = tk.Frame(width=1500,height=600)
C.grid(row=1,column=0,columnspan=5)

C.config(background=config_data['background'])

def documentationopen(): # Self explanatory
    webbrowser.open("https://hntech.gitbook.io/blueconda-documentation", autoraise=True)

def websiteopen(): # Self explanatory
    webbrowser.open("https://hntechsoftware.github.io/blueconda", autoraise=True)

#DANGEROUS TEST REIGON STR

def compilerrun():
    code = usertext.get("1.0", tk.END)

    output_dir = ""
    with open("temp/currentfile.txt", "r", encoding="utf-8") as f:
        output_dir = f.read().strip()

    # Check if output_dir is a file path
    if os.path.isfile(output_dir):
        # Extract directory from the file path
        output_dir, _ = os.path.split(output_dir)

    with open("temp/pyarchiver.py", "w") as f:
        f.write(code)

    try:
        # Use the extracted directory if it's a file path, otherwise use the provided path
        subprocess.run(["pyinstaller", "--onefile", "temp/pyarchiver.py", "-d", output_dir], check=True)

        exe_file = os.path.join(output_dir, "pyarchiver.exe")
        subprocess.Popen(exe_file)

        while True:
            if not os.path.exists(exe_file):
                print("EXE closed, deleting...")
                os.remove("temp_code.spec")
                os.remove(f"dist/{exe_file}")
                break
            time.sleep(0.5)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", "Compilation failed: " + str(e))
    del(code)


#DANGEROUS TEST REIGON END

# Function invoked when window closed, to show warning message
def closecode():
    answer = messagebox.askyesno(title='Confirmation',
                      message='Are you sure that you want to quit? Any unsaved changes will be lost.\n\nYES to quit, NO to cancel.')
    if answer:
        with open("temp/currentfile.txt","r", encoding="utf-8") as Atlantis:
            components = Atlantis.read()
            Atlantis.close()
        if components == "":
            window.destroy()
            return
        with open("temp/currentfile.txt","w", encoding="utf-8") as cat:
            cat.write("")
            cat.close()
        with open('temp/mostrecentfile.txt','w',encoding='utf-8') as casio:
            casio.write(components)
            casio.close()
            del(components)
        window.destroy()
window.protocol("WM_DELETE_WINDOW",closecode)

def newline():
    usertext.insert(tk.END,"\n")


# In the below function is the first mention of a Toplevel. It is a subwindow.
# There are many subwindows for Blueconda. There is a general code I use for all 
# subwindows as specified here:
# This doesn't include the Install manager (thats more utilarian than usage-oriented)
#
#    win = tk.Toplevel()                            Declare Window
#    win.attributes('-topmost', True)               Set Window on top
#    win.attributes("-alpha", 0.9)                  Make Window Transluscent
#    win.geometry("Width x Height")                 Set Size (Omitted for some)
#    win.configure(bg=config_data["background"])    Change bg based of theme (Omitted for some)
#    win.title("Title")                             Give Window a title
#
#   All code for Window goes here...
#
#    pywinstyles.change_header_color(win, color=config_data['background'])  Change top bar color
#    maximize_minimize_button.hide(win)                                     Hide the max/- buttons (keep X)
#


def aboutapp():
    aboutwin = tk.Toplevel()                            
    aboutwin.attributes('-topmost', True)               
    aboutwin.attributes("-alpha", 0.9)                  
    # aboutwin.geometry("600x600")                 
    aboutwin.configure(bg=config_data["background"])    
    aboutwin.title("About")     

    aboutwin.bclogo = tk.PhotoImage(file="src/biglogo.png")
    aboutwin.bclogoresized = aboutwin.bclogo.subsample(2,2)
    labele = tk.Label(aboutwin,image=aboutwin.bclogoresized)
    labele.grid(row=0, column=0, rowspan=4, padx=0, pady=10)
    tk.Label(aboutwin, text="Blueconda", font=("Cascadia Code SemiBold", 25)).grid(row=0, column=1, padx=0)
    tk.Label(aboutwin, text=f"Built by HNTech, V{__version__}\n(github: hntechsoftware)", font=("Cascadia Code SemiLight", 11)).grid(row=1, column=1, padx=0)
    tk.Label(aboutwin, text=f"Python Version {sys.version.split()[0]}", font=("Cascadia Code SemiLight", 11)).grid(row=2, column=1, padx=0)
    tk.Label(aboutwin, text=f"Tkinter Version {tk.TkVersion}", font=("Cascadia Code SemiLight", 11)).grid(row=3, column=1, padx=0)
    tk.Label(aboutwin, text="Blueconda is released under the MIT License. (See: License)", font=("Cascadia Code SemiLight", 11)).grid(row=4, column=0, padx=0, pady=12, columnspan=2)

    

    pywinstyles.change_header_color(aboutwin, color=config_data['background']) 
    maximize_minimize_button.hide(aboutwin)                                    


def loadtemplate(usertext):
  """
  Loads a template from a listbox selection in a separate window.
  """
  def on_listbox_select(event):
    """
    Handles listbox selection and inserts the chosen template content.
    """
    selected_item = listbox.get(tk.ANCHOR)
    if selected_item:
      template_path = os.path.join(folder_path, selected_item)
      with open(template_path, 'r', encoding="utf-8") as file:
        file_content = file.read()
      newline()
      usertext.insert(tk.INSERT, file_content)
      tag_all()  # Assuming tag_all function exists for styling
      template_window.destroy()  # Close the template window

  def delalltemplates():
    confirmation = messagebox.askyesno(
        "Delete ALL Templates",
        "Are you sure you want to delete all templates?\n(You can restore them from the Recycle Bin)."
    )
    if confirmation:
      for filename in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, filename)):
          send2trash.send2trash(os.path.join(folder_path, filename))
          # Send2trash sends it to recycle bin instead of permanently deleting it
    template_window.destroy()

  # Create the template selection window
  template_window = tk.Toplevel(usertext)
  template_window.attributes('-topmost', True)
  template_window.attributes("-alpha", 0.9)
  template_window.title("Select Template")



  # Set folder path for templates
  folder_path = "templates"

  # Listbox to display template names
  listbox = tk.Listbox(template_window)
  tk.Label(template_window, text="Select A Template to Insert:").pack(fill=tk.X)
  listbox.pack(fill=tk.BOTH, expand=True)

  tk.Button(template_window, text="Delete All Templates", command=delalltemplates).pack(fill=tk.X, expand=True)
  # Get a list of .py files from the templates directory
  template_files = [f for f in os.listdir(folder_path) if f.endswith(".py")]

  # Add template names to the listbox
  for filename in template_files:
    listbox.insert(tk.END, filename)

  # Bind listbox selection event
  listbox.bind("<<ListboxSelect>>", on_listbox_select)

  # Display the template selection window
  template_window.grab_set()  # Make the template window modal (prevents interaction with main window)
  template_window.wait_window()  # Wait for the window to close before continuing

  pywinstyles.change_header_color(template_window, color=config_data['background'])
  maximize_minimize_button.hide(template_window)
    

def  installpythoncompiler(url="https://www.python.org/downloads/windows/"):
  """
  Downloads the latest Python installer for Windows from the provided URL and attempts to run it.

  **WARNING**: Downloading and running executables from the internet can be risky. 
             It's generally recommended to download installers from official sources and then run them manually.

  Args:
      url (str, optional): Base URL of the Python downloads page (defaults to https://www.python.org/downloads/windows/).
  """

  # Get the latest Python installer download page
  response = requests.get(url)

  # Check for successful download
  if response.status_code == 200:
    # Parse the HTML content to potentially find the latest installer link (risky and not recommended)
    # This part is for demonstration purposes only and might require adjustments based on website structure
    soup = BeautifulSoup(response.content, features="lxml")
    links = soup.findAll("a", href=lambda href: href and href.endswith(".exe"))  # Find links ending with .exe

    # Assuming the first link is the latest installer (risky assumption)
    if links:
      latest_link = urljoin(url, links[0]["href"])
      print(f"Downloading latest Python installer: {latest_link}")

      # Download the installer
      installer_response = requests.get(latest_link, stream=True)

      if installer_response.status_code == 200:
        file_name = latest_link.split("/")[-1]

        # Download and save the installer (risky)
        with open(file_name, "wb") as f:
          for chunk in installer_response.iter_content(chunk_size=1024 * 1024):
            if chunk:
              f.write(chunk)
        print(f"Downloaded Python installer: {file_name}")

        # Attempt to run the installer (risky)
        # **WARNING**: This might have security implications and unintended consequences.
        os.startfile(file_name)
      else:
        print(f"Failed to download installer! Status code: {installer_response.status_code}")
    else:
      print(f"No installer link found on downloads page: {url}")
  else:
    print(f"Failed to download downloads page! Status code: {response.status_code}")

def pythoninstallwindow():
    pywin = tk.Toplevel()
    pywin.attributes('-topmost', True)
    pywin.attributes("-alpha", 0.9)
    pywin.title("Install Latest Python Release")
    pywin.geometry(scalewindow(600, 400))
    tk.Label(pywin, font=fontnew, text="Install Python").pack()
    tk.Label(pywin, text="This system will download the latest Python\nrelease and install it to your system.").pack()
    tk.Label(pywin, text="\n\nInstalling Python means installing the compiler\nthat allows you to run Python scripts.").pack()
    tk.Button(pywin, text="Start", command=installpythoncompiler).pack(fill=tk.X, expand=True, padx=10)
    pywinstyles.change_header_color(pywin, color=config_data['background'])
    maximize_minimize_button.hide(pywin)


def get_greeting(): # simple function to retrieve appropriate greeting
    # Get the current hour (24-hour format)
    current_hour = datetime.now().hour
    
    # Determine the time of day based on the hour
    if 5 <= current_hour < 12:
        return "Good Morning"
    elif 12 <= current_hour < 17:
        return "Good Afternoon"
    elif 17 <= current_hour < 21:
        return "Good Evening"
    else:
        return "Good Night"

# Set this so that the greeting window is destroyed when button is clicked
def invokebuttoncommand(command):
    wscreen.destroy() # destroy welcome window
    # Invoke command of whatever button was pressed (argument passed)
    if command == "recentfile":
        recentfile()
    elif command == "documentation":
        documentationopen()
    elif command == "pythoninstall":
        pythoninstallwindow()

def welcomescreen():
    global wscreen
    with open("settings/showwelcomemessage.txt","r",encoding="utf-8") as op:
        choice = op.read()
        if choice == "Y": # Deploy welcome screen if setting selected
              
            time.sleep(2)
            wscreen = tk.Toplevel()
            wscreen.attributes("-alpha", 0.9)
            wscreen.geometry(f"{str(round((600/2560)*screen_width))}x{str(round((500/1440)*screen_height))}")
            wscreen.configure(bg="white")
            wscreen.title("Get Started!")
            def type_effect(label, text): # Cool type effect because why not
                if text:
                    label.config(text=label['text'] + text[0])
                    label.after(100, lambda: type_effect(label, text[1:]))
            welcomefont = ("Lucida Sans Typewriter",16,"bold")
            label = tk.Label(wscreen, text="", font=welcomefont,bg="white", autostyle=False)
            label.pack()
            username = os.getenv('username') # get username
            type_effect(label, f"{get_greeting()},\n{username}.") # Greeting + username with type effect
            # Buttons for quick commands
            # passed through the invokebuttoncommand function as a gateway to close window before invoking command
            # Elements packed after 2000 milliseconds because thats the time taken for initial message to show
            ttexbutton = tk.Button(wscreen,text="Open Most Recent File",font=welcomefont,bg="white",fg="blue",
                                   autostyle=False, command= lambda: invokebuttoncommand("recentfile"), relief=tk.FLAT)
            wscreen.after(2000, lambda: ttexbutton.pack())
            quickbutton = tk.Button(wscreen,text="Install Python Compiler",font=welcomefont,bg="white",fg="blue",
                                    autostyle=False, command= lambda: invokebuttoncommand("pythoninstall"), relief=tk.FLAT)
            wscreen.after(2000, lambda: quickbutton.pack())
            exbutton = tk.Button(wscreen,text="Read the Documentation",font=welcomefont,bg="white",fg="blue",
                                   autostyle=False, command= lambda: invokebuttoncommand("documentation"), relief=tk.FLAT)
            wscreen.after(2000, lambda: exbutton.pack())
            # Just so that the user knows they can close this
            disablelabel = tk.Label(wscreen,bg="white", fg="black",font=fontnew,autostyle=False,text="You can disable this welcome\nmessage in Settings.")
            wscreen.after(2000, lambda: disablelabel.pack())
        else:
            pass
    
'''
logoimage = tk.PhotoImage(file="src/Bluecondalogo2.png")
logo = tk.Label(C, image=logoimage)
logo.grid(row=0,column=0)

logolabel = tk.Label(C,text="Blueconda",fg="blue",bg="white")
logolabel.grid(row=0,column=1,padx=8)

logolabel.config(background=config_data["background"])
logo.configure(background=config_data["background"])
'''

def resize(): # To make scrollbar work properly
    usertext.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=usertext.yview)
    window.after(1000, resize)

frame = tk.Frame(window,bg="white", highlightbackground="black", highlightthickness=textandlineborder)
frame.grid_columnconfigure(0, weight=1)
frame.grid_rowconfigure(0, weight=1)

#--RowColumn------------------------------------------------------------------
def update_row_column():
    # Get the current cursor position
    cursor_index = usertext.index('insert')

    # Convert the cursor index to row and column numbers
    row = int(cursor_index.split('.')[0]) 
    column = int(cursor_index.split('.')[1]) + 1

    # Update the label with the current row and column number
    indicat.config(text=f"Line {row}, Column {column}")
    window.after(10,update_row_column)
#--RowColumn------------------------------------------------------------------

#---
def ShouldIAutocomplete(): #TODO fix this
    """This is The Code to see if Blueconda should disable Autocomplete (for strings and comments)."""
    text_widget = usertext
    line_number =  usertext.index(tk.INSERT).split(".")[0]
    line_start = text_widget.index("%s.0" % line_number)

    # tags = text_widget.tag_names(line_start)

    tags = text_widget.tag_names("insert-1c")
    for item in tags:
        if item == "string" or item == "comment":
            return False
        return True
    

doApiComplete = False

def auto_duplicate_quotes_and_parentheses(usertext): # for convenience 
    def on_key_press(event):
        global doApiComplete
        if event.char == '"':
            usertext.insert(tk.INSERT, '"')
            usertext.mark_set(tk.INSERT, "insert-1c")
        elif event.char == "(":
            current_pos = usertext.index(tk.INSERT)  # Get the current cursor position
            usertext.insert(tk.INSERT, ")")  # Insert ")"
            usertext.mark_set(tk.INSERT, current_pos)  # Restore the cursor position
        elif event.char == "'":
            usertext.insert(tk.INSERT, "'")
            usertext.mark_set(tk.INSERT, "insert-1c")
        elif event.char == "[":
            usertext.insert(tk.INSERT, "]")
            usertext.mark_set(tk.INSERT, "insert-1c")
        elif event.char == "{":
            usertext.insert(tk.INSERT, "}")
            usertext.mark_set(tk.INSERT, "insert-1c")
        elif event.char == ".":
            doApiComplete = True
            on_key(event, DotTyped=True, SpaceTyped=False)
            
        elif event.char == " ":
            doApiComplete = False
            on_key(event, DotTyped=False, SpaceTyped=True)
        else:
            #if ShouldIAutocomplete():
            on_key(event, DotTyped=False, SpaceTyped=False) # for autocomplete function

    usertext.bind('<Key>', on_key_press)
#---
window.columnconfigure(0, weight=1)
window.rowconfigure(1, weight=5, uniform=1)
window.columnconfigure(1, weight=1)
#Codebox



# select line function to go here
def select_linemain(line_number): 
    usertext.tag_remove("sel", 1.0, tk.END)
    start_index = usertext.index(f"{line_number}.0")
    end_index = usertext.index(f"{line_number}.end")
    usertext.tag_add("sel", start_index, end_index)


# Main Code Editor
usertext = tb.Text(frame,width=95,height=24,borderwidth=textandlineborder,wrap="none",autostyle=False,undo=True)
usertext.grid(row=0,column=0,sticky="NSEW",pady=0,padx=0)
fontnew=("Segoe UI SemiBold",12,"bold")
usertext.configure(font=fontnew)
# logolabel.configure(font=fontnew)
usertext.configure(bg=config_data['background'])
usertext.configure(fg=config_data['textforeground'])
usertext.config(insertbackground="grey")

# Override text selection colors
usertext.tag_configure("sel", background="", selectbackground="#75dee3", selectforeground="white")

#Code for undo/redo functions
usertext.configure(autoseparators=True)
usertext.configure(maxundo=-1)

auto_duplicate_quotes_and_parentheses(usertext)

def find_todos_fixmes(text_widget):
    content = text_widget.get("1.0", tk.END)
    todos_fixmes = []
    for line in content.splitlines():
        if "TODO" in line or "FIXME" in line:
            todos_fixmes.append(line.strip())
    return todos_fixmes

def todofixmewindow(event=None):
    global todo_fixme_index

    # tf stands for Todo/Fixme, not whatever
    # else you were thinking you bad minded person!
    tfwin = tk.Toplevel()
    tfwin.attributes('-topmost', True)
    tfwin.attributes("-alpha", 0.9)
    tfwin.title("TODOs/FIXMEs")
    tfentry = tk.Entry(tfwin, width=60)
    tfentry.grid(row=0, column=0, columnspan=2)

    todos_fixmes = find_todos_fixmes(usertext)
    todo_fixme_index = 0

    def update_entry():
        if todos_fixmes:
            tfentry.delete(0, tk.END)
            tfentry.insert(0, todos_fixmes[todo_fixme_index])

    def forward():
        global todo_fixme_index
        todo_fixme_index = (todo_fixme_index + 1) % len(todos_fixmes)
        update_entry()

    def backward():
        global todo_fixme_index
        todo_fixme_index = (todo_fixme_index - 1) % len(todos_fixmes)
        update_entry()


    fbutton = tk.Button(tfwin, text="→", command=forward)
    fbutton.grid(row=1, column=1, padx=5, sticky="EW")
    bbutton = tk.Button(tfwin, text="←", command=backward)
    bbutton.grid(row=1, column=0, padx=5, sticky="EW")
    pywinstyles.change_header_color(tfwin, color=config_data['background'])
    maximize_minimize_button.hide(tfwin)
    update_entry()


usertext.bind("<Control-t>", todofixmewindow)

def get_line_count(usertext):
    linenumbertotal = int(usertext.index('end-1c').split('.')[0])
    return linenumbertotal

def calibratelinenums(): # automatically make linenums smaller if they go into 4 digits
    global fontsize
    fontsize = None
    linetotal = get_line_count(usertext)
    if linetotal > 999:
        fontsize = 10
    else:
        fontsize = 12
    return fontsize
    

def linenumbers():
    size = calibratelinenums()
    linenums.redraw(font=("Segoe UI SemiBold", size, "bold"))
    window.after(10, linenumbers)

def handle_tab(event): # make TAB 4 spaces
    # Get the current cursor position
    cursor_pos = usertext.index(tk.INSERT)
    # Insert four spaces at the cursor position
    usertext.insert(cursor_pos, "    ")
    # Return "break" to prevent the default Tab behavior  
    return "break"
usertext.bind("<Tab>", handle_tab)

def handle_backspace(event): # Backspacing indent removes it completely
    current_pos = usertext.index(tk.INSERT)
    prev_text = usertext.get(current_pos + ' - 4 chars', current_pos)
    
    if prev_text == '    ':
        usertext.delete(current_pos + ' - 4 chars', current_pos)
        usertext.insert(tk.INSERT, "\n") # Add new line to start from same line
    else:
        pass # allow normal backspace behavior if condition is false

usertext.bind("<BackSpace>", handle_backspace)

# Code for error message area
newlabel = tk.Label(text="No Errors Detected!")
newlabel.grid(row=3,column=0, columnspan=2, sticky="W") 

#-----------------------------------------------------------------



# The following code used to extract all callables for python syntax highlight (pretty neat, huh?)

kwrdslist = extractbuiltins.listfunctions()



keywords = {k: 'orange' for k in kwrdslist}
# In emergency situations, remove docstring from code below for pre defined syntax highlight (limited set)
'''
keywords['print'] = 'orange'
keywords['input'] = 'orange'
keywords['int'] = 'orange'
keywords['bin'] = 'orange'
keywords['exec'] = 'orange'
keywords['float'] = 'orange'
keywords['True'] = 'orange'
keywords['False'] = 'orange'
keywords['configure'] = 'orange'
keywords['id'] = 'orange'
keywords['len'] = 'orange'
keywords['range'] = 'orange'
keywords['open'] = 'orange'
keywords['Tk'] = 'orange'
keywords['return'] = 'orange'
keywords['pass'] = 'orange'
keywords['break'] = 'orange'
keywords['elif'] = 'orange'
keywords['str'] = 'orange'
'''

# Define colours from theme
syntax_colors = {
    'comment': config_data['comment'],
    'string': config_data['string'],
    'keyword': config_data['keyword'],
    'number': config_data['number'],
    'operator': config_data['operator'],
    'parenthesis': config_data['parenthesis'],
    'function': config_data['function'],
    'variable': config_data['variable'],
    'f_string': config_data['f_string'],
    'module': config_data['module']

}


def tag_f_strings(event):
    usertext.tag_remove("curly_brace", 1.0, tk.END)
    """Highlights curly brace pairs and their contents, and the 'f' in f-strings"""
    syntax_color = syntax_colors['f_string']

    text_string = usertext.get("1.0", tk.END)

    # Match curly brace pairs (content inside {})
    curly_brace_pattern = r"\{(.*?)\}"
    for match in re.finditer(curly_brace_pattern, text_string):
        start, end = match.span()
        usertext.tag_configure("curly_brace", foreground=syntax_color)
        usertext.tag_add("curly_brace", f"1.0 + {start} chars", f"1.0 + {end} chars")

    # Match 'f' followed by quotes, but only if it's at the beginning of the string (before any quote)
    f_string_pattern = r"f(['\"])"
    
    # Use lookahead to ensure 'f' is part of an f-string
    for match in re.finditer(f_string_pattern, text_string):
        start, end = match.span()
        
        # Check if the 'f' is indeed at the beginning of a string (not part of a normal string)
        if text_string[start-1] not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
            usertext.tag_configure("curly_brace", foreground=syntax_color)
            usertext.tag_add("curly_brace", f"1.0 + {start} chars", f"1.0 + {start+1} chars")

    del(text_string)  # delete the temporary string


def tag_todofixme(event):
  """Highlights todo and fixme keywords in the text widget."""
  usertext.tag_remove("highlight", 1.0, tk.END)


  # Configure single tag for keywords
  usertext.tag_configure("highlight", background="orange", foreground="black")

  # Get entire text content
  text_string = usertext.get("1.0", tk.END)

  # Define regular expressions for keywords 
  keywords = r"\b(TODO|FIXME)\b"

  # Find all occurrences of keywords
  for match in re.finditer(keywords, text_string): # Removed flags = re.IGNORECASE so it can be case sensitive
    start, end = match.span()
    usertext.tag_add("highlight", f"1.0 + {start} chars", f"1.0 + {end} chars")

  del(text_string)  # Free up memory


def tag_variables(event):
  """
  This function tags all occurrences of variables in the text widget.

  Args:
      event (tkinter.Event): The event object triggered by the text change.
  """

  # Configure variable tag appearance (adjust color as needed)
  usertext.tag_configure("variable", foreground=syntax_colors["variable"])

  # Get the current text content
  text_string = usertext.get("1.0", tk.END)

  # Parse the text as a Python expression
  try:
    tree = ast.parse(text_string)
      # Clear existing variable tags
    usertext.tag_remove("variable", 1.0, tk.END)
  except SyntaxError:
    # Handle potential syntax errors gracefully 
    return

  # Extract variable names from assignment nodes
  global variables
  variables = []
  for node in ast.walk(tree):
    if isinstance(node, ast.Assign):
      for target in node.targets:
        if isinstance(target, ast.Name):
          variables.append(target.id)

  # Highlight variable occurrences using regular expressions
  for var in variables:
    for match in re.finditer(rf"\b{var}\b", text_string):
      start, end = match.span()
      usertext.tag_add("variable", f"1.0 + {start} chars", f"1.0 + {end} chars")





#define syntax coloring
def tag_keywords(event):
    usertext.tag_remove("keyword", 1.0, tk.END)
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
    usertext.tag_remove("comment", 1.0, tk.END)
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
    usertext.tag_remove("string", 1.0, tk.END)
    usertext.tag_configure("string", foreground=syntax_colors['string'])

    # Define patterns for single and double quoted strings
    single_quote_pattern = r"[rR]?'[^'\\]*(\\.[^'\\]*)*'"
    double_quote_pattern = r'[rR]?"[^"\\]*(\\.[^"\\]*)*"'

    # Search for both types of strings
    for pattern in [single_quote_pattern, double_quote_pattern]:
        start = "1.0"
        while True:
            start = usertext.search(pattern, start, stopindex=tk.END, regexp=True)
            if not start:
                break

            # Find the matching end quote
            end = usertext.search(pattern[-1], start + "+1c", stopindex=tk.END, regexp=True)
            if not end:
                end = tk.END

            # Tag the entire string
            usertext.tag_add("string", start, end + "+1c")

            # Update start for next iteration
            start = end


def tag_numbers(event):
    usertext.tag_remove("number", 1.0, tk.END)
    usertext.tag_configure("number", foreground=syntax_colors['number'])
    text_string = usertext.get("1.0", tk.END)
    for match in re.finditer(r"\b\d+\b", text_string):
        start, end = match.span()
        usertext.tag_add("number", f"1.0 + {start} chars", f"1.0 + {end} chars")
    del(text_string)

def tag_module_names(event):
    usertext.tag_remove("module", 1.0, tk.END)
    usertext.tag_configure("module", foreground=syntax_colors['module'])
    
    # Get all the text from the editor
    text_string = usertext.get("1.0", tk.END)
    
    # Regular expression to match import statements, including aliases (e.g., import ast as AST)
    import_pattern = r"(import|from)\s+([a-zA-Z0-9_]+)(\s+as\s+[a-zA-Z0-9_]+)?"
    
    # Find all matches of import statements
    global imported_modules
    imported_modules = set() # TODO Make it work for aliases and multiple imports per line
    for match in re.finditer(import_pattern, text_string):
        module_name = match.group(2)  # The module name (without alias)
        alias = match.group(3)  # The alias (if any)
        
        # Add the module and alias to the list of imported modules
        imported_modules.add(module_name)
        if alias:
            alias_name = alias.split()[1]  # Get the alias name after "as"
            imported_modules.add(alias_name)
    
    # Now, highlight all occurrences of the imported modules throughout the code
    for module in imported_modules:
        for match in re.finditer(r"\b" + re.escape(module) + r"\b", text_string):
            start, end = match.span()
            usertext.tag_add("module", f"1.0 + {start} chars", f"1.0 + {end} chars")
    
    del(text_string)





def tag_syntax_errors(event):
    usertext.tag_remove("error", "1.0", tk.END)
    usertext.tag_configure("error", foreground="red", underline=True)

    index = usertext.index("insert") # Code to retrieve the line number 
    current_line_number = int(index.split(".")[0])

    text_string = usertext.get("1.0", tk.END)

    try:
        ast.parse(text_string)
        newlabel.config(text="No Errors Detected!")  # Fix bug, where error message remains
        newlabel.config(bg=config_data["background"]) # When no text present
    except SyntaxError as e:
        # Retrieve line no of the error   
        line_number = e.lineno

        # Only do the error thing if the user is currently not typing on the same line
        if line_number != current_line_number: # If error line no unequal to user line no
            start_index = f"{line_number}.0"  # Start of the line
            end_index = f"{line_number}.end"  # End of the line

            usertext.tag_add("error", start_index, end_index)

            # Assuming 'error_label' is the name of your label widget
            newlabel.config(text=f"Line {line_number}: {e.msg}")
            newlabel.config(bg="#85000b") # Change bg to a dark red color
        else:
            newlabel.config(text="No Errors Detected!")  # Clear error message if no errors
            newlabel.config(bg=config_data["background"]) # Remove Red color

    if len(text_string) == 0:
            newlabel.config(text="No Errors Detected!")  # Fix bug, where error message remains
            newlabel.config(bg=config_data["background"]) # When no text present


def tag_other(event):
    usertext.tag_remove("operator", 1.0, tk.END)
    usertext.tag_remove("parenthesis", 1.0, tk.END)
    usertext.tag_remove("function", 1.0, tk.END)
    # Access the text widget's content using its `get` method
    text_string = usertext.get("1.0", tk.END)
    # Update syntax colors dictionary if needed (assuming it's defined elsewhere)
    usertext.tag_configure("operator", foreground=syntax_colors['operator'])
    usertext.tag_configure("parenthesis", foreground=syntax_colors['parenthesis'])
    usertext.tag_configure("function", foreground=syntax_colors['function'])
    # Regular expressions for matching syntax elements (excluding numbers)
    operator_regex = r"[+\-*/%&|!><=]=?|[\+\-=]*=" # Modified to include the brand new +=
    parenthesis_regex = r"\(|\)"
    function_regex = r"\bdef\s+\w+\(.*\)"  # Matches `def` followed by whitespace, word, parentheses
    function_call_regex = r"\b(?<!\.)\w+\(.*\)"

    for regex, tag in [
        (operator_regex, "operator"),
        (parenthesis_regex, "parenthesis"),
        (function_regex, "function"),
        (function_call_regex, "function"),
    ]:
        for match in re.finditer(regex, text_string):
            start, end = match.span()
            usertext.tag_add(tag, f"1.0 + {start} chars", f"1.0 + {end} chars")
    del(text_string)

def tag_escaped_characters(event):
    try:
        usertext.tag_remove("escaped_char", 1.0, tk.END)
        usertext.tag_configure("escaped_char", foreground=syntax_colors['operator'])

        text_string = usertext.get("1.0", tk.END)

        # Find all escaped characters (backslashes followed by any character)
        for match in re.finditer(r"\\.", text_string):
            start, end = match.span()
            
            # Convert Python string indices to Tkinter "line.char" format safely
            # Or if using absolute integer indices directly:
            start_idx = f"1.0 + {start} chars"
            end_idx = f"1.0 + {end} chars"
            
            # Tag the entire match (backslash + character)
            usertext.tag_add("escaped_char", start_idx, end_idx)

        del text_string
        
    except (tk.TclError, IndexError): # Handle the highly common bad text index errors
        pass

# MASTER Function for Syntax Highlight
def tag_all(event=None):
    tag_syntax_errors(event)
    tag_todofixme(event)
    tag_other(event)
    tag_keywords(event)
    tag_numbers(event)
    tag_variables(event)
    tag_module_names(event)
    tag_comments(event) # Comment tag has slight delay
    tag_strings(event)
    tag_f_strings(event)
    tag_escaped_characters(event)


#-----------------------------------------------------------------
usertext.bind('<Any-KeyRelease>', tag_all)
  
scrollbar = tb.Scrollbar(frame)
scrollbar.grid(row=0,column=1,sticky="NSW")
scrollbar.config(cursor="sb_v_double_arrow")
resize()

# Create the TkLineNumbers widget and pack it to the leftv
linenums = TkLineNumbers(window, usertext, borderwidth=textandlineborder, justify="left", colors=(config_data['linenumfg'], config_data['background']))
linenums.grid(row=2,column=0,sticky="NSW",pady=0,padx=0)
# Redraw the line numbers when the text widget contents are modified
linenumbers()

scrollbar_x = tb.Scrollbar(frame, orient="horizontal", bootstyle="light")
usertext.config(xscrollcommand=scrollbar_x.set)
scrollbar_x.config(command=usertext.xview)
scrollbar_x.grid(row=1,column=0, sticky="ESW",columnspan=2,rowspan=1, pady=0)
scrollbar_x.config(cursor=' sb_h_double_arrow ')


frame.grid(row=2, column=1, columnspan=2,padx=0,sticky="NSEW",)

usertext.insert(tk.END,f"# Welcome to Blueconda: V{__version__}")
usertext.insert(tk.END,'\nprint("Hello, World!")')
tag_all()

indicat = tk.Label(text="Line 1, Column 1",bg="white")
indicat.grid(row=3,column=2)
update_row_column()

style = ttk.Style()
style.configure("TNotebook", background="white")
style.configure("TNotebook.Tab", background="white")

newstyle= tb.Style()
newstyle.configure('custom.TButton', font=fontnew)



#File Explorer Tab
class Application(tb.Frame):
    style = ttk.Style()
    style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 25))
    def __init__(self, window: tk.Tk | tk.Toplevel) -> None:
        super().__init__(window)
        # show="tree" removes the column header, since we
        # are not using the table feature.
        self.treeview = tb.Treeview(self,  show="tree",bootstyle="light")
        self.treeview.grid(row=0, column=0, sticky="nsew")
        self.ascrollbar = ttk.Scrollbar(self, orient="vertical", command=self.treeview.yview)
        # Position the Treeview and scrollbar using grid
        self.ascrollbar.grid(row=0, column=1, sticky="ns")
        self.ascrollbar.config(cursor="sb_v_double_arrow")
        # Fill the available space
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.treeview['yscrollcommand'] = self.ascrollbar.set

        self.bind("<Button-3>", self.show_popup_menu)
        
        # Call the item_opened() method each item an item
        # is expanded.
        self.treeview.tag_bind(
            "fstag", "<<TreeviewOpen>>", self.item_opened)
        # Make sure the treeview widget follows the window
        # when resizing.
        for w in (self, window):
            w.rowconfigure(0, weight=1)
            w.columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="nsew")
        # This dictionary maps the treeview items IDs with the
        # path of the file or folder.
        self.fsobjects: dict[str, Path] = {}
        self.file_image = tk.PhotoImage(file="src/file.png")
        self.folder_image = tk.PhotoImage(file="src/folder.png")
        self.py_file_image = tk.PhotoImage(file="src/python.png")
        # Load the root directory.
        self.load_tree(Path(Path(sys.executable).anchor))

        self.treeview.bind("<Button-3>", self.show_popup_menu)  # Bind right-click event to show popup menu
        self.popup_menu = tk.Menu(self.treeview, tearoff=0)
        self.popup_menu.add_command(label="Load Folder", command=self.load_selected_folder)
        self.popup_menu.add_separator()
        self.popup_menu.add_command(label="New Folder", command=self.create_folder)
        self.popup_menu.add_command(label="New File", command=self.create_file)
        self.popup_menu.add_separator()
        self.popup_menu.add_command(label="Delete", command=self.delete_item)
        self.popup_menu.add_command(label="Rename", command=self.rename_item)
        self.treeview.tag_bind("fstag", "<<TreeviewOpen>>", self.item_opened)

    def load_selected_folder(self):
        selected_folder = filedialog.askdirectory()
        if selected_folder:
            # Clear existing children of the selected folder
            for child_iid in self.treeview.get_children():
                self.treeview.delete(child_iid)
            # Load the selected folder into the treeview
            self.load_tree(Path(selected_folder))
            if len(selected_folder) < 46:
                frame4.config(text=selected_folder)
            else:
                frame4.config(text=". . .  " + selected_folder[-40:]) # Adjust for very long filenames
 
    def safe_iterdir(self, path: Path) -> tuple[Path, ...] | tuple[()]:
        """
        Like `Path.iterdir()`, but do not raise on permission errors.
        """
        try:
            return tuple(path.iterdir())
        except PermissionError:
            return ()
    
    def get_icon(self, path: Path) -> tk.PhotoImage:
        if path.is_dir():
            return self.folder_image
        elif path.suffix == ".py":
            return self.py_file_image
        else:
            return self.file_image
    
    def insert_item(self, name: str, path: Path, parent: str = "") -> str:
        """
        Insert a file or folder into the treeview and return the item ID.
        """
        parent_iid = parent or ""  # Use the provided parent if available, otherwise use an empty string

        iid = self.treeview.insert(
            parent_iid, 'end', text=name, tags=("fstag",),
            image=self.get_icon(path))
        self.fsobjects[iid] = path

        return iid
    
    def load_tree(self, path: Path, parent: str = "") -> None:
        for fsobj in self.safe_iterdir(path):
            fullpath = path / fsobj
            child = self.insert_item(fsobj.name, fullpath, parent)
            if fullpath.is_dir():
                for sub_fsobj in self.safe_iterdir(fullpath):
                    self.insert_item(sub_fsobj.name, fullpath / sub_fsobj, child)
            elif fullpath.suffix == ".py":
                self.treeview.tag_bind("fstag", "<Double-Button-1>", self.on_file_select)
    
    def load_subitems(self, iid: str) -> None:
        """
        Load the content of each folder inside the specified item
        into the treeview.
        """
        for child_iid in self.treeview.get_children(iid):
            if self.fsobjects[child_iid].is_dir():
                self.load_tree(self.fsobjects[child_iid],
                               parent=child_iid)
    
    def item_opened(self, _event: tk.Event) -> None:
        """
        Handler invoked when a folder item is expanded.
        """
        # Get the expanded item.
        iid = self.treeview.selection()[0]
        # If it is a folder, loads its content.
        self.load_subitems(iid)
    def on_file_select(self, event: tk.Event) -> None:
        global file_loaded
        iid = self.treeview.selection()[0]
        path = self.fsobjects[iid]
        if path.suffix == ".py":
            conftext = 'Please ensure you save all your work before navigating out of this file. Any unsaved data will be lost. Do you wish to continue?'
            confirmation = messagebox.askyesno("Confirm",conftext)
            if confirmation:
                with open(path, "r", encoding="utf-8") as f:
                    usertext.delete("1.0", tk.END)
                    usertext.insert("1.0", f.read())
                file_path = path
                update_title(str(file_path))
                tag_all()
                with open("temp/currentfile.txt","w") as rw:
                    rw.write(str(path))
                usertext.edit_modified(False)
                file_loaded = True
            else:
                messagebox.showerror("Abandoned","Task abandoned, no file opened.")
        elif os.path.isfile(path):
            os.startfile(path)

    def show_popup_menu(self, event: tk.Event) -> None:
        iid = self.treeview.identify_row(event.y)  # Get the item ID that was right-clicked
        if iid:  # If an item was right-clicked
            self.treeview.selection_set(iid)  # Set the right-clicked item as the selected item
            self.popup_menu.post(event.x_root, event.y_root)  # Show the popup menu at the right-click position

    def create_folder(self) -> None:
        parent_iid = self.treeview.selection()[0]  # Get the selected item ID
        parent_path = self.fsobjects[parent_iid]  # Get the path of the selected item

        if not parent_path.is_dir():
            parent_path = parent_path.parent  # Use the parent directory if a file is selected

        new_folder_name = simpledialog.askstring("Folder Name", "Enter the folder name:")
        if new_folder_name:
            new_folder_path = parent_path / new_folder_name
            new_folder_path.mkdir()
            self.insert_item(new_folder_name, new_folder_path, parent_iid)
            
    def create_file(self) -> None:
        parent_iid = self.treeview.selection()[0]  # Get the selected item ID
        parent_path = self.fsobjects[parent_iid]  # Get the path of the selected item

        if parent_path.is_file():
            parent_path = parent_path.parent  # Use the parent directory if a file is selected

        new_file_name = simpledialog.askstring("File Name", "Enter the file name (with extension):")
        if new_file_name:
            new_file_path = parent_path / new_file_name
            new_file_path.touch()
            self.insert_item(new_file_name, new_file_path, parent_iid)

    def delete_item(self) -> None:
        iid = self.treeview.selection()[0]  # Get the selected item ID
        path = self.fsobjects[iid]  # Get the path of the selected item
        if messagebox.askyesno("Confirm", f"Are you sure you want to delete {path}?\nYou can restore the file from the recycle bin."):
            send2trash.send2trash(str(path)) # Sends to recycle bin
            self.treeview.delete(iid)  # Remove the item from the treeview

    def rename_item(self) -> None:
        iid = self.treeview.selection()[0]  # Get the selected item ID
        path = self.fsobjects[iid]  # Get the path of the selected item
        new_name = simpledialog.askstring("Rename", "Enter the new name:")
        if new_name:
            new_path = path.with_name(new_name + path.suffix)
            path.rename(new_path)
            self.treeview.item(iid, text=new_name)  # Update the item's text in the treeview

   
#File Explorer Tab


# Create the helpful sidebar
notebook = tb.Notebook(window, width=320, bootstyle="primary")


# create frames
frame1 = tk.Frame(notebook, bg="white")
frame2 = tk.Frame(notebook, bg="white")
frame3 = tk.Frame(notebook, bg="white")
frame4 = tb.LabelFrame(notebook, text="(Click Here to load a Folder)") # This is label frame to 
frame5 = tk.Frame(notebook, bg="white")      # display file path as well
frame6 = tk.Frame(notebook, bg="white")


# add frames to notebook
notebook.add(frame1, text='MiniMap')
notebook.add(frame2, text='Notes')
notebook.add(frame3, text='Variables')
notebook.add(frame4, text='Files')
notebook.add(frame5, text='Analysis')
notebook.add(frame6, text='Library Manager')
notebook.select(3)


notebook.grid(row=2, column=3, columnspan=2, sticky="NSEW")


# Code for minimap 
# TODO This blocks Undo Redo, fix in a later version release
class TextPeer(tk.Text):
  """A peer of an existing text widget with line number synchronization"""
  count = 0

  def __init__(self, master, cnf={}, **kw):
    TextPeer.count += 1
    parent = frame1  # Assuming frame1 is defined elsewhere
    peer_name = "peer-{}".format(TextPeer.count)
    if str(parent) == ".":
      peer_path = ".{}".format(peer_name)
    else:
      peer_path = "{}.{}".format(parent, peer_name)

    # Create the peer (unchanged)
    master.tk.call(master, 'peer', 'create', peer_path, *self._options(cnf, kw))

    # Create the tkinter widget based on the peer (unchanged)
    tk.BaseWidget._setup(self, parent, {'name': peer_name})

    # Bind click event and store reference to other widget
    self.bind("<Button-1>", lambda event: self.on_click(event))
    self.other_widget = usertext  # Store reference to other widget

    self.config(wrap=tk.NONE) # Change the textwrap to None, so that line does not take up more than one
    

    self.tag_configure("sel", background="#75dee3", foreground="white")   # Change the selection color

  def on_click(self, event):
    
    # Get clicked line number
    clicked_line = int(self.index("@{},{}".format(event.x, event.y)).split(".")[0])

    # Update other widget to show the clicked line
    usertext.see(f"{clicked_line}.0")
    usertext.focus_set()
    select_linemain(clicked_line)

with open("settings/font.txt","r",encoding="utf-8") as op: # Obtain the font from setings
    changefont = op.read()

# Create MiniMap
minimap = TextPeer(usertext, font=(f"{changefont}", 6), state="disabled",
                   background=config_data['background'], foreground=config_data['textforeground'])


newscroll = tb.Scrollbar(frame1, orient=tk.VERTICAL)
newscroll.pack(side="right",expand=True,fill=tk.Y)

minimap.pack(side="left",expand=True,fill=tk.BOTH)
minimap['yscrollcommand'] = newscroll.set

usertext.configure(yscrollcommand=scrollbar.set)
scrollbar.config(command=usertext.yview)

def on_yview(usertext):
  # Get the current vertical scroll position of the first widget
  y_view = minimap.yview()[0]
  # Update the second widget's scroll position to match
  usertext.yview_moveto(y_view * 1.5)

newscroll.configure(command=minimap.yview)

#Code for minimap end

# Code For Function Tree----------------------------------------------------------------
def outlinewindow(usertext):
    def get_functions_classes(code):
        """Extracts function/class names and line numbers from Python code."""
        functions = []
        classes = []
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                line_number = node.lineno  # Extract line number from AST
                function_name = node.name
                functions.append((function_name + '()', line_number))  # Store with line number
            elif isinstance(node, ast.ClassDef):
                line_number = node.lineno  # Extract line number from AST
                class_name = node.name
                classes.append((class_name, line_number))  # Store with line number
        return {'Functions': functions, 'Classes': classes}
        
    
    def parse_code():
  
        outline = get_functions_classes(usertext.get(1.0, tk.END))
        
        return outline
    
   

    def jump_to_definition(item):
        global usertext

        try:
            # Attempt to extract name and line number from string
            if isinstance(item, str):
                name_and_line = item.split()  # Split at spaces
                if len(name_and_line) == 2:
                    item_name = name_and_line[0]
                    line_number = int(name_and_line[1])  # Convert to integer
                else:
                    raise ValueError("Unexpected item format (string)")
            else:
                raise TypeError("Unexpected item type (not a string or tuple)")
            usertext.focus_set()
            usertext.see(f"{line_number}.0")
            select_linemain(line_number)
            root.attributes('-topmost', True)

            
        except (ValueError, TypeError) as e:
            print(f"Error handling item: {item}\n{e}")

    def on_tree_view_click(event):
        item = tree.item(tree.selection()[0])['text']
        # Try to get line number from AST (optional)
        jump_to_definition(item)

    # Create a new tkinter window
    root = tk.Toplevel()
    root.attributes("-alpha", 0.9)
    root.attributes('-topmost', True)
    root.title("Outline")
    root.geometry(scalewindow(160, 400))
    
    # Create a text widget for entering Python code

    style = ttk.Style()
    style.configure("mystyle.Treeview", font=('Arial', 12))
    # Create a Treeview widget to display the outline
    tree = ttk.Treeview(root, style='mystyle.Treeview')
    tree.pack(fill=tk.BOTH, expand=True)
    tree.bind("<<TreeviewSelect>>", on_tree_view_click)
    # Parse the code and generate the outline
    outline = parse_code()
    
    # Display the outline in the Treeview widget
    for category, items in outline.items():
        category_node = tree.insert('', 'end', text=category)
        for item in items:
            tree.insert(category_node, 'end', text=item)

    pywinstyles.change_header_color(root, color=config_data['background'])
    maximize_minimize_button.hide(root)




def return_quote(): # Fun easter egg
    response = requests.get("https://zenquotes.io/api/random")
    json_data = loads(response.text)
    quote = (
        json_data[0]["q"] + " -" + json_data[0]["a"]
    )  # aligning the quote and it's author name in one string
    return quote

def quote(event):
    quotewin = tb.Toplevel()
    quotewin.attributes('-topmost', True)
    quotewin.attributes("-alpha", 0.9)
    quotewin.title("Quote")
    thequote = return_quote()
    tb.Label(quotewin, text=thequote, font=("Abadi Extra Light", 15)).pack()
    pywinstyles.change_header_color(quotewin, color=config_data['background'])
    maximize_minimize_button.hide(quotewin)





newlabel.bind("<Button-1>", quote)
    
#Function Tree END----------------------------------------------------------------------


# Blueconda's notes tab is autosaved using the below function

def autosavenotes(event):
    txt = open("temp/usernotes.txt","w", encoding="utf-8")
    newnotes = notes.get(1.0,tk.END)
    txt.write(newnotes)
    txt.close()
#====================


notes = tb.ScrolledText(frame2, borderwidth=0,wrap="word")
notes.pack(fill=tk.BOTH)
notes.configure(font=fontnew)


def tutorial(): # REDACTED
    def tutorialwreck():
        ll1.destroy()
        ll2.destroy()
        ll3.destroy()
        ll4.destroy()
        ll5.destroy()
        ll6.destroy()
    global ll1, ll2, ll3, ll4, ll5, ll6
    snfont = ("Segoe Print", 8)
    ll1 = tk.Label(text="Menu bar of buttons\nHover to see function ->", font=snfont, autostyle=False, bg="#ffffa3")
    ll2 = tk.Label(text="Tools Sidebar ->", font=snfont, autostyle=False, bg="#ffffa3")
    ll3 = tk.Label(text="<- Line Numbers\nappear here", font=snfont, autostyle=False, bg="#ffffa3")
    ll4 = tk.Label(text="| Total time elapsed\nV since app opened ", font=snfont, autostyle=False, bg="#ffffa3")
    ll5 = tk.Label(text="Current Row/Column\nClick to jump to line", font=snfont, autostyle=False, bg="#ffffa3")
    ll6 = tk.Label(text="Current overall\n RAM usage", font=snfont, autostyle=False, bg="#ffffa3")
    ll1.place(x=100, y=10)
    ll2.place(x=1700, y=500)
    ll3.place(x=80, y=500)
    ll4.place(x=80, y=1140)
    ll5.place(x=1800, y=1140)
    ll6.place(x=2300, y=1140)
    window.after(5000, tutorialwreck)



#----

def on_enter(event):
    # Get the current line and its starting index
    current_line = usertext.get('insert linestart', 'insert lineend')
    prev_index = usertext.index('insert linestart') + "-1l"
    prev_line = usertext.get(prev_index + ' linestart', prev_index + ' lineend')

    # Check if the previous line ends with a colon
    if prev_line.rstrip().endswith(':') or prev_line.rstrip().endswith(':\n'):
        # Indent the new line with four spaces
        usertext.insert('insert', '\n    ')
        return 'break'

    # Check if the previous line is indented
    prev_indent = len(prev_line) - len(prev_line.lstrip())
    if prev_indent % 4 == 0:
        # Maintain the same indentation in the new line
        usertext.insert('insert', '\n' + ' ' * prev_indent)
        return 'break'

    
#----

usertext.bind('<Return>', on_enter)


#Listbox for Variables

def is_safe_name(name):
    if keyword.iskeyword(name):
        return False
    # Check if the name is in built-in names
    if name in dir(builtins):
        return False
    # Check if the name follows the variable naming pattern (simple regex example)
    if not re.match("^[a-zA-Z_][a-zA-Z0-9_]*$", name):
        return False
    return True

def is_safe_value(value):
    # Check for simple types (could be extended with more types)
    if isinstance(value, (int, float, str, bool, list, tuple, dict, set)):
        return True
    elif value == None:
        return True
    # Additional checks could include:
    # - The size of the data structure (to prevent very large objects)
    # - Content checks (e.g., no executable code within strings)
    elif isinstance(value, tk.Widget):
        return True
    return False

def update_vars_listbox(code): #TODO Fix error: AttributeError: 'Subscript' object has no attribute 'id'

    children = vars_tree.get_children()
    # Delete each child item
    for child in children:
        vars_tree.delete(child)

    tree = ast.parse(code)
    vars_dict = {}

    # I myself don't understand a THING going on here
    for node in ast.walk(tree):
      if isinstance(node, ast.Assign):
          for target in node.targets:
              if isinstance(target, ast.Name) and is_safe_name(target.id):
                  try:
                      # Direct assignment of built-in types
                      if isinstance(node.value, (ast.BinOp, ast.Call)):  # Check for operations or function calls
                          if (isinstance(node.value.func, ast.Attribute) and
                              node.value.func.attr in ['range', 'bytes', 'bytearray', 'memoryview']):
                              value = eval(compile(ast.Expression(node.value), '', 'eval'))
                              vars_dict[target.id] = value
                          elif isinstance(node.value, ast.Call) and node.value.func.id == 'int':
                              # Handle int cast explicitly
                              value = int(eval(compile(ast.Expression(node.value.args[0]), '', 'eval')))
                              vars_dict[target.id] = value
                      # Handle None assignment
                      elif node.value is None:
                          vars_dict[target.id] = None
                      else:
                          # Fallback for other literals and complex values
                          value = eval(compile(ast.Expression(node.value), '', 'eval'))
                          if is_safe_value(value):
                              vars_dict[target.id] = value
                          else:
                              vars_dict[target.id] = f'{value} (Unsafe value)'
                  except Exception as e:
                      vars_dict[target.id] = f"Complex Variable"

                  # Optional: Handle unsafe variable names (example)
              elif is_safe_name(target.id) == False:
                    vars_tree.insert("", tk.END, text=f"A variable with a\nkeyword name caught\n({target.id})")

    for var, value in vars_dict.items():
        item_id = vars_tree.insert("", tk.END, text=var, values=(value,)) 
        vars_tree.tag_configure("value_tag", foreground=config_data['textforeground']) # Left here for customization purposes (Applies to both columns)
        vars_tree.item(item_id, tags="value_tag")  # Apply the tag to the value column

'''
try:
    # Code in your if statement
except Exception as e:
    pass
'''
def update_button_position():
    try:
        x, y, _, _ = usertext.bbox(tk.INSERT)
        if listbox.winfo_ismapped:
            xfactor = listbox.winfo_width() # Not the singing show!
            yfactor = listbox.winfo_height()

            Xbutton.place(x=x + xfactor, y=y + yfactor + 200)
            # To make sure it is same when the screen size changes

    except Exception:
        pass



def get_module_suggestions(module_name, prefix=""):
    try:
        module = __import__(module_name)
        members = dir(module)
        
        if prefix:
            return [m for m in members if m.startswith(prefix)]
        return members
    except ImportError:
        return
    except Exception as e:
        print(f"Error during API completion for {module_name}: {e}")
        return



WordToUse = ''
ApiComplete = False
word_before_dot = ''

def on_key(event, DotTyped, SpaceTyped):
    """Performs autocomplete based on the current word under the caret and handles selection."""
    # Make variables global so that they can work across functions
    global WordToUse, ApiComplete, word_before_dot
    global start_index, end_index
    

    # Get the current word under the caret
    start_index = usertext.index(tk.INSERT + "-1c wordstart")  # Get word start index
    end_index = usertext.index(tk.INSERT + " wordend")  # Get word end index
    current_word = usertext.get(start_index, end_index).strip()

    # using list comprehension to remove duplicated from list
    res = []
    [res.append(x) for x in variables if x not in res]

    # Combine autocomplete data and variables
    autocomplete_data = extractbuiltins.listfunctions() + res

    
    # Extracting word before dot
    if DotTyped == True:
        current_pos = usertext.index(tk.INSERT)
        dot_index = current_pos  # Current position is after the typed dot
        # Move one character to the left to be at the dot
        previous_char_index = f"{current_pos}-1c"
        # Get the index of the beginning of the word before the dot
        word_start_index = usertext.index(f"{previous_char_index} wordstart")
        # Extract the word
        word_before_dot = usertext.get(word_start_index, dot_index).strip()


    # Lot of really complex logic for API AutoComplete

    if doApiComplete == True:
        ApiComplete = True
        WordToUse = word_before_dot

    if doApiComplete == False:
        ApiComplete = False
        WordToUse = ''  

    # In plain english:
    # If dot has been typed and the word before the dot is in the list of imported modules and the word before dot is not blank
    if (DotTyped == True or ApiComplete == True) and (word_before_dot in imported_modules) and (WordToUse != ''):
        autocomplete_options = [option for option in get_module_suggestions(WordToUse) if option.startswith(current_word)]
    else:
        autocomplete_options = [option for option in autocomplete_data if option.startswith(current_word)]

   
    # Update Listbox content
    listbox.delete(0, tk.END)
    for option in autocomplete_options:
        listbox.insert(tk.END, f"{option}")

    # Position Listbox below the caret
    x, y, _, _ = usertext.bbox(tk.INSERT)
    listbox.place(x=x, y=y + 200)
    update_button_position()

    def removeunwantedlistbox():
        # Remove Listbox on focus loss or no options
        if len(autocomplete_options) == 0:
            listbox.place_forget()
            update_button_position()
            Xbutton.place_forget()

    removeunwantedlistbox()
    #indow.after(7000, listbox.place_forget)

def on_listbox_select(event):
    """Handles selection of an item from the listbox."""

    # Get the selected item
    selected_item = listbox.get(listbox.curselection())

    try: 
        info = inspect.getdoc(eval(selected_item))
    except:
        pass
    


listbox = tk.Listbox(window)
listbox.place_forget()

listbox.bind("<<ListboxSelect>>", on_listbox_select)


def removeautocorrect():
    listbox.place_forget() # unmap listbox
    Xbutton.place_forget() # unmap X button

Xbutton = tb.Button(master=window, text="✕", command= removeautocorrect, bootstyle="link")
update_button_position() # Initial placement 


type_definitions = {
    "VARIABLE": "A named reference to a value.",
    "MODULE": "An imported Python module.",
    "CLASS": "A class definition / blueprint for objects.",
    "ABSTRACT BASE CLASS": "A class that cannot be instantiated directly.",
    "FUNCTION": "A regular Python function.",
    "METHOD": "A function bound to a class instance.",
    "BUILTIN": "A built-in function or method implemented in C.",
    "GENERATOR FUNCTION": "A function that returns a generator when called.",
    "COROUTINE FUNCTION": "An async function defined with 'async def'.",
    "ASYNC GENERATOR FUNCTION": "An async function that yields values.",
    "GENERATOR": "An iterator produced by a generator function.",
    "COROUTINE": "An object produced by calling a coroutine function.",
    "AWAITABLE": "An object that can be used in an 'await' expression.",
    "FRAME": "A stack frame object.",
    "TRACEBACK": "A traceback object.",
    "CODE OBJECT": "A compiled code object.",
    "DATA DESCRIPTOR": "A descriptor implementing both __get__ and __set__.",
    "GETSET DESCRIPTOR": "A C-level attribute descriptor.",
    "MEMBER DESCRIPTOR": "A descriptor for a slot member.",
    "METHOD WRAPPER": "A bound wrapper around a slot method.",
    "CALLABLE": "An object that can be called like a function.",
    "UNDEFINED": "This name could not be resolved in the current scope.",
    "OTHER": "Definition not found.",
}
 
 
def resolve_object(name):
    """
    Resolves a (possibly dotted, e.g. 'obj.attr.method') name typed in the
    editor to the actual Python object it refers to.
 
    Lookup order for the root name: tracked `variables` -> module globals()
    -> builtins. Each subsequent '.'-separated part is resolved with
    getattr(). Returns the resolved object, or None if it can't be found.
    """
    if not name:
        return None
 
    parts = name.split('.')
    root = parts[0]
 
    if isinstance(variables, dict) and root in variables:
        # variables is a name -> value dict; use the stored value directly.
        obj = variables[root]
    elif root in variables or root in globals():
        # variables is a list/set/tuple of tracked names (or not tracked
        # at all) - the actual value still needs to come from globals().
        if root not in globals():
            return None
        obj = globals()[root]
    elif hasattr(builtins, root):
        obj = getattr(builtins, root)
    else:
        return None
 
    for attr in parts[1:]:
        try:
            obj = getattr(obj, attr)
        except AttributeError:
            return None
 
    return obj
 
 
def showdefinition(title, content=None):
    """
    Displays info in a styled Toplevel popup (instead of a messagebox), to
    match the rest of the app's window styling.
 
    Backwards-compatible mode: if `content` is None, `title` is treated as
    an object-type key (e.g. "FUNCTION") and looked up in type_definitions.
    Otherwise `title`/`content` are shown directly, which is how the
    Declaration/Documentation/Methods entries use it.
    """
    if content is None:
        object_type = title
        content = type_definitions.get(object_type, "Definition not found.")
        title = f"Definition of {object_type}"
        content = f"{object_type}: {content}"
 
    win = tk.Toplevel()
    win.attributes('-topmost', True)
    win.attributes("-alpha", 0.9)
    win.geometry("420x260")
    win.configure(bg=config_data["background"])
    win.title(title)
 
    text_box = tk.Text(
        win,
        wrap="word",
        bg=config_data["background"],
        fg=config_data.get("foreground", "white"),
        relief="flat",
        borderwidth=0,
        font=("Consolas", 11),
    )
    text_box.insert("1.0", content)
    text_box.configure(state="disabled")
    text_box.pack(fill="both", expand=True, padx=12, pady=12)
 
    pywinstyles.change_header_color(win, color=config_data['background'])
    maximize_minimize_button.hide(win)
 
 
def get_object_type(word):
    """Determines the type of the object that `word` refers to."""
    if word in variables:
        return "VARIABLE"
 
    obj = resolve_object(word)
 
    if obj is None:
        return "UNDEFINED"
    elif inspect.ismodule(obj):
        return "MODULE"
    elif inspect.isclass(obj):
        # isabstract() only makes sense for classes, and isclass() would
        # otherwise always win first, so check it here.
        return "ABSTRACT BASE CLASS" if inspect.isabstract(obj) else "CLASS"
    elif inspect.isfunction(obj):
        return "FUNCTION"
    elif inspect.ismethod(obj):
        return "METHOD"
    elif inspect.isbuiltin(obj):
        return "BUILTIN"
    elif inspect.isgeneratorfunction(obj):
        return "GENERATOR FUNCTION"
    elif inspect.iscoroutinefunction(obj):
        return "COROUTINE FUNCTION"
    elif inspect.isasyncgenfunction(obj):
        return "ASYNC GENERATOR FUNCTION"
    elif inspect.isgenerator(obj):
        return "GENERATOR"
    elif inspect.iscoroutine(obj):
        return "COROUTINE"
    elif inspect.isawaitable(obj):
        return "AWAITABLE"
    elif inspect.isframe(obj):
        return "FRAME"
    elif inspect.istraceback(obj):
        return "TRACEBACK"
    elif inspect.iscode(obj):
        return "CODE OBJECT"
    elif inspect.isdatadescriptor(obj):
        return "DATA DESCRIPTOR"
    elif inspect.isgetsetdescriptor(obj):
        return "GETSET DESCRIPTOR"
    elif inspect.ismemberdescriptor(obj):
        return "MEMBER DESCRIPTOR"
    elif isinstance(obj, types.MethodWrapperType):
        return "METHOD WRAPPER"
    elif callable(obj):
        return "CALLABLE"
    else:
        return "OTHER"
 
 
def show_context_menu(event):
    """Shows the context menu on a right-click."""
    text_widget = event.widget
    x, y = event.x_root, event.y_root
 
    # Get the index of the character at the click position
    index = text_widget.index(f"@{event.x},{event.y}")
 
    # Extract the word at the clicked position
    word, word_color = get_word_at_index(text_widget, index)
 
    if not word:
        return
 
    obj = resolve_object(word)
    obj_type = get_object_type(word)
 
    def show_declaration():
        if obj is None:
            content = f"'{word}' could not be resolved in the current scope."
        elif inspect.isroutine(obj) or inspect.isclass(obj):
            try:
                content = f"{word}{inspect.signature(obj)}"
            except (TypeError, ValueError):
                content = f"{word}(...)  (signature unavailable)"
        else:
            content = f"{word} = {obj!r}"
        showdefinition(f"Declaration of {word}", content)
 
    def show_documentation():
        if obj is None:
            content = f"'{word}' could not be resolved in the current scope."
        else:
            content = inspect.getdoc(obj) or "No documentation available."
        showdefinition(f"Documentation for {word}", content)
 
    def show_members():
        if obj is None:
            content = f"'{word}' could not be resolved in the current scope."
        else:
            members = [m for m in dir(obj) if not m.startswith('__')]
            content = "\n".join(members) if members else "No public methods/attributes."
        showdefinition(f"Methods/Attributes of {word}", content)
 
    # Create the context menu
    context_menu = tk.Menu(text_widget, tearoff=0)
    bold_font = tkfont.Font(weight="bold", size=20, family="Consolas")
    try:
        # word_color[-1] is the current value in the tag_config tuple;
        # word_color[-1:] (a 1-item tuple) was being passed before, which
        # is not a valid Tk color and always fell into the except branch.
        context_menu.add_command(label=f"{word}", font=bold_font, foreground=word_color[-1])
    except (TypeError, IndexError):
        # No color tag applied to this word
        context_menu.add_command(label=f"{word}", font=bold_font)
 
    context_menu.add_command(
        label=f"Type: {obj_type}",
        command=lambda: showdefinition(obj_type)
    )
    context_menu.add_command(label="Declaration", command=show_declaration)
    context_menu.add_command(label="Documentation", command=show_documentation)
    context_menu.add_command(label="Methods/Attributes", command=show_members)
 
    # Display the menu
    context_menu.post(x, y)
 
 
def get_word_at_index(text_widget, index):
    """
    Extracts the 'word' and its foreground color at the given text index,
    handling dots and underscores.
 
    Args:
        text_widget: The tkinter.Text widget.
        index: The index of the character.
 
    Returns:
        A tuple containing the extracted word (str) and its foreground color (str or None).
    """
    start_index = index
    end_index = index
 
    # Scan backward for word start
    while True:
        if start_index == "1.0":
            break
        prev_index = text_widget.index(f"{start_index}-1c")
        char = text_widget.get(prev_index, start_index)
        if not (char.isalnum() or char in ('.', '_')):
            break
        start_index = prev_index
 
    # Scan forward for word end
    while True:
        next_index = text_widget.index(f"{end_index}+1c")
        if next_index == f"{text_widget.index('end-1c')}+1c" or next_index == end_index:
            break
        char = text_widget.get(end_index, next_index)
        if not (char.isalnum() or char in ('.', '_')):
            break
        end_index = next_index
 
    # Extract the word. Note: parentheses can never end up in `word` since
    # the scans above only ever include alnum/./_ characters, so the old
    # parenthesis-stripping logic here was dead code and has been removed.
    word = text_widget.get(start_index, end_index)
 
    # Get the color at the start of the word
    color = get_text_color(text_widget, start_index)
 
    return word, color
 
 
def get_text_color(text_widget, index):
    """
    Gets the foreground color of the text at the given index in the Text widget.
    """
    tag_names = text_widget.tag_names(index)
    for tag_name in tag_names:
        config = text_widget.tag_config(tag_name)
        if 'foreground' in config:
            return config['foreground']
    return None
 


usertext.bind("<Button-3>", show_context_menu)

def get_function_description(func_name):
  """
  This function retrieves the docstring and signature for a built-in function.

  Args:
      func_name: The name of the built-in function (e.g., "print", "input").

  Returns:
      A string containing the docstring and signature if found, 
      or an error message if not found.
  """
  try:
    # Get the built-in function object
    func = getattr(builtins, func_name)
    # Extract docstring and signature
    docstring = inspect.getdoc(func)
    try:
        signature = inspect.signature(func)
    except Exception:
        signature = "No Signature Found"
    # Format the output with clear separation
    return f"Description:\n{docstring}\n\nSignature:\n{signature}"
  except AttributeError:
    return "ERROR"

def on_run():
    code = usertext.get("1.0", tk.END)
    update_vars_listbox(code)
    del(code)
#Listbox for Variables END


text_file = open("temp/usernotes.txt", "r", encoding="utf-8")
newinsert = text_file.read()
text_file.close()
notes.insert(tk.END,newinsert)
del(newinsert)
notes.bind("<Any-KeyRelease>",autosavenotes)

app = Application(frame4)
frame4.bind("<Button-1>", lambda event: app.load_selected_folder())


# The following code has been redacted (kept here for emergency use)
#vars_listbox = tk.Listbox(frame3,height=20)
#vars_listbox.pack(fill=tk.BOTH)
#vars_listbox.configure(font=fontnew)


def ResourceUsageWindow():
    # Boilerplate Toplevel code
    rwin = tk.Toplevel()                            
    rwin.attributes('-topmost', True)               
    rwin.attributes("-alpha", 0.9)                  
    #rwin.geometry("600x600")                 
    rwin.configure(bg=config_data["background"])    
    rwin.title("Resource Usage")   
    # Create stop event flag for thread
    stopflag = threading.Event()

    # Create TKChart object
    # IMPORTANT INFO: TKChart contains a VALIDATE module that is buggy
    # On my own system I have modified its source file to delete all validation functions
    # this will need to be resolved if you're building from source.
    line_chart = tkchart.LineChart(
        master=rwin,
        x_axis_data="t/s",
        y_axis_data="% USAGE",
        x_axis_values=("01", "02", "03", "04", "05", "06", "07", "08", "09", "10"),
        y_axis_values=(0, 100),
        y_axis_label_count=10,
        y_axis_section_count=10,
        x_axis_section_count=10,
    )
    line_chart.grid(row=0,column=0, columnspan=2, sticky="NSEW")
    line1 = tkchart.Line( # CPU USAGE LINE
        master=line_chart,
        color="#5dffb6",
        size=2,
        style="dashed",
        style_type=(10, 5),
    )
    line2 = tkchart.Line( # RAM USAGE LINE
        master=line_chart,
        color="#FFBAD2",
        size=2,
        point_highlight="enabled",
        point_highlight_color="#FFBAD2",
    )
    # DATA handler function
    def display_data():
        while not stopflag.is_set(): # Repeat indefinitely until flag exists
            # Use psutil to get CPU and RAM usage
            cpu_usage = psutil.cpu_percent(interval=0.5)
            ram = psutil.virtual_memory()
            ram_usage = ram.percent
            # Display on graph
            line_chart.show_data(line=line1, data=[cpu_usage])
            line_chart.show_data(line=line2, data=[ram_usage])
            if stopflag.wait(timeout=0.5):
                break # Terminate loop
    def on_close(): # Function to terminate thread on window close, override usual
        stopflag.set()  # Signal the thread to stop
        rwin.destroy()  # Close the window
    rwin.protocol("WM_DELETE_WINDOW", on_close)  # Override close button behavior

    threading.Thread(target=display_data, daemon=True).start()

    # Labels for graph lines
    ttk.Label(rwin, foreground="#5DFFB6", text="CPU USAGE").grid(row=1, column=0)
    ttk.Label(rwin, foreground="#FFBAD2", text="RAM USAGE").grid(row=1, column=1)
    # Lock window size, AFTER widgets have been placed within
    rwin.resizable(False, False)
    # Theming boilerplate
    pywinstyles.change_header_color(rwin, color=config_data['background'])  
    maximize_minimize_button.hide(rwin)  


def swap_icons():
  '''
  Change between simple icons and regular icons
  '''
  temp_name = "src_temp_swap_xyz"
  os.rename("src", temp_name)
  os.rename("srcminimalist", "src")
  os.rename(temp_name, "srcminimalist")
  newtoast = ToastNotification(
        title="Icon Pack Changed!",
        message=f"Icon Pack changed.\nRestart to see changes.",
        duration=3000,
        icon="🎨"
    )
  newtoast.show_toast()

def get_help_info(selected_text):
  """Gets help information for the selected text in a separate thread.

  Args:
    selected_text: The selected text from the text widget.
  """

  def run_subprocess(): # TO-DO Make it not overlap two help notes eg: for del and delattr
    try:                # Due to this being an obscure feature I'll consider doing this, one day
        kwargs = {
            "capture_output": True,
            "text": True,
            "check": True
        }
        if platform.system() == "Windows":
            CREATE_NO_WINDOW = 0x08000000  # Constant for CREATE_NO_WINDOW
            kwargs['creationflags'] = CREATE_NO_WINDOW

        result = subprocess.run(
            ["python", "-m", "pydoc", selected_text],
            **kwargs
        )
        output = result.stdout
        firstbit = output.split('\n')[2].strip()
        nextbit = output.split('\n')[3].strip()
        data = firstbit + "\n" + nextbit
        if data.startswith("class str"):
            return
        elif data.startswith("There are 3 basic"):
            return
        # Update UI with output in the main thread (explained later)
        update_ui_with_output(data)
    except Exception:
        pass

  # Create and start a new thread
  thread = threading.Thread(target=run_subprocess)
  thread.daemon = True  # Set as daemon to avoid blocking program exit
  thread.start()

def update_ui_with_output(output):
  """Updates the UI with the help information in the main thread.

  Args:
    output: The help information retrieved from subprocess.
  """

  index = usertext.index(tk.INSERT)
  bbox = usertext.bbox(index)
  x, y, _, _ = bbox




  newlabel = tk.Label(window,
                        text=output,
                        font=("Cascadia Code", 11),
                        background=config_data['background'],
                        foreground=config_data['textforeground'],
                        highlightcolor=config_data['textforeground'],
                        highlightthickness=3,
                        autostyle=False,)

  # Update UI elements in the main thread using window.after
  window.after(1000, lambda: newlabel.place(x=x, y=y+200))
  window.after(4000, lambda: newlabel.destroy())


def helpinfo(event):
  try:
    selected_text = usertext.selection_get()
  except Exception:
      return
  if selected_text:
    get_help_info(selected_text)
  else:
    newlabel.place_forget()

# usertext.bind("<<Selection>>", helpinfo)
# TODO One day this'll be fixed... that day is not today

vars_tree = tb.Treeview(frame3, height=20, bootstyle="light")
vars_tree["columns"] = ("value")
vars_tree.heading("#0", text="Variable", anchor=tk.CENTER)
vars_tree.heading("value", text="Value", anchor=tk.CENTER)
vars_tree.pack(fill=tk.BOTH, expand=True)

msg = "Variable value will\nbe printed here" # Used this because I had errors displaying multiline in the second var column
# Give a small help info to the user 
vars_tree.insert("", tk.END, text="Click the\nbutton below to\nview variables", values=(msg, ))

varbut = tk.Button(frame3,text='Update Variables',bg='white',command=on_run)
varbut.pack(fill=tk.BOTH)


# Create a button to trigger file creation
def create_template(usertext):
    predefined_directory = "templates" # I really don't know why Google Gemini included this
    filename = simpledialog.askstring("Template Name","Enter the name for your template: ")
    if filename is not None:
        editfile = open(f"templates/{filename}.py","w")
        temptext = usertext.get(1.0,tk.END)
        editfile.write(temptext)
        editfile.close()
    else:
        messagebox.showerror("Error", "Please enter a Name for the Template.")
    del(temptext)

def linenumright():
    linenums.set_justify("right")

def linenumleft():
    linenums.set_justify("left")

def themeselect(themename):
    theme = themename
    with open("settings/currenttheme.txt", "w", encoding="utf-8") as themechange:
        themechange.write(theme)
        themechange.close()
    newtoast = ToastNotification(
        title="Theme Changed!",
        message=f"Theme changed to {theme}.\nRestart to see changes.",
        duration=3000,
        icon="🎨"
    )
    newtoast.show_toast()

def fontchange(fontname):
    thefont = fontname
    with open("settings/font.txt", "w") as fff:
        fff.write(thefont)
        fff.close()
    if thefont == "Consolas": # Handling Consolas font scaling issue
        usertext.config(font=(thefont, 13))
    else: # Other 2 fonts: Segoe UI Semibold and Lucida Console
        usertext.config(font=(thefont, 12))

def changefont(): # Changes reflect without restarting!!! :)
    fontwin = tk.Toplevel()
    fontwin.attributes('-topmost', True)
    fontwin.title("Font")
    fontwin.attributes("-alpha", 0.9)
    tk.Label(fontwin, text="Choose a font to change to:").pack()
    tk.Button(fontwin, text="Segoe UI SemiBold", command=lambda: fontchange("Segoe UI SemiBold"), font=("Segoe UI SemiBold", 10, "bold")).pack(fill=tk.BOTH, pady=10)
    tk.Button(fontwin, text="Cascadia Code Semilight", command=lambda: fontchange("Cascadia Code Semilight"), font=("Cascadia Code Semilight", 10)).pack(fill=tk.BOTH, pady=10)
    tk.Button(fontwin, text="Consolas", command=lambda: fontchange("Consolas"), font=("Consolas", 10)).pack(fill=tk.BOTH, pady=10)
    pywinstyles.change_header_color(fontwin, color=config_data['background'])
    maximize_minimize_button.hide(fontwin)



# Implement the selected font upon restart
# This overrides the initial usertext.config(font=fontnew)
with open("settings/font.txt", "r") as IDK:
    font = IDK.read()
    if font == "Consolas": # Handling consolas seperately
        usertext.config(font=("Consolas", 13))
    else:
        usertext.config(font=(font, 12))


def changetheme(): # Changes only reflect when app restarted
    cwin = tk.Toplevel()
    cwin.attributes('-topmost', True)
    cwin.title("Theme")
    cwin.attributes("-alpha", 1)
    tk.Label(cwin, text="Choose a theme to change to:\n(Changes only reflect when you restart Blueconda)").pack()
    tk.Button(cwin, text="Default", fg="black", bg="white", autostyle=False, borderwidth=3, command= lambda: themeselect("Default")).pack(pady=10, fill=tk.BOTH)
    tk.Button(cwin, text="TreeTrunks (Experimental)", fg="black", bg="#fdf6e3", autostyle=False, borderwidth=3, command=lambda: themeselect("TreeTrunks")).pack(pady=10, fill=tk.BOTH)
    tk.Button(cwin, text="Batman", fg="white", bg="#222222", autostyle=False, borderwidth=3, command=lambda: themeselect("Batman")).pack(pady=10, fill=tk.BOTH)
    tk.Button(cwin, text="DeepBlue", fg="white", bg="#2b3e50", autostyle=False, borderwidth=3, command=lambda: themeselect("DeepBlue")).pack(pady=10, fill=tk.BOTH)
    tk.Button(cwin, text="Solarized", fg="#f8fd62", bg="#002b36", autostyle=False, borderwidth=3, command=lambda: themeselect("Solarized")).pack(pady=10, fill=tk.BOTH)
    pywinstyles.change_header_color(cwin, color=config_data['background'])
    maximize_minimize_button.hide(cwin)


def transluscent():
    window.attributes("-alpha", 0.92)

def opaque():
    window.attributes("-alpha", 1)

def settings(): # TO-DO fix this ugly UI ... NOPE. LATER. Bigger fish to fry.
    genfont = ("Lucida Sans Typewriter",16,"bold")
    setmenu = tk.Toplevel()
    setmenu.attributes('-topmost', True)
    setmenu.attributes("-alpha", 0.9)
    setmenu.configure(bg=config_data['background'])
    setmenu.geometry(f"400x{screen_height}")
    setmenu.title("Settings")
    label1 = tk.Label(setmenu,bg="white",font=genfont,text="Settings")
    label1.pack()
    label2 = tk.Label(setmenu,bg="white",font=fontnew,text="Show Welcome Message")
    label2.pack()
    def switch():
        global is_on
        # Determine is on or off
        if is_on:
            on_button.config(text="Disabled")
            on_button.config(bg="red")
            is_on = False
            with open("settings/showwelcomemessage.txt","w") as op:
                op.write("N")
        else:
            on_button.config(text="Enabled")
            on_button.config(bg="green")
            is_on = True
            with open("settings/showwelcomemessage.txt","w") as op:
                op.write("Y")

               

    # Create A Button
    on_button = tk.Button(
        setmenu,
        command = switch,
        text="Enabled",
        bg="green",
        fg="white",
        )
    on_button.pack(fill=tk.BOTH)
    switch()
    tk.Label(setmenu,bg="white",font=fontnew,text="Line Number Justification:").pack()
    tk.Button(setmenu, text="Justifed Left", command=linenumleft).pack(fill=tk.BOTH, pady=10)
    tk.Button(setmenu, text="Justifed Right", command=linenumright).pack(fill=tk.BOTH)
    setframe = tk.Frame(setmenu, bg="white")
    tk.Label(setframe, text="Automatically save the file\nwhen Run button clicked?").grid(row=0, column=0, padx=40)
    
    def sbr():
        if sbrvar.get() == 1:
            with open("settings/savebeforerun.txt","w") as troll:
                troll.write("Y")
        else:
            with open("settings/savebeforerun.txt","w") as troll:
                troll.write("N")


    sbrvar = tk.IntVar()
    sbrcheck = tb.Checkbutton(setframe, bootstyle="round-toggle", variable=sbrvar, command=sbr)
    sbrcheck.grid(row=0, column=1, padx=20)
    setframe.pack(fill=tk.X, pady=8)
    with open("settings/savebeforerun.txt", "r", encoding="utf=8") as dha:
        saveornot = dha.read()
    if saveornot == "Y":
        sbrcheck.invoke()
    else:
        pass
    tk.Button(setmenu, text="Change Theme", command=changetheme).pack(fill=tk.BOTH, pady=10)
    tk.Button(setmenu, text="Change Font", command=changefont).pack(fill=tk.BOTH, pady=10)
    transparentframe = tb.Frame(setmenu)
    transparentframe.pack(fill=tk.X, pady=5)

    tk.Label(transparentframe, text="Set Window Opacity:").grid(row=0, column=0)
    tk.Button(transparentframe, command=transluscent, text=" Transluscent ").grid(row=0, column=1, padx=4, sticky="EW")
    tk.Button(transparentframe, command=opaque, text="  Opaque  ").grid(row=0, column=2, padx=4, sticky="EW")

    tk.Button(setmenu, text="Swap Icon Pack", command=swap_icons).pack(fill=tk.X, pady=10)

    pywinstyles.change_header_color(setmenu, color=config_data['background'])
    maximize_minimize_button.hide(setmenu)


def get_random_affirmation():
    affims = ["The fact that you're facing this challenge head-on shows your determination and dedication. You've got this!",
               "Remember to celebrate the small victories along the way. Even if the error persists, you're gaining valuable insights with each attempt.",
                 "Mistakes are an essential part of the learning process. You're getting closer to the solution with each error you encounter.", 
                 "Reach out for help and collaborate with other programmers. Sometimes a fresh pair of eyes can spot what you've missed.",
                   "You're a skilled programmer, and this error is just a temporary challenge. Keep going!", "Perseverance is key in programming. Don't give up! Keep troubleshooting, and you'll find that satisfying 'Eureka!' moment.",
                     "Remember, every error you encounter is an opportunity for growth and learning. You're capable of overcoming this challenge!", "Believe in your problem-solving abilities. You've overcome similar hurdles before, and you will conquer this one too.",
                       "Remember, every bug you fix makes your code stronger and more resilient. You're making progress!", 'Take a moment to step back, breathe, and approach the problem from a different angle. A fresh perspective can lead to breakthroughs.',
                         "The best programmers encounter errors regularly. It's a sign that you're exploring new territory and pushing your limits."]
    newaffim = random.choice(affims)
    return newaffim


def sanitize_error_message(error_message):
    """Pull the actual exception line out of a traceback, rather than 
    feeding the whole multi-line blob into the search query."""
    lines = [l.strip() for l in error_message.strip().splitlines() if l.strip()]
    if not lines:
        return ""
    # The real error is almost always the last non-empty line
    last_line = lines[-1]
    # Strip caret pointers like "^" and File "...", line N noise
    last_line = re.sub(r'File\s+".*?",\s*line\s*\d+', '', last_line)
    last_line = last_line.replace('^', '').strip()
    return last_line

def get_clean_error_message(filepath):
    """Run the script directly with plain Python (not friendly) purely to
    get a reliable, standard-format traceback. The last non-empty line of
    a Python traceback is ALWAYS 'ExceptionType: message' — this is
    guaranteed by the language, unlike friendly's decorative formatting."""
    try:
        result = subprocess.run(
            [sys.executable, filepath],
            capture_output=True, text=True, timeout=10
        )
    except subprocess.TimeoutExpired:
        return None

    if result.returncode == 0:
        return None  # script ran fine, no error to search for

    stderr_lines = [l for l in result.stderr.splitlines() if l.strip()]
    if not stderr_lines:
        return None

    return stderr_lines[-1]  # e.g. "SyntaxError: '(' was never closed"

def get_page_title(url, timeout=4):
    """Fetch a readable page title; fall back to domain name if it fails."""
    domain = urlparse(url).netloc.replace('www.', '').split('.')[0]
    try:
        resp = requests.get(url, timeout=timeout, headers={'User-Agent': 'Mozilla/5.0'})
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        title_tag = soup.find('title')
        if title_tag and title_tag.text.strip():
            return f"{domain.capitalize()}: {title_tag.text.strip()}"
    except Exception as e:
        print(f"Could not fetch title for {url}: {e}")
    return f"{domain.capitalize()}: {url}"

def duckduckgo_search(query, num_results=5, timeout=6):
    """Scrape DuckDuckGo's lite HTML endpoint. No API key needed, and it's
    far less aggressive about blocking scrapers than Google."""
    url = "https://lite.duckduckgo.com/lite/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    params = {'q': query}

    try:
        resp = requests.post(url, data=params, headers=headers, timeout=timeout)
        resp.raise_for_status()
    except Exception as e:
        print(f"DuckDuckGo search request failed: {e}")
        return []

    soup = BeautifulSoup(resp.text, 'html.parser')
    links = []

    for a in soup.find_all('a', class_='result-link'):
        href = a.get('href', '')
        if href.startswith('http'):
            links.append(href)
        if len(links) >= num_results:
            break

    # Fallback selector, DDG's lite markup shifts occasionally
    if not links:
        for a in soup.find_all('a'):
            href = a.get('href', '')
            if href.startswith('http') and 'duckduckgo.com' not in href:
                links.append(href)
            if len(links) >= num_results:
                break

    return links


def finderrorlinks(error_message):
    query = f"{sanitize_error_message(error_message)} solution"
    print(f"Searching for: {query}")
    results = []

    urls = duckduckgo_search(query, num_results=5)
    if not urls:
        print("No URLs returned from search - check network/DDG markup changes")
        return results

    for url in urls:
        label = get_page_title(url)
        results.append((label, url))

    return results

def ShowSolutions(err):
    # search_btn.configure(text="Searching...")
    time.sleep(0.3)  # Allow button text to update before search starts (lazy solution)
    link_data = finderrorlinks(err)  # list of (label, url) tuples

    def on_listbox_select(event):
        selected_indices = errlistbox.curselection()
        if selected_indices:
            index = selected_indices[0]
            if 0 <= index < len(link_data):
                webbrowser.open_new_tab(link_data[index][1])

    win = tk.Toplevel()
    # win.attributes('-topmost', True)
    win.attributes("-alpha", 0.9)
    win.configure(bg=config_data["background"])
    win.title("Error Solutions")

    tk.Label(
        win, text="The following solutions were found for your error:\n(Double-Click to open in browser:)",
        background=config_data['background'],
        ).pack(pady=10)
    errlistbox = tk.Listbox(win, font=fontnew, bg=config_data['background'], fg=config_data['textforeground'])
    errlistbox.pack(fill=tk.BOTH, expand=True)

    if link_data:
        for label, url in link_data:
            errlistbox.insert(tk.END, label)
    else:
        errlistbox.insert(tk.END, "No solutions found.")

    errlistbox.bind('<Double-1>', on_listbox_select)

    # Resize the window to fit the listbox content
    win.geometry(f"{screen_width}x{errlistbox.winfo_reqheight()+150}")
    pywinstyles.change_header_color(win, color=config_data['background'])
    maximize_minimize_button.hide(win)
    # search_btn.configure(text="Search for Answer Online")  # Reset button text after search


def runinterminal():
    try:
        subprocess.run(['friendly', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        messagebox.showerror(
            "Friendly Missing",
            "Friendly is not installed.\nUse the Library Manager to install Friendly for Error Msgs.")
        return

    filepath = "temp/qruncodec.py"

    nwin = tk.Toplevel()
    nwin.attributes('-topmost', True)
    nwin.attributes("-alpha", 0.9)
    nwin.minsize(800, 500)
    nwin.title("Error Occured")
    command = f"friendly {filepath}"
    output_text = tb.ScrolledText(nwin, wrap="word")
    output_text.pack(fill=tk.BOTH, expand=True)
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    newsd = str(result.stdout).replace("|", "")
    newsr = str(result.stderr).replace("|", "")

    full_output = newsd + newsr
    lines = full_output.splitlines()
    trimmed_lines = lines[2:-2] if len(lines) > 4 else lines
    trimmed_text = "\n".join(trimmed_lines).strip()

    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, trimmed_text + "\n\n" + get_random_affirmation())
    output_text.config(state="disabled")

    # Get a clean, reliable error message separately - not from friendly's
    # decorated text, but from a plain Python run of the same file.
    errormsg = get_clean_error_message(filepath)
    print(f"Extracted errormsg: {errormsg!r}")  # debug line, remove once confirmed working

    search_btn = tk.Button(
        nwin, text="Search for Answer Online",
        command=lambda: ShowSolutions(errormsg) if errormsg else messagebox.showinfo("No Error", "No error was detected to search for.")
    )
    search_btn.pack(fill=tk.BOTH, expand=True, pady=8)


    pywinstyles.change_header_color(nwin, color=config_data['background'])
    maximize_minimize_button.hide(nwin)


def install_dependencies():

    dependencies = ["friendly", "flake8", "pyinstaller"]

    def run_installs():
        install_btn.config(state="disabled", text="Installing...")
        output_text.config(state="normal")
        output_text.delete("1.0", tk.END)

        for package in dependencies:
            output_text.insert(tk.END, f"--- Installing {package} ---\n")
            output_text.see(tk.END)
            output_text.update_idletasks()

            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", package],
                capture_output=True, text=True
            )

            output_text.insert(tk.END, result.stdout)
            if result.stderr:
                output_text.insert(tk.END, result.stderr)

            if result.returncode == 0:
                output_text.insert(tk.END, f"--- {package} installed successfully ---\n\n")
            else:
                output_text.insert(tk.END, f"--- {package} FAILED to install ---\n\n")

            output_text.see(tk.END)
            output_text.update_idletasks()

        output_text.insert(tk.END, "All installations finished.")
        output_text.see(tk.END)
        output_text.config(state="disabled")
        install_btn.config(state="normal", text="Click to Begin Installing Dependencies")

    def start_install_thread():
        if checkwifistatus(): # Ensure wifi is working
        # Run in a separate thread so the pip install output can stream
        # into the text widget live, instead of freezing the whole GUI
        # until all installs finish.
            threading.Thread(target=run_installs, daemon=True).start()
        else: # Deploy error message
            messagebox.showerror("No WiFi", "Please check your WiFi connection and try again.")

    win = tk.Toplevel()
    win.attributes('-topmost', True)
    win.attributes("-alpha", 0.9)
    win.configure(bg=config_data["background"])
    win.title("Installing Dependencies")

    install_btn = tk.Button(win, text="Click to Begin Installing Dependencies", command=start_install_thread)
    install_btn.pack(fill=tk.BOTH, pady=8)

    output_text = tb.ScrolledText(win, wrap="word")
    output_text.pack(fill=tk.BOTH, expand=True)

    # Pre-fill the list of what will be installed, before the button is pressed
    output_text.insert(tk.END, "Dependencies to install:\n")
    for package in dependencies:
        output_text.insert(tk.END, f" - {package}\n")
    output_text.config(state="disabled")

    pywinstyles.change_header_color(win, color=config_data['background'])
    maximize_minimize_button.hide(win)

def DependencyManager():
    '''
    Launches dependency installation in a new thread.
    '''
    installerthread = threading.Thread(target=install_dependencies)
    installerthread.start()

# Poorly written function, its almost three years old and never got rewritten 
# since it... somehow still works fine
def quickrunmain():
    qrunfile = open("temp/qruncodec.py","w",encoding='utf-8')
    qrunfile.write("import os")
    qrunfile.close()
    qrunfile = open("temp/qruncodec.py","a",encoding='utf-8')
    qrunfile.write("\n")
    qruncode = usertext.get(1.0,tk.END)
    qrunfile.write(qruncode)
    qrunfile.close()
    qrunfile = open("temp/qruncodec.py","a",encoding='utf-8')
    qrunfile.write("\n")
    qrunfile.write("os.system('pause')")
    qrunfile.close()
    result = os.system("python temp/qruncodec.py")
    if result != 0:
        runinterminal()



def quickrun(usertext):
    thread = threading.Thread(target=quickrunmain)
    thread.start()
'''
            result = subprocess.run(["python", "temp/qruncodec.py"], capture_output=True)
            result.check_returncode()
        except subprocess.CalledProcessError as error:
            error_message = error.stderr.decode()
            messagebox.showerror("Error", f"A problem occurred:\n{error_message}")
 
    else:
        messagebox.showinfo("Task Preview","Code ran sucessfully.")
    del(qruncode)
'''

def textfind(event=None): # REDACTED
    # Clear existing tags
    usertext.tag_remove('found', '1.0', tk.END)
    # Get text to find
    find_text = simpledialog.askstring("Find", "Text to Find:")
    if find_text:
        idx = '1.0'
        while True:
            # Search for occurrence
            idx = usertext.search(find_text, idx, nocase=1, stopindex=tk.END)
            if not idx:
                break
            lastidx = '%s+%dc' % (idx, len(find_text))
            # Tag and highlight
            usertext.tag_add('found', idx, lastidx)
            idx = lastidx
        # Set highlight color
        usertext.tag_config('found', foreground='black', background='yellow')



def textfindnew(event):
    def find(*args):
        # remove tag 'found' from index 1 to END
        usertext.tag_remove('found', '1.0', tk.END)

        # returns to widget currently in focus
        s = findentry.get()

        if (s):
            idx = '1.0'
            while 1:
                # searches for desried string from index 1
                idx = usertext.search(s, idx, nocase=1,
                                stopindex=tk.END)

                if not idx: break
                # last index sum of current index and
                # length of text
                lastidx = '% s+% dc' % (idx, len(s))
                # overwrite 'Found' at idx
                usertext.tag_add('found', idx, lastidx)
                idx = lastidx

            # mark located string as green and bg = ''yellow
            usertext.tag_config('found', foreground='black', background='cyan')
        findentry.focus_set()
    def REFFUNC():
        usertext.tag_delete('found')
    
    def findandreplace(*args):
        # remove tag 'found' from index 1 to END
        usertext.tag_remove('found', '1.0', tk.END)

        # returns to widget currently in focus
        s = findentry.get()
        r = replaceentry.get()

        if (s and r):
            idx = '1.0'
            while 1:
                # searches for desried string from index 1
                idx = usertext.search(s, idx, nocase=1,
                                stopindex=tk.END)
                print(idx)
                if not idx: break

                # last index sum of current index and
                # length of text
                lastidx = '% s+% dc' % (idx, len(s))

                usertext.delete(idx, lastidx)
                usertext.insert(idx, r)

                lastidx = '% s+% dc' % (idx, len(r))

                # overwrite 'Found' at idx
                usertext.tag_add('found', idx, lastidx)
                idx = lastidx

            # mark located string as green and bg = ''yellow
            usertext.tag_config('found', foreground='blue', background='cyan')
        findentry.focus_set()

    finwin = tk.Toplevel(width=50, height=500)
    finwin.attributes('-topmost', True)
    finwin.attributes("-alpha", 0.9)
    finwin.title("Find/Replace")
    findentry = tk.Entry(finwin,width=40)
    findentry.grid(row=0,column=1)
    findlabel = tk.Label(finwin,text="Find:")
    findlabel.grid(row=0,column=0)

    replaceentry = tk.Entry(finwin,width=40)
    replaceentry.grid(row=1,column=1)
    replacelabel = tk.Label(finwin,text="Replace With:")
    replacelabel.grid(row=1,column=0)

    findbutton = tk.Button(finwin,text="Find", command=find)
    findbutton.grid(row=2,column=1, pady=7, columnspan=3,sticky="EW")

    findrepbutton = tk.Button(finwin,text="Find And Replace", command=findandreplace)
    findrepbutton.grid(row=3,column=1, pady=7, columnspan=3,sticky="EW")

    refbutton = tk.Button(finwin,text="Remove Highlights", command=REFFUNC)
    refbutton.grid(row=4,column=1, pady=7, columnspan=3,sticky="EW")
    pywinstyles.change_header_color(finwin, color=config_data['background'])
    maximize_minimize_button.hide(finwin)

usertext.bind("<Control-f>", textfindnew)

#FUNC FOR COLOURADD
def inscolour():
    cd = ColorChooserDialog()
    cd.show()
    colors = cd.result
    index = usertext.index(tk.INSERT)
    usertext.insert(index, colors.hex)
#FUNC COLORDD END
        
#FUNCS FOR FILES]]

file_path = None
default_dir = os.path.join(os.path.expanduser('~'), 'Downloads')


def update_title(file_path):
    if file_path:
        window.title("Blueconda - " + file_path)
    else:
        window.title("Blueconda Editor 1.0")
        file_path = None
        with open("temp/currentfile.txt","w") as dr:
          dr.write(" ")
          

def openfileregular():
    file_path = filedialog.askopenfilename(
            title="Open File",
            filetypes=[("Python files", "*.py")],
            initialdir=default_dir,
        )
    if file_path:
        with open(file_path, "r", encoding="utf-8") as f:
            usertext.delete("1.0", tk.END)
            usertext.insert("1.0", f.read())
        update_title(file_path)
        tag_all()
        with open("temp/currentfile.txt","w") as rw:
            rw.write(file_path)


def open_file(): 
    global file_path, file_loaded

    file_path = filedialog.askopenfilename(    # Below this line is the list
        title="Open File (py, py3, pyw, pyi)", # of supported filetypes for Blueconda
        filetypes=[("Python files", ["*.py"  ,    "*.py3",    "*.pyw",    "*.pyi"]  )],
        initialdir=default_dir,
    )
    
    if file_path: # ERRORLOCATEDHERE
        with open(file_path, "r", encoding="utf-8") as f:
            usertext.delete("1.0", tk.END)
            usertext.insert("1.0", f.read())
        update_title(file_path)
        tag_all()
        with open("temp/currentfile.txt","w", encoding="utf-8") as rw:
            rw.write(file_path)
    file_loaded = True
    usertext.edit_modified(False)



def save_file_as():
    file_path = filedialog.asksaveasfilename(
        title="Save File As",
        filetypes=[("Python files", "*.py")],
        initialdir=default_dir,
    )
    
    if file_path:
        with open(file_path + ".py", "w", encoding="utf-8") as f:
            f.write(usertext.get("1.0", tk.END))
        update_title(file_path + ".py")
        with open("temp/currentfile.txt","w", encoding="utf-8") as rw:
            rw.write(file_path + ".py")

def mark_as_saved():
  """Call this inside your existing SAVE function."""
  global unsaved_label, usertext

  # Reset the tkinter text widget's internal modification flag
  if "usertext" in globals():
    usertext.edit_modified(False)

  # Hide the warning label
  if unsaved_label:
    unsaved_label.grid_forget()

# Had to make this earlier to prevent errors
menuframe = tk.Frame(window, bg=config_data["background"])
menuframe.grid(row=0, column=0, columnspan=5, sticky="EW")

def save_file():
    with open("temp/currentfile.txt","r", encoding="utf-8") as cf:
        newfilepath = cf.read()
    try:
        with open(newfilepath, "w") as f:
            f.write(usertext.get("1.0", tk.END))
            # Show a small success message!
        toast = ToastNotification(
        title="Saved",
        message="Your changes have been saved successfully!",
        duration=1000,
        icon="💾",
        position=[300, 200, "nw"],
        alert=True,
        )
        toast.show_toast()
        mark_as_saved()
    except Exception:
        save_file_as()
    
def create_unsaved_indicator(parent_window, save_button):
  """Call this once during setup to create the hidden warning label."""
  global unsaved_label, menuframe

  with open("settings/font.txt", "r") as file:
    font_name = file.read().strip()

  # Create the label (styled to look like a notification/button)
  unsaved_label = ttk.Label(
      menuframe,
      text="⚠ Unsaved Changes. Click to Save.",
      background= config_data["f_string"],
      foreground= config_data["keyword"],
      borderwidth=2,
      relief="solid",
      font=(font_name, 9, "bold"),
      cursor="hand2",
  )
  # Clicking the warning label can also trigger the save function
  unsaved_label.bind("<Button-1>", lambda e: save_file())
  # Hide it initially by default
  unsaved_label.grid_forget()

def new_file():
    if usertext.edit_modified():
        response = messagebox.askyesno(
            title="Save Changes",
            message="Do you want to save your changes before creating a new file?",
        )
        if response:
            save_file_as()
            
    usertext.delete("1.0", tk.END)
    update_title(None)
    with open("temp/currentfile.txt", "w", encoding="utf-8") as tree:
        tree.write("")
        tree.close()
    
######################################

    
def doceditor():
    try:
        subprocess.Popen(["MDEditor.exe"])
    except Exception:
        build_exe("MDEditor.py","MDEditor.exe",False)

    # Continue with Python code while the .exe runs
    #process.wait()

######################################
#FUNCS FOR FILES END
    
is_hovering = False

def enter_function(event):
  global is_hovering
  is_hovering = True

def leave_function(event):
  global is_hovering
  is_hovering = False


def update_memory_usage():
    global usage_percent
    memory_usage = psutil.virtual_memory()
    usage_percent = memory_usage.percent
    # Update progressbar value and label
    memory_bar['value'] = usage_percent
    # Schedule next update after 1 second
    #ToolTip(memory_bar, text=f"Memory usage: {usage_percent}%")
    if is_hovering:

        disp = tk.Label(text=f'Memory usage: {usage_percent}%')
        disp.grid(row=3, column=3, sticky='e')
        disp.after(1000, lambda: disp.destroy())
        if usage_percent > 85:
            disp.config(fg='red')
            memory_bar.config(bootstyle="warning")
        else:
            disp.config(fg="#4bb1ea")
            memory_bar.config(bootstyle='primary')
    window.after(100, update_memory_usage)    

memory_bar = tb.Progressbar(window, orient="horizontal", mode="determinate", maximum=100, cursor='dot', bootstyle="striped")
memory_bar.grid(row=3,column=4,padx=20,sticky="e")
update_memory_usage()

memory_bar.bind("<Enter>", enter_function)
memory_bar.bind("<Leave>", leave_function)
memory_bar.bind("<Button-1>", lambda e: ResourceUsageWindow())


# ---------- SETTINGS FILE HANDLING ----------

SETTINGS_FILE = "settings/ai_settings.txt"

def load_ai_settings():
    global model
    if not os.path.exists(SETTINGS_FILE):
        return None
    try:
        with open(SETTINGS_FILE, "r") as file:
            lines = file.read().splitlines()
        api_key = lines[0]
        model_name = lines[1]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        return True
    except Exception:
        # File exists but is broken/empty/invalid -> treat as "not configured"
        return None


def save_ai_settings(api_key):
    global model
    selected_model = model_var.get()
    with open(SETTINGS_FILE, "w") as file:
        file.write(api_key + "\n")
        file.write(selected_model + "\n")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(selected_model)
    messagebox.showinfo("Saved", "AI Settings have been saved.")
    settings_win.destroy()


# ---------- AI SETTINGS MENU (RIGHT CLICK) ----------

def use_api_key():
    global model_var, model_dropdown

    api_key = api_key_entry.get()
    if api_key == "":
        messagebox.showerror("Error", "Please enter an API Key.")
        return

    try:
        genai.configure(api_key=api_key)
        all_models = genai.list_models()
    except Exception as exception:
        messagebox.showerror("Error", f"Could not use this API Key.\n{exception}")
        return

    text_model_names = []
    for m in all_models:
        # Only keep models that can actually output TEXT (generateContent)
        if "generateContent" in m.supported_generation_methods:
            text_model_names.append(m.name)

    if len(text_model_names) == 0:
        messagebox.showerror("Error", "No text generation models found for this API Key.")
        return

    model_var.set(text_model_names[0])
    model_dropdown["menu"].delete(0, "end")
    for name in text_model_names:
        model_dropdown["menu"].add_command(label=name, command=lambda value=name: model_var.set(value))

    model_dropdown.grid(row=5, column=0, columnspan=2, pady=5)
    save_button.grid(row=6, column=0, columnspan=2, pady=10)


def open_ai_settings(event=None):
    global api_key_entry, model_var, model_dropdown, settings_win, save_button

    win = tb.Toplevel()
    win.attributes('-topmost', True)
    win.attributes("-alpha", 0.9)
    win.configure(bg=config_data["background"])
    win.title("AI Settings")
    settings_win = win

    tb.Label(win, text="Enter API Key:").grid(row=0, column=0, columnspan=2, pady=5, padx=5)
    api_key_entry = tb.Entry(win, width=40)
    api_key_entry.grid(row=1, column=0, columnspan=2, padx=5)

    use_button = tb.Button(win, text="USE", command=use_api_key)
    use_button.grid(row=2, column=0, columnspan=2, pady=10, sticky="EW")

    tb.Button(win, command=lambda:webbrowser.open_new_tab("https://aistudio.google.com/api-keys"), text="Get API Key...").grid(row=3, column=0, columnspan=1, pady=10, sticky="EW")
    tb.Button(win, command=lambda:webbrowser.open_new_tab("https://aistudio.google.com/rate-limit"), text="Rate Limits").grid(row=3, column=1, columnspan=1, pady=10, sticky="EW")

   
    tb.Label(win, text="Choose a Model:").grid(row=4, column=0, columnspan=2)

    model_var = tk.StringVar(win)
    model_dropdown = tb.OptionMenu(win, model_var, "")
    # not gridded yet, appears only after USE succeeds

    save_button = tb.Button(win, text="Save Settings", command=lambda: save_ai_settings(api_key_entry.get()))
    # not gridded yet either, appears only after USE succeeds

    pywinstyles.change_header_color(win, color=config_data['background'])
    maximize_minimize_button.hide(win)


def checkwifistatus(): # Function to check if WiFi is working
    try:
        request = requests.get("https://google.com", timeout=10) # Send Requests to a Server (google)
        del(request) # Manually delete request data to prevent clogging of memory
        return True # Requests came through so internet is active
    except (requests.ConnectionError,requests.Timeout) as exception:
        return  False # Requests failed so internet is not working

# Data for AI Model
# The following code used to remove markdown formatting (credit to Pavel Vorobyov, stackoverflow)

def unmark_element(element, stream=None):
    if stream is None:
        stream = StringIO()
    if element.text:
        stream.write(element.text)
    for sub in element:
        unmark_element(sub, stream)
    if element.tail:
        stream.write(element.tail)
    return stream.getvalue()
# patching Markdown
Markdown.output_formats["plain"] = unmark_element
__md = Markdown(output_format="plain")
__md.stripTopLevelTags = False



def unmark(text):
    return __md.convert(text)

def getaianswer():
    tag_name = "blue_text"
    anstext.tag_configure(tag_name, foreground=config_data['operator'])

    question = qentry.get()
    qentry.delete(0, tk.END)
    anstext.insert(tk.END,f"\n\nYou: {question}\n\n" , tag_name)
    response = chat.send_message(question, stream=False)
    text = unmark(response.text)
    for char in text:
        anstext.insert(tk.END, char)
        anstext.update()  # Update the GUI to display the new character
        anstext.see(tk.END)
        time.sleep(0.01)


def aiask(): 
    global anstext
    global qentry
    global chat
    global model

    configured = load_ai_settings()
    if configured is None:
        open_ai_settings()
        return

    WiFiStatus = checkwifistatus()
    if WiFiStatus == False: # Check WiFi by trying to send requests (prevent funny errors if WiFi not working)
        messagebox.showerror("Error", "Could Not Connect to Server.\n Please check your internet connection.")
        return
    aiwindow = tb.Toplevel()
    aiwindow.attributes('-topmost', True)
    aiwindow.attributes("-alpha", 0.9)
    # aiwindow.geometry("800x600")
    aiwindow.title("Ask AI")
    chat = model.start_chat() # Start the chat Session
    tb.Label(aiwindow, text="Enter your question here:").grid(row=2, column=0, columnspan=2)
    qentry = tb.Entry(aiwindow, width=50)
    qentry.grid(row=3, column=0, pady=5)
    qbutton = tb.Button(aiwindow, text="    Ask    ", command=getaianswer)
    qbutton.grid(row=3, column=1, columnspan=2)
    tb.Label(aiwindow, text="Your Answer appears here: (Click once and Wait)").grid(row=0, column=0, columnspan=2)
    #                                                   ^ Added because of the absence of a loading screen
    anstext = tb.Text(aiwindow, width=56, height=12, wrap="word")
    anstext.grid(row=1, column=0, columnspan=2, pady=8)

    qentry.bind("<Return>", lambda event: getaianswer())

    scrollbar_x2 = tb.Scrollbar(aiwindow, orient="vertical")
    anstext.config(yscrollcommand=scrollbar_x2.set)
    scrollbar_x2.config(command=anstext.yview)
    scrollbar_x2.grid(row=1,column=2, sticky="WNS")
    scrollbar_x2.config(cursor=' sb_v_double_arrow ')
    pywinstyles.change_header_color(aiwindow, color=config_data['background'])
    maximize_minimize_button.hide(aiwindow)


def tip():
    python_tips = [
    "Use f-strings for clean string formatting:\n| name = 'Alice'\n greeting = f'Hello, {name}!'",
    "Don't be ashamed to use Stack Overflow or AI. All programmers do it.",
    "The bar at the bottom right of the Blueconda Editor displays how much of your RAM is occupied.\nHover over it to see the value as a percentage",
    "Leverage list comprehensions for concise data manipulation:\n|numbers = [x for x in range(10) if x % 2 == 0]",
    "Get type information about a variable using the built-in type() function:\n|data = 42\n data_type = type(data)",
    "Explore built-in functions like filter() and map() for functional programming: \n|doubled_numbers = list(map(lambda x: x * 2, [1, 2, 3]))",
    "Utilize the powerful NumPy library for numerical computations: \n|import numpy as np\n array = np.array([1, 2, 3])",
    "Work with data structures efficiently using the Pandas library: \n|import pandas as pd\n data = pd.DataFrame({'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']})",
    "Visualize data with Matplotlib for clear insights: \n|import matplotlib.pyplot as plt\n plt.plot([1, 2, 3], [4, 5, 6])\n plt.show()",
    "Regular expressions with the re library for powerful text processing: \n|import re\n match = re.search(r'\d+', 'hello123world')",
    "Access web data using the requests library for web scraping and APIs: \n|import requests\n response = requests.get('https://www.example.com')",
    "Use `len()` to get the length of a sequence (string, list, tuple):\n|my_string = 'hello'\n string_length = len(my_string)",
    "Remove elements from a list using `del`:\n|my_list = [1, 2, 3]\n del my_list[1]",  # Remove element at index 1
    "Select a random element from a sequence with `random.choice()`:\n|import random\n random_item = random.choice(['apple', 'banana', 'cherry'])",
    "Get the current time in seconds since the epoch with `time.time()`:\n|import time\n current_time = time.time()",
    "Format time objects into readable strings using `time.strftime()`:\n|import time\n current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())",
    "Convert data types using built-in functions like `int()`, `float()`, and `str()`:\n|num_str = '42'\n number = int(num_str)",
    "Enumerate a sequence to get both index and element as a tuple pair: \n|for index, item in enumerate(['apple', 'banana', 'cherry']):\n  print(index, item)",
    "Use `zip()` to combine elements from multiple iterables into tuples: \n|names = ['Alice', 'Bob', 'Charlie']\n ages = [25, 30, 28]\n for name, age in zip(names, ages):\n  print(f'{name} is {age} years old')",
    "Sort a list in-place with `list.sort()`:\n|my_list = [3, 1, 4, 2]\n my_list.sort()",
    "Reverse the order of elements in a list with `list.reverse()`:\n|my_list = [1, 2, 3]\n my_list.reverse()",
    "Copy a list to create a new independent list with `list()` or `slice notation`:\n|original_list = [1, 2, 3]\n copy_list = list(original_list)",
    "Make your program more memory efficient by deleting variables after you don't need them.\n|var = 213\ndel(var)",
    "Avoid `IndexError` by checking list/string bounds before accessing elements: \n|my_list = ['apple', 'banana']\n if len(my_list) > 1: \n  print(my_list[1])",  # Check length before accessing element at index 1
    "Use `try-except` blocks to gracefully handle potential errors, such as when accessing dictionaries: \n|my_dict = {'name': 'Alice'}\n try: \n  value = my_dict['age']  # Might raise KeyError if 'age' doesn't exist\n except KeyError: \n  value = 'Unknown'",
    "Prevent `TypeError` by ensuring operations are performed on compatible data types: \n|num1 = 5\n num2 = '10'\n try: \n  # This would raise TypeError (can't add int and string)\n  result = num1 + num2\n except TypeError: \n  print('Incompatible data types for operation')",
    "Be mindful of `NameError` by ensuring variables are defined before use: \n|greeting = 'Hello, world!'\n print(message)",  # 'message' is not defined before use
    "Use descriptive variable names to avoid potential `NameError` due to typos",
    "Utilize clear and consistent indentation to prevent `IndentationError`:\n|  if x > 0:  # Correct indentation\n   print('Positive')\n  else:  # Correct indentation\n   print('Non-positive')",
    "Variables within a function should be global if you want them accessed outside the function.\n|def func():\n    global username\n    username = input('Enter username')",
    "Utilize Blueconda's builtin markdown editor to write documentation for your code\n before uploading to platforms such as Github",
    "Use Blueconda's builtin color picker to create custom colors and insert them into\n your code as HEX.",
    "When opening files using open(), use encoding UTF-8 to make sure you code raises no Unicode Errors.\n|with open('myfile.txt','w', encoding='utf-8') as f:\n    f.write('New Text')",
    ]
    newtip = random.choice(python_tips)
    newwin = tk.Toplevel()
    newwin.attributes("-alpha", 0.9)
    newwin.title("Tip")
    if config_data["themename"] == "superhero": # ttkbootstrap theme for DeepBlue
        cls = "mariana"
    elif config_data["themename"] == "cerculean": # ... Default and TreeTrunks
        cls = "ayu-light"
    elif config_data["themename"] == "darkly": # ... Batman
        cls = "ayu-dark"
    elif config_data["themename"] == "solar": # ... Solarized
        cls = "dracula"
    codeview = CodeView(newwin, lexer=pygments.lexers.PythonLexer, color_scheme=cls) # CodeView Widget for Tips
    seperated = newtip.split("|") # To get the tip and the code
    if len(seperated) == 1: # Just code no tip
        tk.Label(newwin, text="Tip", font=("Cascadia Code", 20), fg=config_data['textforeground'], bg=config_data['background'], autostyle=False).pack()
        tk.Label(newwin, text=newtip, justify='left', font=("Cascadia Code", 16), bg=config_data['background'], fg=config_data['textforeground'], autostyle=False).pack()
    else:
        thetip = seperated[0] # The tip goes into the text
        thecode = seperated[1] # C0de goes into the codebox
        tk.Label(newwin, text="Tip", font=("Cascadia Code", 20), fg=config_data['textforeground'], bg=config_data['background'], autostyle=False).pack()
        tk.Label(newwin, text=thetip, justify='left', font=("Cascadia Code", 16), bg=config_data['background'], fg=config_data['textforeground'], autostyle=False).pack()
        codeview.insert(1.0, thecode)
        codeview.pack(fill="both", expand=True)
    pywinstyles.change_header_color(newwin, color=config_data['background'])
    maximize_minimize_button.hide(newwin) # looks cleaner

# Code for GUIBuilder runner
def guibuilder():
    try:
        process = subprocess.Popen(["GUIBuilder.exe"])
        # process.wait() commenting this out keeps the UI active whilst GUIbuilder is open
    except Exception: # This is used for people who are building from source and don't have .exe
        build_exe("GUIBuilder.py","GUIBuilder.exe", False)

def pythonrun():

    with open("temp/currentfile.txt", "r", encoding="utf=8") as dhamaka:
        pathway = dhamaka.read().strip()
        print(pathway)
        if len(str(pathway)) < 2:
            save_file_as()
            return
        
    with open("settings/savebeforerun.txt", "r", encoding="utf=8") as dha:
        saveornot = dha.read()  
    if saveornot == "Y":
        save_file()
    else:
        pass

    full_path = os.path.abspath(pathway)

    # Store the current directory to revert later
    current_dir = os.getcwd()
    
    # Get the script's directory
    script_dir = os.path.dirname(os.path.abspath(full_path))

    # Change the working directory to the script's location (temporary)
    # This chdir function is now useless; it was for Method 1 but I'm keeping it
    os.chdir(script_dir)

    """Method 1: subprocess.call() had some errors"""
    # Execute the script using subprocess (handles spaces in file path)
    #result = subprocess.call(["python", os.path.basename(full_path)])
    #if result != 0:
    #    save_file_as()
    #else:
    #    messagebox.showinfo("Task Preview", "Code ran successfully.")
    """Method 2: os.startfile() works but limited"""
    #os.startfile(full_path)

    """Method 3: Using cmd (current preferred method)"""

    subprocess.call(f'start cmd /K python "{full_path}"', shell=True)

    # NEW: the cmd /K window above runs detached and async, so its return
    # code doesn't tell us if the script actually errored. To check, we run
    # the same script a second time, silently, in the background, purely to
    # detect success/failure - the visible cmd window above is untouched.
    check_for_errors(full_path)

    # Change back the directory
    os.chdir(current_dir)


def check_for_errors(full_path, timeout=10):
    """Silently re-runs the script to detect if it errors. If it does,
    pulls up the Friendly traceback window for the user."""
    try:
        result = subprocess.run(
            [sys.executable, full_path],
            capture_output=True, text=True, timeout=timeout
        )
    except subprocess.TimeoutExpired:
        # Script is likely waiting on input() or running long - can't
        # reliably judge success/failure here, so just skip the popup
        return

    if result.returncode != 0:
        show_friendly_traceback(full_path)

# This function had to be redone here because it wasn't fully usable
# From outside the Quick Run.
# Ideally it'd be one function but this is a lazy fix, TWO identical functions.
def show_friendly_traceback(filepath):
    """Displays a Friendly traceback window for the given script, same
    style as runinterminal(), but parameterized so it works for any file
    instead of being hardcoded to temp/qruncodec.py."""
    try:
        subprocess.run(['friendly', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        messagebox.showerror(
            "Friendly Missing",
            "Friendly is not installed.\nUse the Library Manager to install Friendly for Error Msgs.\nCommand: pip install friendly")
        return

    nwin = tk.Toplevel()
    nwin.attributes('-topmost', True)
    nwin.attributes("-alpha", 0.9)
    nwin.minsize(800, 500)
    nwin.title("Error Occured")
    command = f'friendly "{filepath}"'
    output_text = tb.ScrolledText(nwin, wrap="word")
    output_text.pack(fill=tk.BOTH, expand=True)
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    newsd = str(result.stdout).replace("|", "")
    newsr = str(result.stderr).replace("|", "")

    full_output = newsd + newsr
    lines = full_output.splitlines()
    trimmed_lines = lines[2:-2] if len(lines) > 4 else lines
    trimmed_text = "\n".join(trimmed_lines).strip()

    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, trimmed_text + "\n\n" + get_random_affirmation())
    output_text.config(state="disabled")

    errormsg = get_clean_error_message(filepath)
    print(f"Extracted errormsg: {errormsg!r}")  # debug line, remove once confirmed working

    search_btn = tk.Button(
        nwin, text="Search for Answer Online",
        command=lambda: ShowSolutions(errormsg) if errormsg else messagebox.showinfo("No Error", "No error was detected to search for.")
    )
    search_btn.pack(fill=tk.BOTH, expand=True, pady=8)

    pywinstyles.change_header_color(nwin, color=config_data['background'])
    maximize_minimize_button.hide(nwin)
'''
#Code to Run with Threading for Terminate | pythonrunV2
script_thread = None

def run_script_in_thread(file_path):
    try:
        subprocess.run(["python", file_path], check=True)
    except subprocess.CalledProcessError as e:
        # Handle errors here, e.g., display a message box
        pass

def pythonrun():
    with open("temp/currentfile.txt", "r", encoding="utf=8") as dhamaka:
        pathway = dhamaka.read().strip()
        print(pathway)
        if len(str(pathway)) < 2:
            save_file_as()
            return

    full_path = os.path.abspath(pathway)

    # Store the current directory to revert later
    current_dir = os.getcwd()

    # Get the script's directory
    script_dir = os.path.dirname(os.path.abspath(full_path))

    # Change the working directory to the script's location (temporary)
    os.chdir(script_dir)

    # Create a thread for running the script
    global script_thread
    script_thread = threading.Thread(target=run_script_in_thread, args=(full_path,))
    script_thread.start()

    # Change back the directory
    os.chdir(current_dir)

def terminate_script(event=None):
    global script_thread
    if script_thread and script_thread.is_alive():
        script_thread.terminate()
    else:
        # Handle cases where the thread is already terminated or not running
        messagebox.showinfo("Info", "Script is not running or already terminated.")

window.bind("<Control-t>", terminate_script)
'''

def pythonrun_throughsourceruntime():
    # Read the current file path
    with open("temp/currentfile.txt", "r", encoding="utf-8") as dhamaka:
        pathway = dhamaka.read().strip()
        print(pathway)
        if len(str(pathway)) < 2:
            save_file_as()
            return

    # Check save-before-run setting
    with open("settings/savebeforerun.txt", "r", encoding="utf-8") as dha:
        saveornot = dha.read()
    if saveornot == "Y":
        save_file()

    full_path = os.path.abspath(pathway)
    current_dir = os.getcwd()
    script_dir = os.path.dirname(full_path)

    def run_in_thread():
        import io, contextlib, traceback
        # Fresh isolated namespace each run — like running from terminal
        namespace = {
            "__name__": "__main__",
            "__builtins__": __builtins__,
            "__file__": full_path,
        }
        modules_before = set(sys.modules.keys())
        os.chdir(script_dir)
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                code = f.read()
            stdout_capture = io.StringIO()
            with contextlib.redirect_stdout(stdout_capture):
                exec(compile(code, full_path, "exec"), namespace)
            output = stdout_capture.getvalue()
            if output:
                print(output)  # replace with your IDE output panel
        except Exception:
            print(traceback.format_exc())  # replace with your IDE output panel
        finally:
            # Clean up any modules the user's script imported
            for mod in set(sys.modules.keys()) - modules_before:
                del sys.modules[mod]
            os.chdir(current_dir)

    """Method 1: subprocess.call() had some errors"""
    #result = subprocess.call(["python", os.path.basename(full_path)])
    #if result != 0:
    #    save_file_as()
    #else:
    #    messagebox.showinfo("Task Preview", "Code ran successfully.")
    """Method 2: os.startfile() works but limited"""
    #os.startfile(full_path)
    """Method 3: Using cmd (current preferred method)"""
    #subprocess.call(f'start cmd /K python "{full_path}"', shell=True)
    """Method 4: In-process exec() — fresh namespace each run, isolated like terminal.
    Runs in a daemon thread so the IDE UI stays responsive during execution.
    The thread genuinely runs on a separate core if using a free-threaded Python
    build (3.13t / 3.14t) where the GIL is disabled (sys._is_gil_enabled() == False).
    On a standard GIL build it still keeps the UI unblocked via context switching."""
    t = threading.Thread(target=run_in_thread, daemon=True)
    t.start()


def on_text_modified(event=None):
  """Bound to the text widget to detect edits."""
  global file_loaded, unsaved_label, usertext, savefilebutton

  # Only trigger if a file has actually been opened and the widget exists
  if file_loaded and unsaved_label and savefilebutton:
    # Check if the text widget is currently modified
    if usertext.edit_modified():
      # Position it right underneath the save button dynamically
      # Get the save button's geometry relative to its parent
      bx = savefilebutton.winfo_x()
      by = savefilebutton.winfo_y()
      bh = savefilebutton.winfo_height()

      # Place the label right under the save button
      # Place the label right under the save button
      unsaved_label.grid(row=0, column=3, sticky="W")  # Adjust padding as needed
    else:
      # If modified is False (e.g. after a save), forcefully hide the label
      unsaved_label.grid_forget()
usertext.bind("<<Modified>>", on_text_modified)

# -----------------
# Code For Buttons
# -----------------

# NOTE: Not in correct order

# Open File
openfile= tk.PhotoImage(file='src/opennew.png')
openfilelabel= tk.Label(image=openfile)
openfilebutton= tk.Button(C, image=openfile, command=open_file, cursor="dot",
borderwidth=0,highlightthickness = 0,bd = 0,bg = config_data['background'],activebackground = config_data['background'], autostyle=False)
openfilebutton.grid(row=0,column=4,padx=3)

# Save File
savefile= tk.PhotoImage(file='src/savefile.png')
savefilelabel= tk.Label(image=savefile)
savefilebutton= tk.Button(C, image=savefile, command= save_file,cursor="dot",
borderwidth=0,highlightthickness = 0,bd = 0,bg = config_data['background'],activebackground = config_data['background'], autostyle=False)
savefilebutton.grid(row=0,column=3,padx=3)

# New File
newfile= tk.PhotoImage(file='src/newfile.png')
newfilelabel= tk.Label(image=newfile)
newfilebutton= tk.Button(C, image=newfile, command=new_file,cursor="dot",
borderwidth=0,highlightthickness = 0,bd = 0,bg = config_data['background'],activebackground = config_data['background'], autostyle=False)
newfilebutton.grid(row=0,column=2,padx=3)

# Find And Replace
findfile= tk.PhotoImage(file='src/find.png')
findfilelabel= tk.Label(image=findfile)
findfilebutton= tk.Button(C, image=findfile, command = lambda: textfindnew(event=None),cursor="dot",
borderwidth=0,highlightthickness = 0,bd = 0,bg = config_data['background'],activebackground = config_data['background'], autostyle=False)
findfilebutton.grid(row=0,column=5,padx=3)

# Insert Template
tempfile= tk.PhotoImage(file='src/template.png')
tempfilelabel= tk.Label(image=tempfile)
tempfilebutton= tk.Button(C, image=tempfile,command=lambda: loadtemplate(usertext),cursor="dot",
borderwidth=0,highlightthickness = 0,bd = 0,bg = config_data['background'],activebackground = config_data['background'], autostyle=False)
tempfilebutton.grid(row=0,column=6,padx=3)

# Save as Template
savetempfile= tk.PhotoImage(file='src/savetemp.png')
savetempfilelabel= tk.Label(image=savetempfile)
savetempfilebutton= tk.Button(C, image=savetempfile, command=lambda: create_template(usertext),cursor="dot",
borderwidth=0,highlightthickness = 0,bd = 0,bg = config_data['background'],activebackground = config_data['background'], autostyle=False)
savetempfilebutton.grid(row=0,column=7,padx=3)

# Insert Color
colourfile= tk.PhotoImage(file='src/colour.png')
colourfilelabel= tk.Label(image=colourfile)
colourfilebutton= tk.Button(C, image=colourfile, command=inscolour,cursor="dot",
borderwidth=0,highlightthickness = 0,bd = 0,bg = config_data['background'],activebackground = config_data['background'], autostyle=False)
colourfilebutton.grid(row=0,column=8,padx=3)

# Launch markdown editor
mdfile= tk.PhotoImage(file='src/md.png')
mdfilelabel= tk.Label(image=mdfile)
mdfilebutton= tk.Button(C, image=mdfile, command = doceditor,cursor="dot",
borderwidth=0,highlightthickness = 0,bd = 0,bg = config_data['background'],activebackground = config_data['background'], autostyle=False)
mdfilebutton.grid(row=0,column=10,padx=3)

# Open program tree
treefile= tk.PhotoImage(file='src/tree.png')
treefilelabel= tk.Label(image=treefile)
treefilebutton= tk.Button(C, image=treefile,  cursor="dot", command=lambda: outlinewindow(usertext),
borderwidth=0,highlightthickness = 0,bd = 0,bg = config_data['background'],activebackground = config_data['background'], autostyle=False)
treefilebutton.grid(row=0,column=11,padx=3)

# Launch GUI builder
guifile= tk.PhotoImage(file='src/gui.png')
guifilelabel= tk.Label(image=guifile)
guifilebutton= tk.Button(C, image=guifile,  cursor="dot", command=guibuilder,
borderwidth=0,highlightthickness = 0,bd = 0,bg = config_data['background'],activebackground = config_data['background'], autostyle=False)
guifilebutton.grid(row=0,column=12,padx=3)

# Display Random Tip
tipfile= tk.PhotoImage(file='src/tip.png')
tipfilelabel= tk.Label(image=tipfile)
tipfilebutton= tk.Button(C, image=tipfile,  cursor="dot", command=tip,
borderwidth=0,highlightthickness = 0,bd = 0,bg = config_data['background'],activebackground = config_data['background'], autostyle=False)
tipfilebutton.grid(row=0,column=13,padx=3)

# Quick Run
qrunfile= tk.PhotoImage(file='src/qrun.png')
qrunfilelabel= tk.Label(image=qrunfile)
qrunfilebutton= tk.Button(C, image=qrunfile, command = lambda: quickrun(usertext), cursor="dot",
borderwidth=0,highlightthickness = 0,bd = 0,bg = config_data['background'],activebackground = config_data['background'], autostyle=False)
qrunfilebutton.grid(row=0,column=15,padx=3)

# Run file
runfile= tk.PhotoImage(file='src/run.png')
runfilelabel= tk.Label(image=runfile)
runfilebutton= tk.Button(C, image=runfile,cursor="dot", command=pythonrun,
borderwidth=0,highlightthickness = 0,bd = 0,bg = config_data['background'],activebackground = config_data['background'], autostyle=False)
runfilebutton.grid(row=0,column=16,padx=3)

# Settings menu
setfile= tk.PhotoImage(file='src/settings.png')
setfilelabel= tk.Label(image=setfile)
setfilebutton= tk.Button(C, image=setfile,command=settings,cursor="dot",
borderwidth=0,highlightthickness = 0,bd = 0,bg = config_data['background'],activebackground = config_data['background'], autostyle=False)
setfilebutton.grid(row=0,column=9,padx=3)

# AI Q&A
aifile= tk.PhotoImage(file='src/ai.png')
aifilelabel= tk.Label(image=aifile)
aifilebutton= tk.Button(C, image=aifile,cursor="dot", command=aiask,
borderwidth=0,highlightthickness = 0,bd = 0,bg = config_data['background'],activebackground = config_data['background'], autostyle=False)
aifilebutton.grid(row=0,column=14,padx=3)
aifilebutton.bind("<Button-3>", open_ai_settings) # This button has a right click too

#ToolTips
ToolTip(openfilebutton, msg="Open a Python file", follow=True, delay=0.1)
ToolTip(savefilebutton, msg="Save your Python project", follow=True, delay=0.1)
ToolTip(newfilebutton, msg="Make a new Python project", follow=True, delay=0.1)
ToolTip(findfilebutton, msg="Find text in this file\n and optionally replace it", follow=True, delay=0.1)
ToolTip(tempfilebutton, msg="Insert a template into this file", follow=True, delay=0.1)
ToolTip(savetempfilebutton, msg="Save this Python file as a template", follow=True, delay=0.1)
ToolTip(qrunfilebutton, msg="Quickly preview\n this code's result \n(Can cause errors if it\n relies on other files)", follow=True, delay=0.1)
ToolTip(runfilebutton, msg="Run the code", follow=True, delay=0.1)
ToolTip(setfilebutton, msg="Settings menu", follow=True, delay=0.1)
ToolTip(colourfilebutton, msg="Insert a colour as HEX \n(Opens a colour picking window)", follow=True, delay=0.1)
ToolTip(mdfilebutton, msg="Open the Markdown file editor", follow=True, delay=0.1)
ToolTip(treefilebutton, msg="Open the Program Tree\nDisplays All Functions/Classes", follow=True, delay=0.1)
ToolTip(guifilebutton, msg="Launch the Tkinter GUI Builder\n(Helps design elements for Tkinter GUI apps)", follow=True, delay=0.1)
ToolTip(tipfilebutton, msg="Displays a random Python tip", follow=True, delay=0.1)
ToolTip(aifilebutton, msg="Ask AI for Help\nRight-Click: AI Settings", follow=True, delay=0.1)

#----------------
#End for Buttons
#----------------


#-Analysis- # TODO Make it jump to the line needed
def check_code():
  
  try:
    subprocess.run(['flake8', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
  except FileNotFoundError:
    # Flake8 not found, show message box
    messagebox.showerror(
        "Flake8 Missing",
        "Flake8 is not installed.\nUse the Library Manager to install Flake8 for Analysis.\nCommand: pip install flake8")
    return

  # Get the code from the text widget
  code = usertext.get("1.0", tk.END)

  # Clear anal_listbox
  anal_listbox.delete(0, tk.END)

  # Create a temporary file to hold the code
  with NamedTemporaryFile(delete=False, mode='w', encoding="utf-8", suffix='.py') as tmp:
    tmp.write(code)
    tmp.flush()

    # Run flake8 using subprocess
    result = subprocess.run(['flake8', tmp.name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

  # Check for errors in the output
  if not result.stdout:
    # No errors detected, add a message
    anal_listbox.insert(tk.END, "Awesome job! Flake8 sees no improvements needed.")
  else:
    # Parse the flake8 output and add to the listbox
    output = StringIO(result.stdout)
    for line in output:
      # Split the line into parts - filepath, line number, column number, and message
      parts = line.split(':')
      if len(parts) > 1:
        # Extract line number and error message
        line_number = parts[2]
        error_message = parts[4]
        # Construct the error message with line number
        error_with_line = f"Line {line_number}: {error_message}"
        anal_listbox.insert(tk.END, error_with_line)

    # Additional message about Flake8 rules
    anal_listbox.insert(tk.END, "Click the bottom button to learn about Flake8 rules.")



#-Analysis END-

anal_listbox = tk.Listbox(frame5)
alalabel = tk.Button(frame5,bg="white",text="Analyze Code for Suggestions (with flake8)",command=check_code)
alalabel.pack(fill=tk.BOTH)
alalabel.configure(font=fontnew)
anal_listbox.pack(fill=tk.BOTH, expand=True)

anal_listbox.insert(tk.END, "Click the above button to start analysing code.")

def flake8rules():
    webbrowser.open("https://www.flake8rules.com",autoraise=True)

flbutton = tk.Button(frame5,bg="white",text="Flake8 Rules",command=flake8rules)
flbutton.pack(fill=tk.BOTH)
flbutton.configure(font=fontnew)

# Function to auto tidy code using autopep8
# Wanted to use Black but its too controversial with some stuff like func paras
# YAPF was a trouble to set up
# So AutoPEP8 it is :)

def formatcode(codetofix):
    code = codetofix
    fixedcode = fix_code(code, encoding="utf-8") # Return PEP8 Compliant code
    del(code)
    return fixedcode

def tidycodebutton():
    if messagebox.askyesno( "Confirmation", "Do you wish to tidy all your code to Python compliant standards?\n(This will not affect code functionality)."):
        stuff = usertext.get(1.0, tk.END)
        newcode =  formatcode(stuff)
        usertext.delete(1.0, tk.END)
        usertext.insert(1.0, newcode)
        tag_all() # Call syntax highlight function

        toast = ToastNotification( # Show a sucess message
            title="Formatted!",
            message="Code fixed to meet Python standards.",
            duration=3000,
            icon="👍",
            alert=True,
        )
        toast.show_toast()

        del(stuff)
        del(newcode) # del statements free up memory to make Blueconda more
                    # memory efficient (I hope it works as I think it does)



clbutton = tk.Button(frame5,bg="white",text="Make Code Neater...",command=tidycodebutton)
clbutton.pack(fill=tk.BOTH, pady=5)
clbutton.configure(font=fontnew)

frame1.rowconfigure(0, weight=1)
frame1.columnconfigure(0, weight=1)

frame2.rowconfigure(0, weight=1)
frame2.columnconfigure(0, weight=1)

frame3.rowconfigure(0, weight=1)
frame3.columnconfigure(0, weight=1)

frame4.rowconfigure(0, weight=1)
frame4.columnconfigure(0, weight=1)

frame5.rowconfigure(0, weight=1)
frame5.columnconfigure(0, weight=1)




# ---------------
# Library Manager
# ---------------

frame6.rowconfigure(0, weight=1)
frame6.columnconfigure(0, weight=1)

notebook.rowconfigure(0, weight=1)
notebook.columnconfigure(0, weight=1)

libmanager = tb.Notebook(frame6, bootstyle="primary")
libsframe = tb.Frame(libmanager)
installframe = tb.Frame(libmanager)
libmanager.add(libsframe, text="Installed Libraries")
libmanager.add(installframe, text="Install Library")
libmanager.grid(row=0, column=0, sticky="nsew")

_libs_python_exe = None
_libs_dist_map = {}
_libs_row_widgets = []
_libs_canvas = None
_libs_scrollable_frame = None
_libs_list_button = None
_libs_status_label = None
_libs_search_var = None
_libs_search_entry = None
_libs_all_packages = []
_libs_search_placeholder = "🔎Search..."
 
def find_system_python():
    # If your editor already stores/lets the user pick an interpreter, use that path instead.
    return shutil.which("python") or shutil.which("python3")
 
 
def get_site_packages_path(python_exe):
    kwargs = {}
    if sys.platform == "win32":
        kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
 
    result = subprocess.run(
        [python_exe, "-c", "import sysconfig; print(sysconfig.get_paths()['purelib'])"],
        capture_output=True, text=True, timeout=5, **kwargs
    )
    path = result.stdout.strip()
    return path or None
 
 
def get_installed_packages(python_exe=None):
    """
    Returns (packages, dist_map)
      packages: sorted list of {"name": ..., "version": ...}
      dist_map: {name: importlib.metadata.Distribution} for INFO lookups
    """
    exe = python_exe or find_system_python()
    if exe is None:
        return [], {}
 
    try:
        site_packages = get_site_packages_path(exe)
        if not site_packages:
            return [], {}
 
        dists = list(metadata.distributions(path=[site_packages]))
        dist_map = {d.metadata["Name"]: d for d in dists if d.metadata["Name"]}
 
        packages = sorted(
            ({"name": name, "version": d.version} for name, d in dist_map.items()),
            key=lambda p: p["name"].lower()
        )
        return packages, dist_map
    except Exception as e:
        print(f"Failed to list packages: {e}")
        return [], {}
 
 
def uninstall_package(python_exe, package_name):
    """Uninstall a package from the target interpreter's environment via pip."""
    kwargs = {}
    if sys.platform == "win32":
        kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
 
    result = subprocess.run(
        [python_exe, "-m", "pip", "uninstall", "-y", package_name],
        capture_output=True, text=True, timeout=60, **kwargs
    )
    return result.returncode == 0, (result.stdout + result.stderr)
 
 
# ---- UI setup -------------------------------------------------------------
 
def build_libsframe_ui():
    """Call once to build the top bar + scrollable list inside libsframe."""
    global _libs_canvas, _libs_scrollable_frame, _libs_list_button, _libs_status_label, _libs_python_exe
 
    _libs_python_exe = find_system_python()
 
    top = ttk.Frame(libsframe)
    top.pack(side="top", fill="x", padx=8, pady=8)
 
    _libs_list_button = ttk.Button(top, text="List Libraries", command=refresh_libs)
    _libs_list_button.pack(side="left")
 
    _libs_status_label = ttk.Label(top, text="")
    _libs_status_label.pack(side="left", padx=10)

    global _libs_search_var, _libs_search_entry

    _libs_search_var = tk.StringVar()
    _libs_search_entry = ttk.Entry(top, textvariable=_libs_search_var, width=15, foreground="grey")
    _libs_search_entry.pack(side="left", padx=(10, 0))
    _libs_search_entry.insert(0, _libs_search_placeholder)
    _libs_search_entry.bind("<FocusIn>", _libs_on_search_focus_in)
    _libs_search_entry.bind("<FocusOut>", _libs_on_search_focus_out)
    _libs_search_var.trace_add("write", _libs_on_search_changed)
 
    container = ttk.Frame(libsframe)
    container.pack(side="top", fill="both", expand=True, padx=8, pady=(0, 8))
 
    _libs_canvas = tk.Canvas(container, borderwidth=0, highlightthickness=0)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=_libs_canvas.yview)
    _libs_scrollable_frame = ttk.Frame(_libs_canvas)
 
    _libs_scrollable_frame.bind(
        "<Configure>",
        lambda e: _libs_canvas.configure(scrollregion=_libs_canvas.bbox("all"))
    )
 
    canvas_window = _libs_canvas.create_window((0, 0), window=_libs_scrollable_frame, anchor="nw")
    _libs_canvas.configure(yscrollcommand=scrollbar.set)
 
    _libs_canvas.bind(
        "<Configure>",
        lambda e: _libs_canvas.itemconfig(canvas_window, width=e.width)
    )
    
    scrollbar.pack(side="right", fill="y")
    _libs_canvas.pack(side="left", fill="both", expand=True)
    
 
    _libs_canvas.bind_all("<MouseWheel>", _libs_on_mousewheel)   # Windows / macOS
    _libs_canvas.bind_all("<Button-4>", _libs_on_mousewheel)     # Linux scroll up
    _libs_canvas.bind_all("<Button-5>", _libs_on_mousewheel)     # Linux scroll down
 
def _libs_on_search_focus_in(event):
    if _libs_search_var.get() == _libs_search_placeholder:
        _libs_search_entry.delete(0, "end")
        _libs_search_entry.config(foreground=config_data['textforeground'])  # Reset to normal text color


def _libs_on_search_focus_out(event):
    if not _libs_search_var.get():
        _libs_search_entry.insert(0, _libs_search_placeholder)
        _libs_search_entry.config(foreground="grey")


def _libs_on_search_changed(*args):
    query = _libs_search_var.get()
    if query == _libs_search_placeholder:
        return
    filtered = [p for p in _libs_all_packages if query.lower() in p["name"].lower()]
    _libs_populate_rows(filtered)
 
def _libs_on_mousewheel(event):
    if event.num == 4:
        _libs_canvas.yview_scroll(-1, "units")
    elif event.num == 5:
        _libs_canvas.yview_scroll(1, "units")
    else:
        _libs_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
 
 
# ---- data / refresh --------------------------------------------------------
 
def refresh_libs():
    if _libs_python_exe is None:
        messagebox.showerror("No Python found", "Could not locate a system python/python3 interpreter.")
        return
 
    _libs_list_button.config(state="disabled")
    _libs_status_label.config(text="Loading...")
    _libs_clear_rows()
 
    threading.Thread(target=_libs_load_packages_thread, daemon=True).start()
 
 
def _libs_load_packages_thread():
    packages, dist_map = get_installed_packages(_libs_python_exe)
    libsframe.after(0, _libs_on_packages_loaded, packages, dist_map)
 
 
def _libs_on_packages_loaded(packages, dist_map):
    global _libs_dist_map, _libs_all_packages
    _libs_dist_map = dist_map
    _libs_all_packages = packages
    _libs_populate_rows(packages)
    _libs_list_button.config(state="normal")
    _libs_status_label.config(text=f"{len(packages)} found." if packages else "No packages found")
 
 
def _libs_clear_rows():
    global _libs_row_widgets
    for widget in _libs_row_widgets:
        widget.destroy()
    _libs_row_widgets = []
 
 
def _libs_populate_rows(packages):
    _libs_clear_rows()
 
    for pkg in packages:
        row = ttk.Frame(_libs_scrollable_frame)
        row.pack(side="top", fill="x", padx=4, pady=2)
 
        label_text = f"{pkg['name']}  ({pkg['version']})"
        label = ttk.Label(row, text=label_text, anchor="w")
        label.pack(side="left", fill="x", expand=True, padx=(4, 4))
 
        delete_btn = tb.Button( 
            row, text="⨉", width=4, bootstyle="danger", 
            command=lambda name=pkg["name"]: _libs_on_delete_clicked(name)
        )
        ToolTip(delete_btn, msg="Delete Library", follow=True, delay=0.7, y_offset=-50, x_offset=-100)
        delete_btn.pack(side="right", padx=(4, 4))
 
        info_btn = tb.Button(
            row, text= "🛈", width=4, 
            command=lambda name=pkg["name"]: _libs_on_info_clicked(name)
        )
        ToolTip(info_btn, msg="View Library Info", follow=True, delay=0.7, y_offset=-50, x_offset=-100)
        info_btn.pack(side="right", padx=(4, 0))
 
        sep = ttk.Separator(_libs_scrollable_frame, orient="horizontal")
        sep.pack(side="top", fill="x", padx=4)
 
        _libs_row_widgets.extend([row, sep])
 
 
# ---- actions ----------------------------------------------------------------
 
def _libs_on_info_clicked(name):
    dist = _libs_dist_map.get(name)
    if dist is None:
        messagebox.showerror("Not found", f"No metadata found for {name}.")
        return
 
    meta = dist.metadata
    fields = [
        ("Name", meta.get("Name", name)),
        ("Version", dist.version),
        ("Summary", meta.get("Summary", "")),
        ("Author", meta.get("Author", "") or meta.get("Author-email", "")),
        ("License", meta.get("License", "")),
        ("Home-page", meta.get("Home-page", "")),
        ("Requires-Python", meta.get("Requires-Python", "")),
        ("Location", str(getattr(dist, "_path", "")) or ""),
    ]
 
    requires = dist.requires or []
    requires_preview = ", ".join(requires[:10]) + (" ..." if len(requires) > 10 else "")
 
    win = tk.Toplevel(libsframe)
    win.title(f"Info: {name}")
    #win.geometry("480x420")
 
    text = tk.Text(win, wrap="word")
    text.pack(fill="both", padx=8, pady=8)
 
    for label, value in fields:
        text.insert("end", f"{label}: ", ("bold",))
        text.insert("end", f"{value}\n\n")
 
    text.insert("end", "Requires: ", ("bold",))
    text.insert("end", requires_preview or "(none)")
 
    text.tag_configure("bold", font=("TkDefaultFont", 9, "bold"))
    text.configure(state="disabled")
 
    ttk.Button(win, text="Close", command=win.destroy).pack(pady=(0, 8),fill=tk.X)
 
 
def _libs_on_delete_clicked(name):
    confirm = messagebox.askyesno(
        "Confirm uninstall",
        f"Uninstall '{name}'? This runs pip uninstall and cannot be undone."
    )
    if not confirm:
        return
 
    _libs_list_button.config(state="disabled")
    _libs_status_label.config(text=f"Uninstalling {name}...")
    threading.Thread(target=_libs_delete_thread, args=(name,), daemon=True).start()
 
 
def _libs_delete_thread(name):
    success, output = uninstall_package(_libs_python_exe, name)
    libsframe.after(0, _libs_on_delete_finished, name, success, output)
 
 
def _libs_on_delete_finished(name, success, output):
    if success:
        messagebox.showinfo("Uninstalled", f"'{name}' was uninstalled successfully.")
    else:
        messagebox.showerror("Uninstall failed", f"Failed to uninstall '{name}':\n\n{output}")
    refresh_libs()
 
 
# Build the UI into the existing libsframe now that everything above is defined
build_libsframe_ui()


_install_pypi_index = None          # cached list of all PyPI package names, filled in by the prefetch thread
_install_index_event = threading.Event()   # set once the prefetch thread finishes (success or failure)
_install_python_exe = None
_install_canvas = None
_install_scrollable_frame = None
_install_search_var = None
_install_search_entry = None
_install_search_button = None
_install_status_label = None
_install_row_widgets = []
_install_search_placeholder = "🔎Search..."
_install_max_results = 25            # how many matched names to fetch details for
 
 
def install_package(python_exe, package_name):
    """Install a package into the target interpreter's environment via pip."""
    kwargs = {}
    if sys.platform == "win32":
        kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
 
    result = subprocess.run(
        [python_exe, "-m", "pip", "install", package_name],
        capture_output=True, text=True, timeout=120, **kwargs
    )
    return result.returncode == 0, (result.stdout + result.stderr)
 
 
def _install_fetch_pypi_index():
    """Downloads and parses https://pypi.org/simple/ into a flat list of names."""
    response = requests.get("https://pypi.org/simple/", timeout=20)
    html = response.text
 
    names = []
    for chunk in html.split('<a href="')[1:]:
        try:
            name = chunk.split('>')[1].split('<')[0]
            names.append(name)
        except IndexError:
            continue
 
    return names
 
 
def _install_prefetch_index_thread():
    """Runs once at startup on a background thread to warm _install_pypi_index."""
    global _install_pypi_index
    try:
        names = _install_fetch_pypi_index()
        _install_pypi_index = names
    except Exception as e:
        _install_pypi_index = []
        installframe.after(0, _install_on_prefetch_failed, str(e))
        _install_index_event.set()
        return
 
    installframe.after(0, _install_on_prefetch_done)
    _install_index_event.set()
 
 
def _install_on_prefetch_done():
    # Only touch the status label if the user hasn't already started searching
    if _install_status_label.cget("text") == "Loading package list...":
        _install_status_label.config(text="")
 
 
def _install_on_prefetch_failed(error_text):
    _install_status_label.config(text="Package index failed to load")
    print(f"Failed to prefetch PyPI index: {error_text}")
 
 
def _install_fetch_package_summary(name):
    """Fetch short description for a single package. Returns '' on any failure."""
    try:
        response = requests.get(f"https://pypi.org/pypi/{name}/json", timeout=5)
        if response.status_code != 200:
            return ""
        data = response.json()
        return data.get("info", {}).get("summary", "") or ""
    except Exception:
        return ""
 
 
# ---- UI setup -------------------------------------------------------------
 
def build_installframe_ui():
    global _install_canvas, _install_scrollable_frame
    global _install_search_var, _install_search_entry, _install_search_button
    global _install_status_label, _install_python_exe
 
    _install_python_exe = find_system_python()
 
    container = ttk.Frame(installframe)
    container.pack(side="top", fill="both", expand=True, padx=8, pady=(8, 0))
 
    _install_canvas = tk.Canvas(container, borderwidth=0, highlightthickness=0)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=_install_canvas.yview)
    _install_scrollable_frame = ttk.Frame(_install_canvas)
 
    _install_scrollable_frame.bind(
        "<Configure>",
        lambda e: _install_canvas.configure(scrollregion=_install_canvas.bbox("all"))
    )
 
    canvas_window = _install_canvas.create_window((0, 0), window=_install_scrollable_frame, anchor="nw")
    _install_canvas.configure(yscrollcommand=scrollbar.set)
 
    _install_canvas.bind(
        "<Configure>",
        lambda e: _install_canvas.itemconfig(canvas_window, width=e.width)
    )
 
    _install_canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
 
    _install_canvas.bind_all("<MouseWheel>", _install_on_mousewheel)
    _install_canvas.bind_all("<Button-4>", _install_on_mousewheel)
    _install_canvas.bind_all("<Button-5>", _install_on_mousewheel)
 
    # Bottom bar: status label + search box + search button
    bottom = ttk.Frame(installframe)
    bottom.pack(side="bottom", fill="x", padx=8, pady=8)
 
    _install_status_label = ttk.Label(bottom, text="")
    _install_status_label.pack(side="left")
 
    _install_search_button = ttk.Button(bottom, text="🔎Search", command=_install_on_search_clicked)
    _install_search_button.pack(side="right")
 
    _install_search_var = tk.StringVar()
    _install_search_entry = ttk.Entry(bottom, textvariable=_install_search_var, foreground="grey")
    _install_search_entry.pack(side="right", fill="x", expand=True, padx=(10, 10))
    _install_search_entry.insert(0, _install_search_placeholder)
    _install_search_entry.bind("<FocusIn>", _install_on_search_focus_in)
    _install_search_entry.bind("<FocusOut>", _install_on_search_focus_out)
    _install_search_entry.bind("<Return>", lambda e: _install_on_search_clicked())
 
 
def _install_on_mousewheel(event):
    if event.num == 4:
        _install_canvas.yview_scroll(-1, "units")
    elif event.num == 5:
        _install_canvas.yview_scroll(1, "units")
    else:
        _install_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
 
 
def _install_on_search_focus_in(event):
    if _install_search_var.get() == _install_search_placeholder:
        _install_search_entry.delete(0, "end")
        _install_search_entry.config(foreground=config_data['textforeground'])  # Reset to normal text color
 
 
def _install_on_search_focus_out(event):
    if not _install_search_var.get():
        _install_search_entry.insert(0, _install_search_placeholder)
        _install_search_entry.config(foreground="grey")
 
 
# ---- search flow ------------------------------------------------------------
 
def _install_on_search_clicked():
    query = _install_search_var.get().strip()
    if not query or query == _install_search_placeholder:
        return
 
    _install_search_button.config(state="disabled")
    _install_clear_rows()
    _install_status_label.config(text="Searching...")
    threading.Thread(target=_install_search_thread, args=(query,), daemon=True).start()
 
 
def _install_search_thread(query):
    # If the startup prefetch is still running, this just waits for it in the
    # background — the main window is never blocked. If it already finished,
    # this returns instantly.
    _install_index_event.wait()

    index = _install_pypi_index or []
    query_lower = query.lower()

    # Split into an exact name match (if any) and everything else that just
    # contains the query, so the exact one can be shown first and separately.
    exact_matches = [n for n in index if n.lower() == query_lower]
    similar_matches = [n for n in index if n.lower() != query_lower and query_lower in n.lower()]

    ordered_matches = (exact_matches + similar_matches)[:_install_max_results]
    exact_count = len(exact_matches)

    results = []
    for name in ordered_matches:
        summary = _install_fetch_package_summary(name)
        results.append({"name": name, "summary": summary})

    installframe.after(0, _install_on_search_finished, results, exact_count)


def _install_on_search_finished(results, exact_count=0):
    _install_search_button.config(state="normal")
    _install_status_label.config(text=f"{len(results)} result(s)" if results else "No matches found")
    _install_populate_rows(results, exact_count)
 
def _install_clear_rows():
    global _install_row_widgets
    for widget in _install_row_widgets:
        widget.destroy()
    _install_row_widgets = []
 
 
def _install_populate_rows(results, exact_count=0):
    _install_clear_rows()

    if exact_count > 0:
        heading = ttk.Label(
            _install_scrollable_frame, foreground=config_data["variable"],
            text="Exact Match" if exact_count == 1 else "Exact Matches",
            font=("TkDefaultFont", 9, "bold")
        )
        heading.pack(side="top", fill="x", anchor="w", padx=4, pady=(4, 2))
        _install_row_widgets.append(heading)

    for i, pkg in enumerate(results):
        # Right after the exact match(es), drop in the "Similar Matches" heading
        # before continuing with the rest of the list.
        if exact_count > 0 and i == exact_count:
            similar_heading = ttk.Label(
                _install_scrollable_frame, text="Similar Matches",
                font=("TkDefaultFont", 9, "bold"), foreground=config_data["variable"]
            )
            similar_heading.pack(side="top", fill="x", anchor="w", padx=4, pady=(10, 2))
            _install_row_widgets.append(similar_heading)

        row = ttk.Frame(_install_scrollable_frame)
        row.pack(side="top", fill="x", padx=4, pady=6)

        install_btn = tb.Button(
            row, text="↓",
            command=lambda name=pkg["name"]: _install_on_install_clicked(name)
        )

        ToolTip(install_btn, msg="Install Library", follow=True, delay=0.7, y_offset=-50, x_offset=-100)

        install_btn.pack(side="right", padx=(4, 4), anchor="n")

        text_frame = ttk.Frame(row)
        text_frame.pack(side="left", fill="both", expand=True, padx=(4, 4))

        name_label = ttk.Label(text_frame, text=pkg["name"], font=("TkDefaultFont", 10, "bold"), anchor="w")
        name_label.pack(side="top", fill="x", anchor="w")

        desc_text = pkg["summary"] or "(no description available)"
        desc_label = ttk.Label(text_frame, text=desc_text, anchor="w", justify="left")
        desc_label.pack(side="top", fill="x", anchor="w")
        desc_label.bind("<Configure>", lambda e, lbl=desc_label: lbl.config(wraplength=e.width))

        sep = ttk.Separator(_install_scrollable_frame, orient="horizontal")
        sep.pack(side="top", fill="x", padx=4)

        _install_row_widgets.extend([row, sep])
 
# ---- install action -----------------------------------------------------------
 
def _install_on_install_clicked(name):
    confirm = messagebox.askyesno("Confirm install", f"Install '{name}'?")
    if not confirm:
        return
 
    _install_search_button.config(state="disabled")
    _install_status_label.config(text=f"Installing {name}...")
    threading.Thread(target=_install_install_thread, args=(name,), daemon=True).start()
 
 
def _install_install_thread(name):
    success, output = install_package(_install_python_exe, name)
    installframe.after(0, _install_on_install_finished, name, success, output)
 
 
def _install_on_install_finished(name, success, output):
    _install_search_button.config(state="normal")
    _install_status_label.config(text="")
    if success:
        messagebox.showinfo("Installed", f"'{name}' was installed successfully.")
    else:
        messagebox.showerror("Install failed", f"Failed to install '{name}':\n\n{output}")
 
 
# Build the UI into the existing installframe now that everything above is defined
build_installframe_ui()
 
# Kick off the PyPI index download immediately, on a background thread, so it's
# already warm by the time the user runs their first search.
_install_status_label.config(text="Loading package list...")
threading.Thread(target=_install_prefetch_index_thread, daemon=True).start()



# Simple function to copy all and cut all
def copy_all(event=None):
    text = usertext.get(1.0, tk.END)
    window.clipboard_clear()
    window.clipboard_append(text)
    del(text)

def cut_all(event=None):
    text = usertext.get(1.0, tk.END)
    window.clipboard_clear()
    window.clipboard_append(text)
    usertext.delete(1.0,tk.END)
    del(text)

def go_to_line(event=None):
    maxval = int(usertext.index('end-1c').split('.')[0])
    line_number = simpledialog.askinteger("Line Navigate","Line to Jump to:", maxvalue=maxval)
    usertext.see(f"{line_number + 5}.0")
    usertext.focus_set()
    usertext.tag_remove("sel", 1.0, tk.END)
    start_index = usertext.index(f"{line_number}.0")
    end_index = usertext.index(f"{line_number}.end")
    usertext.tag_add("sel", start_index, end_index)

indicat.bind("<Button-1>",  go_to_line) # Indicat is the Row X, Column Y text
ToolTip(indicat, msg="Click to Jump to Line", follow=True, delay=0.7, y_offset=-50) # Use Y OFFSET Para to
                                                                                    # ensure tooltip is visible
def findreplace(): # REDACTED
    source_text = usertext.get("1.0","end-1c")
    find_text = simpledialog.askstring("Find/Replace", "Text to Find:",parent=window)
    replace_text = simpledialog.askstring("Find/Replace", "Text to replace with:",parent=window)
    replaced_text = source_text.replace(find_text, replace_text)
    usertext.delete("1.0", tk.END)
    usertext.insert(tk.END, replaced_text)
    del(source_text)
    tag_all()
fsmode = True # boolean to control fullscreen state
def fullscreen(): # Low budget Zen mode
    global fsmode
    if fsmode:
        window.overrideredirect(True) # Window overrides the top bar and taskbar
        fsmode = False
    else:
        window.overrideredirect(False)
        fsmode = True
        pywinstyles.change_header_color(window, color=config_data['background'])   # Change header color

# I was gracious enough to license this under MIT License!
# This means anyone is free to take the source code and use
# it as per their wish (Although I wouldn't recommend using
# my crappy code as an example for anything, I don't even 
# know OOP! )

# MIT License: https://opensource.org/license/mit

def licenseapp():
    licensewindow = tk.Toplevel()
    licensewindow.attributes('-topmost', True)
    licensewindow.attributes("-alpha", 0.9)
    licensewindow.title("License")
    licensewindow.configure(bg=config_data["background"])
    
    with open("license.txt",mode="r",encoding="utf-8") as licensefile:
        license_text = licensefile.read()
        licensefile.close()

    # automatically set license to the current year in case I forget to change it
    license_text = license_text.replace("2025",str(date.today().year))
     

    lictextbox = tb.Text(licensewindow, wrap="word")
    lictextbox.insert(tk.END, license_text)
    lictextbox.configure(state="disabled")
    lictextbox.pack(fill=tk.BOTH, expand=True)

    del(license_text) # Remove the unneeded var (enforced garbage collection)

    pywinstyles.change_header_color(licensewindow, color=config_data['background'])
    maximize_minimize_button.hide(licensewindow)

def recentfile(): # Open most recent file opened
    global file_loaded
    try:
        with open("temp/mostrecentfile.txt",mode="r",encoding="utf-8") as greenland:
            currentfile = greenland.read() # No offense to anyone from Greenland! :)
            if not currentfile:
                messagebox.showerror("Error", "No recent file found.")
                return # End function here
            confirmation = messagebox.askyesno("Continue",f"Do you wish to open {currentfile}?\nSave your current work first or it will be lost.")
            if confirmation:
                usertext.delete(1.0, tk.END)
                with open(currentfile,mode="r", encoding="utf-8") as doc:
                    contents = doc.read()
                    usertext.insert(tk.END, contents)
                    tag_all()
                    del(contents)
                with open("temp/currentfile.txt","w") as rw:
                    rw.write(currentfile)
                update_title(file_path= currentfile)
                file_loaded = True
                usertext.edit_modified(False)
                del(currentfile)


    except Exception as e:
        messagebox.showerror("Error", "An Error has occured trying to complete this request. The file requested could not be found.")

def calibratelinenumbers():
    pass
 # This function used to be used in case the line numbers got so long (into 4 digits)
 # that they'd go off screen. I made it an auto scaling feature now so no manual 
 # adjustment needed! Beginner friendlines for life :)


def estimatefilesize():
    filecontent = usertext.get(1.0, tk.END)
    with open("temp/anothertemp.py", 'w', encoding='utf-8') as imrankhan:
        imrankhan.write(filecontent) # Pro Pakistani
        imrankhan.close()
        del(filecontent)
    file_size = os.stat("temp/anothertemp.py").st_size
    if file_size > 1024:
        # Different units (KB, MB, GB or just B)
        nwdf = round(file_size / 1024, 2)
        messagebox.showinfo("File Size", f"Estimated File Size: {nwdf} KB")
    elif file_size > 1024 * 1024:
        nwdf = round(file_size / 1024 * 1024, 2)
        messagebox.showinfo("File Size", f"Estimated File Size: {nwdf} MB")
    elif file_size > 1024 ^ 3:
        nwdf = round(file_size / 1024^3, 2)
        messagebox.showinfo("File Size", f"Estimated File Size: {nwdf} GB")
    else:
        nwdf = file_size 
        messagebox.showinfo("File Size", f"Estimated File Size: {nwdf} B")
    del(filecontent)

def lookfunction(): # This doesn't work for a lot of functions :(
    funcname = simpledialog.askstring("Lookup", "Enter the name of a function:")
    message = get_function_description(funcname)
    if message == "ERROR":
        websearch = messagebox.askyesno("Not Found", f"{funcname} was not found in the list of built in functions. Do you want to look it up online?")
        if websearch:
            webbrowser.open(f"www.google.com/search?q=python+function+{funcname}", autoraise=True)
    else:
        messagebox.showinfo("Lookup", message)

def comingsoon(): # no guarantees!
    cswin = tk.Toplevel()
    cswin.attributes('-topmost', True)
    cswin.attributes("-alpha", 0.9)
    cswin.configure(bg=config_data["background"])
    cswin.title("Coming Soon!")
    tk.Label(cswin, font=fontnew, text="New planned features\nthat might be added soon!\n(No Guarantees)").grid(row=0, column=0)
    tk.Label(cswin, text="1) Better Functionality and support\nfor the AI Feature.", justify="left").grid(row=1, column=0, sticky="W", pady=5)
    tk.Label(cswin, text="2) Ability to auto download and install\nupdates", justify="left").grid(row=2, column=0, sticky="W", pady=5)
    tk.Label(cswin, text="3) Built in python compiler to make installing\neasier (and automatically building exe files)", justify="left").grid(row=3, column=0, sticky="W", pady=5)
    tk.Label(cswin, text="4) Support for programming MicroPython\ncompatible boards like ESP8266", justify="left").grid(row=4, column=0, sticky="W", pady=5)
    tk.Label(cswin, text="5) A built in Git client for version\ncontrol and connecting to repos.", justify="left").grid(row=5, column=0, sticky="W", pady=5)
    pywinstyles.change_header_color(cswin, color=config_data['background'])
    maximize_minimize_button.hide(cswin)

# Initialize Unsaved Changes Indicator
create_unsaved_indicator(window, savefilebutton)




def useconfig():
    configpy = codeview.get(1.0, tk.END)
    with open("settings/userconfig.py", "w") as bbc:
        bbc.write(configpy)
        bbc.close()
    apwin.destroy()

def appconfigutility(): 
    with open("settings/userconfig.py", "r") as tts:
        pretext = tts.read()
        tts.close()
    global codeview, apwin
    apwin = tk.Toplevel()
    apwin.attributes('-topmost', True)
    apwin.attributes("-alpha", 0.9)
    apwin.geometry(scalewindow(620, 600))
    apwin.configure(bg=config_data["background"])
    apwin.title("App Config Utility")
    tk.Label(apwin, text="The App Config Utility is a tool used to customize\nthe Editor using Python code.\n\nThe entered script below can be used\n to modify the app source.").pack()
    # Change color scheme (cls) of CodeView depending on user chosen theme
    if config_data["themename"] == "superhero": # ttkbootstrap theme for DeepBlue
        cls = "mariana"
    elif config_data["themename"] == "cerculean": # ... Default and TreeTrunks
        cls = "ayu-light"
    elif config_data["themename"] == "darkly": # ... Batman
        cls = "ayu-dark"
    elif config_data["themename"] == "solar": # ... Solarized
        cls = "dracula"
    tk.Button(apwin, text="Use Config (Restart Required)", command=useconfig).pack(fill=tk.X, expand=True)
    codeview = CodeView(apwin, lexer=pygments.lexers.PythonLexer, color_scheme=cls) # CodeView Widget for App Config Utility
    codeview.pack(fill="both", expand=True)
    codeview.insert(1.0, pretext)
    pywinstyles.change_header_color(apwin, color=config_data['background'])
    maximize_minimize_button.hide(apwin)


# Add a file menu
file_menu = tk.Menu(window, tearoff=0, background=config_data['background'])
file_menu.add_command(label="Open Most Recent File", command=recentfile)
file_menu.add_separator()
file_menu.add_command(label="New",command=new_file)
file_menu.add_command(label="Open",command=open_file)
file_menu.add_command(label="Save",command=save_file)
file_menu.add_command(label="Save As",command=save_file_as)
file_menu.add_separator()
file_menu.add_command(label="Close",command=closecode)

# Add an edit menu
edit_menu = tk.Menu(window, tearoff=0)
edit_menu.add_command(label="Undo",command=usertext.edit_undo)
edit_menu.add_command(label="Redo",command=usertext.edit_redo)
edit_menu.add_separator()
edit_menu.add_command(label="Calibrate Line Numbers",command=linenumbers)
edit_menu.add_command(label="Estimate File Size",command=estimatefilesize)
edit_menu.add_separator()
edit_menu.add_command(label="App Config Utility",command=appconfigutility)
edit_menu.add_command(label="TODOs/FIXMEs",command=todofixmewindow)
edit_menu.add_separator()
edit_menu.add_command(label="Copy All",command=copy_all)
edit_menu.add_command(label="Cut All",command=cut_all)
edit_menu.add_separator()
edit_menu.add_command(label="Go to Line",command=go_to_line)
edit_menu.add_separator()
edit_menu.add_command(label="Fullscreen",command=fullscreen)

# Add a help menu
help_menu = tk.Menu(window, tearoff=0)
help_menu.add_command(label="Install Python", command=pythoninstallwindow)
help_menu.add_command(label="Install All Dependencies", command=DependencyManager)
# help_menu.add_command(label="Check for Updates...", command=comingsoon) # TODO finish this 
help_menu.add_separator()
help_menu.add_command(label="Lookup Function", command=lookfunction)
help_menu.add_command(label="Documentation", command=documentationopen)
help_menu.add_command(label="Website")
help_menu.add_separator()
help_menu.add_command(label="Coming Soon!", command=comingsoon)
help_menu.add_separator()
help_menu.add_command(label="License",command=licenseapp)
help_menu.add_command(label="About",command=aboutapp)

def remove_inactive_outline(root): # I don't know why the AI made this a function!
  """Removes the outline from inactive ttkbootstrap Menubuttons."""
  style = tb.Style()
  style.configure("Outline.TMenubutton", borderwidth=0, relief="flat")  # Remove outline



menubutton = tb.Menubutton(menuframe,  text="File", menu=file_menu, bootstyle="outline")
menubutton2 = tb.Menubutton(menuframe, text="Edit", menu=edit_menu, bootstyle="outline")
menubutton3 = tb.Menubutton(menuframe, text="Help", menu=help_menu, bootstyle="outline")

menubutton.grid(row=0, column=0, sticky="W")
menubutton2.grid(row=0, column=1, sticky="W")
menubutton3.grid(row=0, column=2, sticky="W")

window.grid_rowconfigure(0, weight=0)
window.grid_rowconfigure(1, weight=0)
window.grid_rowconfigure(2, weight=1)

remove_inactive_outline(window)

for child in window.winfo_children():
    if isinstance(child, tk.Label):
        child.configure(background=config_data['background'])

# This function is used to mask the delayed start of the main editor
try:
    process = subprocess.Popen(["starterspash.exe"])
    process.wait()
except Exception: # This is used for people who are building from source and don't have .exe
    build_exe("starterspash.py","starterspash.exe", True)

# Use Config Data Entered by user
with open("settings/userconfig.py", "r") as setfil:
    data = setfil.read()
    setfil.close()

# This is dangerous, but I trust the user to not misuse this
try:
    exec(data)
except Exception as e:
    messagebox.showerror("Error",
                          f"Blueconda has detected a problem in the App Config Utility.\n\nError: {e}")

window.after(1200, welcomescreen) # Deploy welcomescreen

window.mainloop() # Run the mainloop

# And thats it! End of the Blueconda Source Code.
# Thank you for going through this!
#⠀⠀⠀⠀⠀⠀⠀⢀⣤⣴⣶⣶⣶⣶⣶⣦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⢀⣾⠟⠛⢿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⢸⣿⣄⣀⣼⣿⣿⣿⣿⣿⣿⣿⠀⢀⣀⣀⣀⡀⠀⠀
#⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠉⠉⣿⣿⣿⣿⣿⠀⢸⣿⣿⣿⣿⣦⠀
#⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢸⣿⣿⣿⣿⣿⡇
#⢰⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⠿⠿⠿⠿⠿⠋⠀⣼⣿⣿⣿⣿⣿⡇
#⢸⣿⣿⣿⣿⣿⡿⠉⢀⣠⣤⣤⣤⣤⣤⣤⣤⣴⣾⣿⣿⣿⣿⣿⣿⡇
#⢸⣿⣿⣿⣿⣿⡇⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀
#⠘⣿⣿⣿⣿⣿⡇⠀⣿⣿⣿⣿⣿⠛⠛⠛⠛⠛⠛⠛⠛⠛⠋⠁⠀⠀
#⠀⠈⠛⠻⠿⠿⠇⠀⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⣿⡇⠀⠀⠀⠀⠀⠀
#⠀⠀⠀  ⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣧⣀⣀⣿⠇⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀ ⠀⠀⠀⠘⢿⣿⣿⣿⣿⣿⣿⣿⡿⠋

#    P    Y    T    H    O    N