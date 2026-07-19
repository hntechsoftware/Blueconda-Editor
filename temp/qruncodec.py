import os
import tkinter as tk
from tkinter import filedialog
import os

def clean_chat_log():
    # Set up the file chooser dialog
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window
    
    file_path = filedialog.askopenfilename(
        title="Select your chat log text file",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    
    if not file_path:
        print("No file selected. Exiting.")
        return

    cleaned_lines = []
    keep_line = False

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                # Check for markers to toggle the saving state
                if "You said" in line:
                    keep_line = True
                    cleaned_lines.append(line)
                elif "Gemini said" in line:
                    keep_line = False
                
                # If we are in the 'You' section, keep the content
                elif keep_line:
                    cleaned_lines.append(line)

        # Create the output file name
        base, ext = os.path.splitext(file_path)
        output_path = f"{base}_cleaned{ext}"

        with open(output_path, 'w', encoding='utf-8') as out_file:
            out_file.writelines(cleaned_lines)

        print(f"Success! Cleaned file saved as: {output_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    clean_chat_log()

os.system('pause')