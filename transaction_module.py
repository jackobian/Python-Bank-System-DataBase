import sqlite3
from tkinter import ttk, messagebox

class TransactionModule:
    def __init__(self, frame):
        self.frame = frame
        self.create_transactions_form()

    def create_transactions_form(self):
        ttk.Label(self.frame, text="TransactionID").grid(row=0, column=0, padx=5, pady=5)
        self.transaction_id_entry = ttk.Entry(self.frame)
        self.transaction_id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="AccountID").grid(row=1, column=0, padx=5, pady=5)
        self.transaction_account_id_entry = ttk.Entry(self.frame)
        self.transaction_account_id_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="Amount").grid(row=2, column=0, padx=5, pady=5)
        self.transaction_amount_entry = ttk.Entry(self.frame)
        self.transaction_amount_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="TransactionDate").grid(row=3, column=0, padx=5, pady=5)
        self.transaction_date_entry = ttk.Entry(self.frame)
        self.transaction_date_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="Type").grid(row=4, column=0, padx=5, pady=5)
        self.transaction_type_entry = ttk.Entry(self.frame)
        self.transaction_type_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Button(self.frame, text="Save", command=self.save_transaction).grid(row=5, column=0, padx=5, pady=5)
        ttk.Button(self.frame, text="Delete", command=self.delete_transaction).grid(row=5, column=1, padx=5, pady=5)
        ttk.Button(self.frame, text="Update", command=self.update_transaction).grid(row=5, column=2, padx=5, pady=5)
        ttk.Button(self.frame, text="Search", command=self.search_transactions).grid(row=5, column=3, padx=5, pady=5)

        self.transactions_tree = ttk.Treeview(self.frame, columns=("TransactionID", "AccountID", "Amount", "TransactionDate", "Type"), show="headings")
        self.transactions_tree.heading("TransactionID", text="TransactionID")
        self.transactions_tree.heading("AccountID", text="AccountID")
        self.transactions_tree.heading("Amount", text="Amount")
        self.transactions_tree.heading("TransactionDate", text="TransactionDate")
        self.transactions_tree.heading("Type", text="Type")
        self.transactions_tree.grid(row=6, column=0, columnspan=4, padx=5, pady=5)

        self.populate_transactions_tree()

    def save_transaction(self):
        try:
            conn = sqlite3.connect('bank.db')
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO Transactions (AccountID, Amount, TransactionDate, Type) VALUES (?, ?, ?, ?)''',
                           (self.transaction_account_id_entry.get(), self.transaction_amount_entry.get(),
                            self.transaction_date_entry.get(), self.transaction_type_entry.get()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Transaction saved successfully.")
            self.populate_transactions_tree()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_transaction(self):
        try:
            conn = sqlite3.connect('bank.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM Transactions WHERE TransactionID = ?', (self.transaction_id_entry.get(),))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Transaction deleted successfully.")
            self.populate_transactions_tree()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_transaction(self):
        try:
            conn = sqlite3.connect('bank.db')
            cursor = conn.cursor()
            cursor.execute('''UPDATE Transactions SET AccountID=?, Amount=?, TransactionDate=?, Type=? WHERE TransactionID=?''',
                           (self.transaction_account_id_entry.get(), self.transaction_amount_entry.get(),
                            self.transaction_date_entry.get(), self.transaction_type_entry.get(), self.transaction_id_entry.get()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Transaction updated successfully.")
            self.populate_transactions_tree()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def search_transactions(self):
        try:
            conn = sqlite3.connect('bank.db')
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM Transactions WHERE AccountID LIKE ? AND Type LIKE ?''',
                           (f'%{self.transaction_account_id_entry.get()}%', f'%{self.transaction_type_entry.get()}%'))
            rows = cursor.fetchall()
            conn.close()
            self.transactions_tree.delete(*self.transactions_tree.get_children())
            for row in rows:
                self.transactions_tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def populate_transactions_tree(self):
        try:
            conn = sqlite3.connect('bank.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Transactions')
            rows = cursor.fetchall()
            conn.close()
            self.transactions_tree.delete(*self.transactions_tree.get_children())
            for row in rows:
                self.transactions_tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Error", str(e))
