import sqlite3
from tkinter import ttk, messagebox

class ClientModule:
    def __init__(self, frame):
        self.frame = frame
        self.create_clients_form()

    def create_clients_form(self):
        ttk.Label(self.frame, text="ClientID").grid(row=0, column=0, padx=5, pady=5)
        self.client_id_entry = ttk.Entry(self.frame)
        self.client_id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="First Name").grid(row=1, column=0, padx=5, pady=5)
        self.client_first_name_entry = ttk.Entry(self.frame)
        self.client_first_name_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="Last Name").grid(row=2, column=0, padx=5, pady=5)
        self.client_last_name_entry = ttk.Entry(self.frame)
        self.client_last_name_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="Address").grid(row=3, column=0, padx=5, pady=5)
        self.client_address_entry = ttk.Entry(self.frame)
        self.client_address_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="Phone Number").grid(row=4, column=0, padx=5, pady=5)
        self.client_phone_number_entry = ttk.Entry(self.frame)
        self.client_phone_number_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="Email").grid(row=5, column=0, padx=5, pady=5)
        self.client_email_entry = ttk.Entry(self.frame)
        self.client_email_entry.grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="Client Type").grid(row=6, column=0, padx=5, pady=5)
        self.client_type_entry = ttk.Entry(self.frame)
        self.client_type_entry.grid(row=6, column=1, padx=5, pady=5)

        ttk.Button(self.frame, text="Save", command=self.save_client).grid(row=7, column=0, padx=5, pady=5)
        ttk.Button(self.frame, text="Delete", command=self.delete_client).grid(row=7, column=1, padx=5, pady=5)
        ttk.Button(self.frame, text="Update", command=self.update_client).grid(row=7, column=2, padx=5, pady=5)
        ttk.Button(self.frame, text="Search", command=self.search_clients).grid(row=7, column=3, padx=5, pady=5)

        self.clients_tree = ttk.Treeview(self.frame, columns=("ClientID", "First Name", "Last Name", "Address", "Phone Number", "Email", "Client Type"), show="headings")
        self.clients_tree.heading("ClientID", text="ClientID")
        self.clients_tree.heading("First Name", text="First Name")
        self.clients_tree.heading("Last Name", text="Last Name")
        self.clients_tree.heading("Address", text="Address")
        self.clients_tree.heading("Phone Number", text="Phone Number")
        self.clients_tree.heading("Email", text="Email")
        self.clients_tree.heading("Client Type", text="Client Type")
        self.clients_tree.grid(row=8, column=0, columnspan=4, padx=5, pady=5)

        self.populate_clients_tree()

    def save_client(self):
        try:
            conn = sqlite3.connect('bank.db')
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO Clients (ClientFirstName, ClientLastName, ClientAddress, PhoneNumber, Email, ClientType) 
                              VALUES (?, ?, ?, ?, ?, ?)''',
                           (self.client_first_name_entry.get(), self.client_last_name_entry.get(),
                            self.client_address_entry.get(), self.client_phone_number_entry.get(),
                            self.client_email_entry.get(), self.client_type_entry.get()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Client saved successfully.")
            self.populate_clients_tree()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_client(self):
        try:
            conn = sqlite3.connect('bank.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM Clients WHERE ClientID = ?', (self.client_id_entry.get(),))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Client deleted successfully.")
            self.populate_clients_tree()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_client(self):
        try:
            conn = sqlite3.connect('bank.db')
            cursor = conn.cursor()
            cursor.execute('''UPDATE Clients SET ClientFirstName=?, ClientLastName=?, ClientAddress=?, PhoneNumber=?, Email=?, ClientType=? WHERE ClientID=?''',
                           (self.client_first_name_entry.get(), self.client_last_name_entry.get(),
                            self.client_address_entry.get(), self.client_phone_number_entry.get(),
                            self.client_email_entry.get(), self.client_type_entry.get(), self.client_id_entry.get()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Client updated successfully.")
            self.populate_clients_tree()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def search_clients(self):
        try:
            conn = sqlite3.connect('bank.db')
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM Clients WHERE ClientFirstName LIKE ? AND ClientLastName LIKE ?''',
                           (f'%{self.client_first_name_entry.get()}%', f'%{self.client_last_name_entry.get()}%'))
            rows = cursor.fetchall()
            conn.close()
            self.clients_tree.delete(*self.clients_tree.get_children())
            for row in rows:
                self.clients_tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def populate_clients_tree(self):
        try:
            conn = sqlite3.connect('bank.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Clients')
            rows = cursor.fetchall()
            conn.close()
            self.clients_tree.delete(*self.clients_tree.get_children())
            for row in rows:
                self.clients_tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Error", str(e))
