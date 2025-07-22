import tkinter as tk
from tkinter import ttk, messagebox
from models.database import Database
import re
from typing import Optional

class CRUDApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("CRUD Application")
        self.db = Database()
        
        # Set up the main container
        self.mainframe = ttk.Frame(root, padding="10")
        self.mainframe.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.setup_form()
        self.setup_treeview()
        self.load_records()

    def setup_form(self):
        """Set up the input form."""
        # Form variables
        self.id_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.phone_var = tk.StringVar()

        # Form labels and entries
        ttk.Label(self.mainframe, text="ID:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(self.mainframe, textvariable=self.id_var, state='readonly').grid(row=0, column=1, sticky=(tk.W, tk.E))

        ttk.Label(self.mainframe, text="Name:").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(self.mainframe, textvariable=self.name_var).grid(row=1, column=1, sticky=(tk.W, tk.E))

        ttk.Label(self.mainframe, text="Email:").grid(row=2, column=0, sticky=tk.W)
        ttk.Entry(self.mainframe, textvariable=self.email_var).grid(row=2, column=1, sticky=(tk.W, tk.E))

        ttk.Label(self.mainframe, text="Phone:").grid(row=3, column=0, sticky=tk.W)
        ttk.Entry(self.mainframe, textvariable=self.phone_var).grid(row=3, column=1, sticky=(tk.W, tk.E))

        # Buttons
        button_frame = ttk.Frame(self.mainframe)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Create", command=self.create_record).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Update", command=self.update_record).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete", command=self.delete_record).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_form).pack(side=tk.LEFT, padx=5)

    def setup_treeview(self):
        """Set up the treeview to display records."""
        # Create Treeview
        self.tree = ttk.Treeview(self.mainframe, columns=("ID", "Name", "Email", "Phone"), show="headings")
        
        # Define headings
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Phone", text="Phone")
        
        # Define columns
        self.tree.column("ID", width=50)
        self.tree.column("Name", width=150)
        self.tree.column("Email", width=200)
        self.tree.column("Phone", width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.mainframe, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Grid
        self.tree.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=5, column=2, sticky=(tk.N, tk.S))
        
        # Bind select
        self.tree.bind('<<TreeviewSelect>>', self.item_selected)

    def validate_input(self) -> bool:
        """Validate form input."""
        if not self.name_var.get().strip():
            messagebox.showerror("Error", "Name is required!")
            return False
            
        email = self.email_var.get().strip()
        if not email:
            messagebox.showerror("Error", "Email is required!")
            return False
            
        # Basic email validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            messagebox.showerror("Error", "Invalid email format!")
            return False
            
        return True

    def create_record(self):
        """Create a new record."""
        if not self.validate_input():
            return

        try:
            data = {
                'name': self.name_var.get().strip(),
                'email': self.email_var.get().strip(),
                'phone': self.phone_var.get().strip()
            }
            self.db.create_record(data)
            self.load_records()
            self.clear_form()
            messagebox.showinfo("Success", "Record created successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create record: {str(e)}")

    def update_record(self):
        """Update the selected record."""
        if not self.id_var.get():
            messagebox.showerror("Error", "Please select a record to update!")
            return

        if not self.validate_input():
            return

        try:
            data = {
                'name': self.name_var.get().strip(),
                'email': self.email_var.get().strip(),
                'phone': self.phone_var.get().strip()
            }
            if self.db.update_record(int(self.id_var.get()), data):
                self.load_records()
                self.clear_form()
                messagebox.showinfo("Success", "Record updated successfully!")
            else:
                messagebox.showerror("Error", "Record not found!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update record: {str(e)}")

    def delete_record(self):
        """Delete the selected record."""
        if not self.id_var.get():
            messagebox.showerror("Error", "Please select a record to delete!")
            return

        if messagebox.askyesno("Confirm", "Are you sure you want to delete this record?"):
            try:
                if self.db.delete_record(int(self.id_var.get())):
                    self.load_records()
                    self.clear_form()
                    messagebox.showinfo("Success", "Record deleted successfully!")
                else:
                    messagebox.showerror("Error", "Record not found!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete record: {str(e)}")

    def load_records(self):
        """Load all records into the treeview."""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Load records from database
        try:
            records = self.db.read_all_records()
            for record in records:
                self.tree.insert("", tk.END, values=(
                    record['id'],
                    record['name'],
                    record['email'],
                    record['phone']
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load records: {str(e)}")

    def item_selected(self, event):
        """Handle item selection in treeview."""
        selected_items = self.tree.selection()
        if selected_items:
            item = self.tree.item(selected_items[0])
            values = item['values']
            if values:
                self.id_var.set(values[0])
                self.name_var.set(values[1])
                self.email_var.set(values[2])
                self.phone_var.set(values[3] if values[3] else '')

    def clear_form(self):
        """Clear the input form."""
        self.id_var.set('')
        self.name_var.set('')
        self.email_var.set('')
        self.phone_var.set('')
        # Deselect any selected items in the treeview
        for selected_item in self.tree.selection():
            self.tree.selection_remove(selected_item)
