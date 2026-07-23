import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter.colorchooser import askcolor
from tkinter import ttk  # Import ttk for themed progress bar
from PIL import Image, ImageTk
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Image as PLImage, Spacer, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import tempfile

class TextEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Text Editor")
        self.root.geometry("800x600")
        self.root.configure(bg="#333333")  # Set background color to dark grey

        self.default_font = ("Helvetica", 12)  # Default font
        self.available_fonts = [
            "Helvetica",
            "Arial",
            "Times New Roman",
            "Courier New",
            "Verdana",
            "Tahoma",
        ]

        # Add a default text content
        self.default_text_content = "NoteWrapper: Versatile PDF Editor"

        # Add a themed progress bar for startup
        self.startup_progress_label = tk.Label(self.root, text="NoteWrapper: Starting up!", fg="white", bg="#333333")
        self.startup_progress_label.pack(pady=50)
        self.startup_progress_bar = ttk.Progressbar(self.root, mode="indeterminate", length=400)
        self.startup_progress_bar.pack(pady=10)
        self.startup_progress_bar.start(10)  # Start the progress bar

        # Delay the text editor initialization
        self.root.after(3000, self.initialize_text_editor)

    def initialize_text_editor(self):
        self.startup_progress_label.destroy()
        self.startup_progress_bar.destroy()

        self.text_editor = tk.Text(self.root, wrap=tk.WORD, font=self.default_font, fg="white", bg="#333333")
        self.text_editor.pack(fill=tk.BOTH, expand=True)

        # Add default text content
        self.text_editor.insert(tk.END, self.default_text_content)

        # Create a menu
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        # File menu
        self.file_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Save as PDF", command=self.save_as_pdf)
        self.file_menu.add_command(label="Open File", command=self.open_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)

        # Image menu
        self.image_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Image", menu=self.image_menu)
        self.image_menu.add_command(label="Insert Image", command=self.insert_image)

        # Font menu
        self.font_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Font", menu=self.font_menu)
        for font in self.available_fonts:
            self.font_menu.add_command(label=font, command=lambda f=font: self.change_font(f))

        # Text color menu
        self.text_color_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Text Color", menu=self.text_color_menu)
        self.text_color_menu.add_command(label="Change Text Color", command=self.change_text_color)

        # Text size menu
        self.text_size_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Text Size", menu=self.text_size_menu)
        self.text_size_menu.add_command(label="Increase Text Size", command=self.increase_text_size)
        self.text_size_menu.add_command(label="Decrease Text Size", command=self.decrease_text_size)

        # Keep track of inserted images
        self.images = []

        # Bind keyboard shortcuts
        self.root.bind("<Control-s>", self.save_as_pdf)
        self.root.bind("<Control-o>", self.open_file)
        self.root.bind("<Control-x>", self.cut_text)
        self.root.bind("<Control-c>", self.copy_text)
        self.root.bind("<Control-v>", self.paste_text)

    def insert_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp *.ppm *.pgm")])
        if file_path:
            image = Image.open(file_path)
            photo = ImageTk.PhotoImage(image)
            self.text_editor.image_create(tk.END, image=photo)
            self.images.append((image, photo))

    def change_font(self, selected_font):
        self.default_font = (selected_font, 12)
        self.text_editor.configure(font=self.default_font)

    def change_text_color(self):
        color = askcolor()[1]  # Ask user for a color
        if color:
            self.text_editor.tag_configure("colored", foreground=color)
            self.text_editor.tag_add("colored", self.text_editor.index(tk.SEL_FIRST), self.text_editor.index(tk.SEL_LAST))

    def increase_text_size(self):
        current_font = self.text_editor.cget("font")
        font_size = int(current_font.split(" ")[-1])
        new_font_size = font_size + 2  # Increase font size by 2
        new_font = current_font.replace(str(font_size), str(new_font_size))
        self.text_editor.configure(font=new_font)

    def decrease_text_size(self):
        current_font = self.text_editor.cget("font")
        font_size = int(current_font.split(" ")[-1])
        new_font_size = max(8, font_size - 2)  # Decrease font size by 2 but keep it above 8
        new_font = current_font.replace(str(font_size), str(new_font_size))
        self.text_editor.configure(font=new_font)

    def save_as_pdf(self, event=None):
        text_content = self.text_editor.get("1.0", tk.END).strip()
        if not text_content and not self.images:
            messagebox.showerror("Error", "No content to save.")
            return

        pdf_file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if pdf_file_path:
            try:
                doc = SimpleDocTemplate(pdf_file_path, pagesize=letter)
                story = []

                # Add images to the story
                for img, _ in self.images:
                    img_path = tempfile.mktemp(suffix=".png")
                    img.save(img_path, format="PNG")

                    story.append(PLImage(img_path, width=400, height=300))
                    story.append(Spacer(1, 12))  # Add some spacing between images

                # Add text content to the story
                styles = getSampleStyleSheet()
                style = styles["Normal"]
                # Set a recognized font for ReportLab (e.g., Helvetica)
                style.fontName = "Helvetica"
                style.fontSize = self.default_font[1]
                story.append(Paragraph(text_content, style))

                doc.build(story)
                messagebox.showinfo("Info", "PDF saved successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Error saving PDF: {str(e)}")

    def open_file(self, event=None):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                self.text_editor.delete("1.0", tk.END)  # Clear existing content
                self.text_editor.insert(tk.END, content)

    def cut_text(self, event=None):
        self.text_editor.event_generate("<<Cut>>")

    def copy_text(self, event=None):
        self.text_editor.event_generate("<<Copy>>")

    def paste_text(self, event=None):
        self.text_editor.event_generate("<<Paste>>")

if __name__ == "__main__":
    root = tk.Tk()
    app = TextEditorApp(root)
    root.mainloop()


os.system('pause')