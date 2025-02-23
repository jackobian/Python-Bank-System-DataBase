import sqlite3
from tkinter import ttk, messagebox

class AccountModule:
    def __init__(self, frame):
        self.frame = frame
        self.create_accounts_form()

    def create_accounts_form(self):
        ttk.Label(self.frame, text="AccountID").grid(row=0, column=0, padx=5, pady=5)
        self.account_id_entry = ttk.Entry(self.frame)
        self.account_id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="ClientID").grid(row=1, column=0, padx=5, pady=5)
        self.account_client_id_entry = ttk.Entry(self.frame)
        self.account_client_id_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="AccountType").grid(row=2, column=0, padx=5, pady=5)
        self.account_type_entry = ttk.Entry(self.frame)
        self.account_type_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="Balance").grid(row=3, column=0, padx=5, pady=5)
        self.balance_entry = ttk.Entry(self.frame)
        self.balance_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="OpenDate").grid(row=4, column=0, padx=5, pady=5)
        self.open_date_entry = ttk.Entry(self.frame)
        self.open_date_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Button(self.frame, text="Save", command=self.save_account).grid(row=5, column=0, padx=5, pady=5)
        ttk.Button(self.frame, text="Delete", command=self.delete_account).grid(row=5, column=1, padx=5, pady=5)
        ttk.Button(self.frame, text="Update", command=self.update_account).grid(row=5, column=2, padx=5, pady=5)
        ttk.Button(self.frame, text="Search", command=self.search_accounts).grid(row=5, column=3, padx=5, pady=5)

        self.accounts_tree = ttk.Treeview(self.frame, columns=("AccountID", "ClientID", "AccountType", "Balance", "OpenDate"), show="headings")
        self.accounts_tree.heading("AccountID", text="AccountID")
        self.accounts_tree.heading("ClientID", text="ClientID")
        self.accounts_tree.heading("AccountType", text="AccountType")
        self.accounts_tree.heading("Balance", text="Balance")
        self.accounts_tree.heading("OpenDate", text="OpenDate")
        self.accounts_tree.grid(row=6, column=0, columnspan=4, padx=5, pady=5)

        self.populate_accounts_tree()

    def save_account(self):
        try:
            conn = sqlite3.connect('bank.db')
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO Accounts (ClientID, AccountType, Balance, OpenDate) VALUES (?, ?, ?, ?)''',
                           (self.account_client_id_entry.get(), self.account_type_entry.get(), self.balance_entry.get(), self.open_date_entry.get()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Account saved successfully.")
            self.populate_accounts_tree()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_account(self):
        try:
            conn = sqlite3.connect('bank.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM Accounts WHERE AccountID = ?', (self.account_id_entry.get(),))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Account deleted successfully.")
            self.populate_accounts_tree()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_account(self):
        try:
            conn = sqlite3.connect('bank.db')
            cursor = conn.cursor()
            cursor.execute('''UPDATE Accounts SET ClientID=?, AccountType=?, Balance=?, OpenDate=? WHERE AccountID=?''',
                           (self.account_client_id_entry.get(), self.account_type_entry.get(), self.balance_entry.get(), self.open_date_entry.get(), self.account_id_entry.get()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Account updated successfully.")
            self.populate_accounts_tree()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def search_accounts(self):
        try:
            conn = sqlite3.connect('bank.db')
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM Accounts WHERE ClientID LIKE ? AND AccountType LIKE ?''',
                           (f'%{self.account_client_id_entry.get()}%', f'%{self.account_type_entry.get()}%'))
            rows = cursor.fetchall()
            conn.close()
            self.accounts_tree.delete(*self.accounts_tree.get_children())
            for row in rows:
                self.accounts_tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def populate_accounts_tree(self):
        try:
            conn = sqlite3.connect('bank.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Accounts')
            rows = cursor.fetchall()
            conn.close()
            self.accounts_tree.delete(*self.accounts_tree.get_children())
            for row in rows:
                self.accounts_tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Error", str(e))
