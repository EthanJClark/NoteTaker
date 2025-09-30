import customtkinter as ctk
import tkinter
from tkinter import filedialog, messagebox, simpledialog
import ai
import json



DEFAULT_TEXT = ("Arial", 20)


root = ctk.CTk()
root.title("Burpatron")
root.geometry("800x600")

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")
window_bg_color = root.cget("fg_color") 

menu_frame = ctk.CTkFrame(root, height = 100, fg_color=window_bg_color)
menu_frame.pack(fill = "x", side = "top")

tabview = ctk.CTkTabview(master= root)
tabview.pack(expand = True, fill = "both",side = "left")






def optionmenu_callback(choice):
    print("OptionMenu selected:", choice)

    if "New Note" in choice:
        create_new_tab()
    if "Rename" in choice:
        rename_note()
    if "Save" in choice:
        save_notes()
    if "Import" in choice:
        import_notes()

    optionmenu.set("File")

optionmenu = ctk.CTkOptionMenu(
        master=menu_frame,
        values=[
            "File",
            ("Save   Ctrl+S"),
            "New Note   Ctrl+Tab",
            "Rename   Ctrl+Space",
            "Import   Ctrl+I"
            ],
        command=optionmenu_callback  # Assign the callback function
    )
optionmenu.pack(side="left", padx=5)

optionmenu.set("File")

def rename_note(event = None):
    
    old_tab_name = tabview.get()
    dialog = ctk.CTkInputDialog(text="New name?", title= "Rename",font= DEFAULT_TEXT)
    tab_name = dialog.get_input()
    try:
        tabview._segmented_button._buttons_dict[old_tab_name].configure(text=tab_name)
    except:
        pass

def import_notes(event = None):
    # current_tab = tabview.get()
    # if current_tab:
        # textbox = tabview._tab_dict[current_tab].winfo_children()[0]
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, "r") as file:
                    content = file.read()

                tab_name = file_path.split("/")[-1].split("\\")[-1].split(".")[0]
                create_new_tab(tab_name=tab_name, default_tab=True)
                current_tab = tabview.get()
                textbox = tabview._tab_dict[current_tab].winfo_children()[0]

                textbox.delete("1.0", "end")
                textbox.insert("1.0", content)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import notes: {e}")

def get_json():
    with open("existing_files.json") as file:
        data = json.load(file)
    return data


def update_json(content):
    try:
        # Load existing data from the JSON file
        with open("existing_files.json", "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # If the file doesn't exist or is invalid, start with an empty dictionary
        data = {}

    # Add the new content to the existing data
    data.update(content)

    # Write the updated data back to the JSON file
    with open("existing_files.json", "w") as file:
        json.dump(data, file, indent=4)

    print(f"Updated JSON file with: {content}")

def delete_tab(event = None):
    current_tab = tabview.get()
    if current_tab:
        result = messagebox.askyesno("Confirmation", "Close Current tab?\n  Data may be lost")
        if result:
            tabview.delete(current_tab) 

def create_new_tab(tab_name = None, event = None, default_tab = False):
    if not default_tab:
        dialog = ctk.CTkInputDialog(text="New note name?", title= "New note", font=DEFAULT_TEXT)
        tab_name = dialog.get_input()
    

    if tab_name != "" and tab_name != None:
        tab_1 = tabview.add(tab_name)

        tabview.set(tab_name)

        label_tab1 = ctk.CTkTextbox(master=tab_1, undo = True, wrap = "word", font=("Arial", 20))
        label_tab1.pack(padx = 10, fill = "both", expand = True)

        # command binds
        
        print(tabview._tab_dict.keys())

def save_notes(event = None):
    files = get_json()
    print(files)
    current_tab = tabview.get()  # Get the name of the currently selected tab
    if current_tab:
        # Retrieve the CTkTextbox widget from the current tab
        textbox = tabview._tab_dict[current_tab].winfo_children()[0]
        if isinstance(textbox, ctk.CTkTextbox):
            # Get and print the content of the textbox
            # content = textbox.get("1.0", "end")  # Get all text from the textbox
            if current_tab in files:
                file_path = files[current_tab]
                if file_path:
                    try:
                        with open(file_path, "w") as file:
                            file.write(textbox.get("1.0", "end"))
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to save notes: {e}")
            else:
                new_file_entry = {}
                file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
                if file_path != "":
                    new_file_entry[current_tab] = file_path
                    update_json(new_file_entry)
                    if file_path:
                        try:
                            with open(file_path, "w") as file:
                                file.write(textbox.get("1.0", "end"))
                        except Exception as e:
                            messagebox.showerror("Error", f"Failed to save notes: {e}")




def call_ai():
    current_tab = tabview.get()  # Get the name of the currently selected tab
    if current_tab:
        # Retrieve the CTkTextbox widget from the current tab
        textbox = tabview._tab_dict[current_tab].winfo_children()[0]
        notes = (textbox.get("1.0", "end"))
        organized_notes = ai.organize_notes(notes)
        textbox.delete("1.0", "end")
        textbox.insert("1.0", organized_notes)

def custom_call_ai(event = None):
    current_tab = tabview.get()  # Get the name of the currently selected tab
    dialog = ctk.CTkInputDialog(text="How can I tweak your writing?", title= "AI assistant",font=DEFAULT_TEXT)
    prompt = dialog.get_input()

    if current_tab:
        # Retrieve the CTkTextbox widget from the current tab
        textbox = tabview._tab_dict[current_tab].winfo_children()[0]
        notes = (textbox.get("1.0", "end"))
        organized_notes = ai.custom_prompt(notes, prompt)
        textbox.delete("1.0", "end")
        textbox.insert("1.0", organized_notes)


organize_button = ctk.CTkButton(menu_frame, text="Organize", command=call_ai, width=75)
organize_button.pack(side="left", padx=3)

rewrite_button = ctk.CTkButton(menu_frame, text="Writing Assist", command=custom_call_ai, width=75)
rewrite_button.pack(side="left", padx=3)

close_button = ctk.CTkButton(master= menu_frame,text="Close", width=75, command=delete_tab)
close_button.pack(side="right", padx=5)


root.bind("<Control-s>", save_notes)
root.bind("<Control-Tab>", create_new_tab)
root.bind("<Control-r>", rename_note)
root.bind("<Control-i>", import_notes)
root.bind("<Control-space>", custom_call_ai)
root.bind("<Escape>", delete_tab)



root.mainloop()
