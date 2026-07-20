
'''
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
    exe = python_exe or find_system_python()
    if exe is None:
        return []

    try:
        site_packages = get_site_packages_path(exe)
        if not site_packages:
            return []

        dists = metadata.distributions(path=[site_packages])
        packages = sorted(
            ({"name": d.metadata["Name"], "version": d.version} for d in dists if d.metadata["Name"]),
            key=lambda p: p["name"].lower()
        )
        return packages
    except Exception as e:
        print(f"Failed to list packages: {e}")
        return []

#--------------------------------------------------------------
class ConsoleFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.text = tk.Text(self, height=15, width=60,borderwidth=2, autostyle=False, wrap="word")
        self.text.pack()
        self.text.configure(font=fontnew)
        self.text.configure(fg=config_data['textforeground'])
        self.text.configure(bg=config_data['background'])
        self.entry = tk.Entry(self,borderwidth=2)
        self.entry.bind('<Return>', self.execute_command)
        self.entry.pack(fill=tk.BOTH)

        self.thread = None

    def execute_command(self, event):
        command = self.entry.get()
        self.entry.delete(0, tk.END)

        def run_command(): 
            if command == 'list_lib':
                packages = get_installed_packages()
                for package in packages:
                    self.text.tag_configure("package_name", foreground="black")
                    self.text.tag_configure("version_number", foreground=config_data['operator'])
                    self.text.insert('end', f"{package['name']} ")
                    self.text.insert('end', f"     | Version: {package['version']}\n", "version_number")
            else: # SOME COMMANDS OTHER THAN PIP INSTALL CAN CAUSE CORRUPTION AT THIS STAGE! PLEASE BE CAREFUL!!
                output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
                self.text.insert('end', output.stdout.decode('utf-8'))
            

        self.thread = threading.Thread(target=run_command)
        self.thread.start()
console = ConsoleFrame(frame6)
console.pack()
libman1 = tk.Label(frame6,text="Blueconda Library Manager",bg="white")
libman1.pack()
libman2 = tk.Label(frame6,text="Assuming the name of the library is foo:",bg="white")
libman2.pack()
libman3 = tk.Label(frame6,text="Use command: 'pip install foo' to install",bg="white")
libman3.pack()
libman4 = tk.Label(frame6,text="Use command: list_lib to view all installed libraries",bg="white")
libman4.pack()

#--------------------------------------------------------------
def launch_python_shell():
  def run_python_shell():
    subprocess.call(["python"])
  thread = threading.Thread(target=run_python_shell)
  # Start the thread.
  thread.start()

def launch_command_prompt():
  """Launches the command prompt in a separate thread."""
  def run_command_prompt():
    subprocess.call(["cmd"])
  thread = threading.Thread(target=run_command_prompt)
  thread.start()

def check_library(library_name):
    """Checks if a Python library is installed and displays a message box with its version (if found).

    Args:
        library_name (str): The name of the library to check.
    """

    try:
        # Attempt to get distribution information
        distribution = pkg_resources.get_distribution(library_name)
        version = distribution.version
        messagebox.showinfo(title="Library Installed", message=f"{library_name} is installed!\n(version: {version})")
    except pkg_resources.DistributionNotFound:
        messagebox.showerror(title="Library Not Found", message=f"{library_name} is not installed.")



def libcheckmain(): # IDK why the AI split this into two functions ¯\_(ツ)_/¯
    libname = simpledialog.askstring("Enter Name:", "Enter the Name of the Library:")
    if libname:
        check_library(libname)
    else:
        messagebox.showerror("Error", "Please enter a Library Name.")

consolelaunch = tk.Button(frame6,bg="white",text="Launch Python Shell",command=launch_python_shell)
consolelaunch.pack(fill=tk.BOTH, pady=3)

solelaunch = tk.Button(frame6,bg="white",text="Launch Command Prompt",command=launch_command_prompt)
solelaunch.pack(fill=tk.BOTH)

serlaunch = tk.Button(frame6,bg="white",text="Check if Python Library is Installed...",command=libcheckmain)
serlaunch.pack(fill=tk.BOTH, pady=3)
'''