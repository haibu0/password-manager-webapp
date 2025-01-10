import webbrowser
from tkinter import *
import random
import string
import pyperclip
import json
from collections import Counter
import os
from tkinter import messagebox, PhotoImage
from PIL import Image, ImageTk

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    password_entry.delete(0, END)
    length = 20
    chars = string.ascii_letters + string.digits + '!@#$%^&*()'
    generated_password = ''.join(random.choice(chars) for i in range(length))
    password_entry.insert(0, generated_password)
    pyperclip.copy(generated_password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_entries():
    website=website_entry.get()
    password=password_entry.get()
    username=username_entry.get()
    input_data = {
        website: {
            "username": username,
            "password": password,
        }
    }

    if len(website)==0 or len(password)==0 or len(username)==0:
        messagebox.showinfo("Information", "Please do not leave any fields empty!")
    else:
        try:
            with open('saved_passwords_data.json', mode='r') as saved_passwords_file:
                data = json.load(saved_passwords_file)
        except FileNotFoundError:
            with open('saved_passwords_data.json', mode='w') as saved_passwords_file:
                json.dump(input_data, saved_passwords_file,indent=4)
        else:
            data.update(input_data)
            confirm = messagebox.askokcancel(
                "Confirm Save",  # Title
                f"Website: {website_entry.get()}\n"
                f"Username: {username_entry.get()}\n"
                f"Password: {password_entry.get()}\n"
                "Is it ok to save?"
            )
            if confirm:
                with open('saved_passwords_data.json', mode='w') as saved_passwords_file:
                    json.dump(data, saved_passwords_file, indent=4)
                website_entry.delete(0, END)
                password_entry.delete(0, END)

# ---------------------------- FILE COMMANDS ------------------------------- #
def get_most_used_email():
    usernames = []
    try:
        with open('saved_passwords_data.json', mode='r') as f:
            data = json.load(f)
    except:
        return ''
    else:
        for key,value in data.items():
            usernames.append(value['username'])
        most_common = Counter(usernames).most_common(1)
        try:
            return most_common[0][0]
        except IndexError:
            return ''

def find_password():
    searching_for = website_entry.get()
    try:
        with open('saved_passwords_data.json',mode='r') as f:
            data = json.load(f)

    except FileNotFoundError:
        messagebox.showinfo("Info", f"Data file not found!")

    else:
        if searching_for in data:
            username = data[searching_for]['username']
            password = data[searching_for]['password']

            messagebox.showinfo(searching_for,f"Username: {username}\nPassword: {password}\nPassword copied to clipboard")
            pyperclip.copy(password)
        else:
            messagebox.showinfo("Info",f"No saved data for this website!")

def open_file():
    file_path = 'saved_passwords_data.json'
    if os.path.exists(file_path):
        webbrowser.open(file_path)
    else:
        messagebox.showinfo('FileNotFoundError',f"The file '{file_path}' does not exist.")

def clear_file():
    confirm = messagebox.askokcancel('Info','Are you sure you would like to clear the data file?')
    if confirm:
        with open('saved_passwords_data.json', mode='w') as f:
            json.dump({}, f)
        messagebox.showinfo('Info', 'Data File Cleared')

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title('Password Manager')
window.config(padx=50, pady=50, bg="#F4F4F9")

# Logo and Image

img = Image.open('image2.png')
img = img.resize((200,200))
logo_img = ImageTk.PhotoImage(img)

canvas = Canvas(window, width=200, height=200, bg="#F4F4F9", bd=0, highlightthickness=0)
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1, pady=10)

canvas.image = logo_img

# Labels
website_label = Label(window, text="Website: ", font=("Arial", 12, "bold"), bg="#F4F4F9")
website_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

username_label = Label(window, text="Username/Email: ", font=("Arial", 12, "bold"), bg="#F4F4F9")
username_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

password_label = Label(window, text="Password: ", font=("Arial", 12, "bold"), bg="#F4F4F9")
password_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

# Entries
website_entry = Entry(window, width=35, font=("Arial", 12), borderwidth=2)
website_entry.grid(row=1, column=1, padx=10, pady=5)
website_entry.focus()

username_entry = Entry(window, width=55, font=("Arial", 12), borderwidth=2)
username_entry.grid(row=2, column=1, columnspan=2, padx=10, pady=5)
username_entry.insert(0, get_most_used_email())

password_entry = Entry(window, width=35, font=("Arial", 12), borderwidth=2)
password_entry.grid(row=3, column=1, padx=10, pady=5)

# Buttons
search_button = Button(window, text="Search", command=find_password, font=("Arial", 12, "bold"), bg="#0099FF", fg="white", relief="flat", width=15)
search_button.grid(row=1, column=2, padx=10, pady=5)

generate_password_button = Button(window, text="Generate Password", command=generate_password, font=("Arial", 12, "bold"), bg="#0099FF", fg="white", relief="flat", width=15)
generate_password_button.grid(row=3, column=2, padx=10, pady=5)

add_button = Button(window, text="Add", command=add_entries, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", relief="flat", width=40)
add_button.grid(row=4, column=1, columnspan=2, padx=10, pady=10)

open_file_button = Button(window, text="Open File", command=open_file, font=("Arial", 12, "bold"), bg="#FF9800", fg="white", relief="flat", width=20)
open_file_button.grid(row=5, column=1, columnspan=2, padx=10, pady=5)

clear_file_button = Button(window, text="Clear File", command=clear_file, font=("Arial", 12, "bold"), bg="#FF5722", fg="white", relief="flat", width=20)
clear_file_button.grid(row=6, column=1, columnspan=2, padx=10, pady=5)


# Run the UI
window.mainloop()
