import tkinter as tk
from tkinter import ttk, messagebox
from library.models import DigitalLibrary, BookNotAvailableError, Book

# Initialize the digital library
library = DigitalLibrary()

root = tk.Tk()
root.title("Library Management System")
root.geometry("600x500")

# Variables
title_var = tk.StringVar()
author_var = tk.StringVar()
isbn_var = tk.StringVar()
size_var = tk.StringVar()
ebook_check = tk.BooleanVar()

# Functions
def toggle_ebook():
    if ebook_check.get():
        size_entry.config(state='normal')
    else:
        size_entry.delete(0, tk.END)
        size_entry.config(state='disabled')

def add_book():
    title = title_var.get()
    author = author_var.get()
    isbn = isbn_var.get()
    size = size_var.get()

    if not (title and author and isbn):
        messagebox.showerror("Input Error", "Title, Author, and ISBN are required.")
        return

    if ebook_check.get():
        try:
            size_mb = float(size)
            library.add_ebook(title, author, isbn, size_mb)
        except ValueError:
            messagebox.showerror("Input Error", "eBook size must be a number.")
            return
    else:
        book = Book(title, author, isbn)
        library.add_book(book)

    messagebox.showinfo("Success", "Book added successfully!")
    update_book_list()
    clear_fields()

def clear_fields():
    title_var.set("")
    author_var.set("")
    isbn_var.set("")
    size_var.set("")
    ebook_check.set(False)
    toggle_ebook()

def update_book_list():
    book_list.delete(0, tk.END)
    for book in library:
        book_list.insert(tk.END, str(book))

def lend_selected():
    selection = book_list.curselection()
    if not selection:
        messagebox.showwarning("Select Book", "Select a book to lend.")
        return
    book_str = book_list.get(selection[0])
    isbn = book_str.split("ISBN: ")[-1].split(")")[0]
    try:
        library.lend_book(isbn)
        messagebox.showinfo("Success", f"Book lent: {book_str}")
        update_book_list()
    except BookNotAvailableError as e:
        messagebox.showerror("Unavailable", str(e))

# Layout
form_frame = ttk.LabelFrame(root, text="Add New Book")
form_frame.pack(fill="x", padx=10, pady=10)

# Title
ttk.Label(form_frame, text="Title:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_title = ttk.Entry(form_frame, textvariable=title_var)
entry_title.grid(row=0, column=1, padx=5, pady=5)

# Author
ttk.Label(form_frame, text="Author:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_author = ttk.Entry(form_frame, textvariable=author_var)
entry_author.grid(row=1, column=1, padx=5, pady=5)

# ISBN
ttk.Label(form_frame, text="ISBN:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
entry_isbn = ttk.Entry(form_frame, textvariable=isbn_var)
entry_isbn.grid(row=2, column=1, padx=5, pady=5)

# eBook Checkbox
ebook_cb = ttk.Checkbutton(form_frame, text="Is eBook?", variable=ebook_check, command=toggle_ebook)
ebook_cb.grid(row=3, column=0, padx=5, pady=5, sticky="e")

# Size (MB)
ttk.Label(form_frame, text="Size (MB):").grid(row=3, column=1, padx=5, pady=5, sticky="w")
size_entry = ttk.Entry(form_frame, textvariable=size_var, state='disabled')
size_entry.grid(row=3, column=1, padx=100, pady=5)

# Add Button
ttk.Button(form_frame, text="Add Book", command=add_book).grid(row=4, column=0, columnspan=2, pady=10)

# Book List
book_list = tk.Listbox(root, height=10, width=80)
book_list.pack(padx=10, pady=10)

# Lend Button
ttk.Button(root, text="Lend Selected Book", command=lend_selected).pack(pady=5)

update_book_list()
root.mainloop()
