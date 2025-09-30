import ttkbootstrap
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

# Initialize the main window
root = tk.Tk()
root.title("NoteTaker")
root.geometry("800x600")
style = ttkbootstrap.Style(theme="journal")

# Configure styles
style.configure("TNotebook.Tab", font=("TkDefaultFont", 14, "bold"))

# Create a frame for buttons and place it at the top
button_frame = tk.Frame(root)
button_frame.pack(fill="x", padx=10, pady=5, side="top")

# Create a notebook (tabs container)
notebook = ttkbootstrap.Notebook(root)
notebook.pack(expand=True, fill="both", padx=10, pady=10)

# Function to create a new tab
def create_new_tab():
    frame = tk.Frame(notebook)
    text_area = tk.Text(frame, wrap="word", font=("TkDefaultFont", 12))
    text_area.pack(expand=True, fill="both", padx=10, pady=10)
    notebook.add(frame, text=f"Note {len(notebook.tabs()) + 1}")

# Function to save notes from the current tab
def save_notes():
    current_tab = notebook.select()
    if current_tab:
        text_area = notebook.nametowidget(current_tab).winfo_children()[0]
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, "w") as file:
                    file.write(text_area.get("1.0", tk.END))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save notes: {e}")

# Function to import notes into the current tab
def import_notes():
    current_tab = notebook.select()
    if current_tab:
        text_area = notebook.nametowidget(current_tab).winfo_children()[0]
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, "r") as file:
                    content = file.read()
                text_area.delete("1.0", tk.END)
                text_area.insert("1.0", content)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import notes: {e}")

# Function to close the current tab
def close_current_tab():
    current_tab = notebook.select()
    if current_tab:
        notebook.forget(current_tab)

# Function to rename the current tab
def rename_current_tab():
    current_tab = notebook.select()
    if current_tab:
        new_name = simpledialog.askstring("Rename Tab", "Enter new name for the tab:")
        if new_name:
            notebook.tab(current_tab, text=new_name)

# Add buttons for Save, Import, New Tab, Close Tab, and Rename Tab
save_button = ttkbootstrap.Button(button_frame, text="Save Notes", command=save_notes, bootstyle="primary")
save_button.pack(side="left", padx=5)

import_button = ttkbootstrap.Button(button_frame, text="Import Notes", command=import_notes, bootstyle="success")
import_button.pack(side="left", padx=5)

new_tab_button = ttkbootstrap.Button(button_frame, text="New Tab", command=create_new_tab, bootstyle="secondary")
new_tab_button.pack(side="left", padx=5)

close_tab_button = ttkbootstrap.Button(button_frame, text="Close Tab", command=close_current_tab, bootstyle="danger")
close_tab_button.pack(side="left", padx=5)

rename_tab_button = ttkbootstrap.Button(button_frame, text="Rename Tab", command=rename_current_tab, bootstyle="info")
rename_tab_button.pack(side="left", padx=5)

# Create the first tab by default
create_new_tab()

# Run the application
root.mainloop()