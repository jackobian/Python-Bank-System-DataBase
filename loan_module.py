import sqlite3
from tkinter import ttk, messagebox

class LoanModule:
    def __init__(self, frame):
        self.frame = frame
        self.create_loans_form()

    def create_loans_form(self):
        ttk.Label(self.frame, text="LoanID").grid(row=0, column=0, padx=5, pady=5)
        self.loan_id_entry = ttk.Entry(self.frame)
        self.loan_id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="ClientID").grid(row=1, column=0, padx=5, pady=5)
        self.loan_client_id_entry = ttk.Entry(self.frame)
        self.loan_client_id_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="Loan Amount").grid(row=2, column=0, padx=5, pady=5)
        self.loan_amount_entry = ttk.Entry(self.frame)
        self.loan_amount_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="Interest Rate (%)").grid(row=3, column=0, padx=5, pady=5)
        self.interest_rate_entry = ttk.Entry(self.frame)
        self.interest_rate_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="Start Date").grid(row=4, column=0, padx=5, pady=5)
        self.start_date_entry = ttk.Entry(self.frame)
        self.start_date_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="End Date").grid(row=5, column=0, padx=5, pady=5)
        self.end_date_entry = ttk.Entry(self.frame)
        self.end_date_entry.grid(row=5, column=1, padx=5, pady=5)

        ttk.Button(self.frame, text="Save", command=self.save_loan).grid(row=6, column=0, padx=5, pady=5)
        ttk.Button(self.frame, text="Delete", command=self.delete_loan).grid(row=6, column=1, padx=5, pady=5)
        ttk.Button(self.frame, text="Update", command=self.update_loan).grid(row=6, column=2, padx=5, pady=5)
        ttk.Button(self.frame, text="Search", command=self.search_loans).grid(row=6, column=3, padx=5, pady=5)

        self.loans_tree = ttk.Treeview(self.frame, columns=("LoanID", "ClientID", "Loan Amount", "Interest Rate", "Start Date", "End Date"), show="headings")
        self.loans_tree.heading("LoanID", text="LoanID")
        self.loans_tree.heading("ClientID", text="ClientID")
        self.loans_tree.heading("Loan Amount", text="Loan Amount")
        self.loans_tree.heading("Interest Rate", text="Interest Rate")
        self.loans_tree.heading("Start Date", text="Start Date")
        self.loans_tree.heading("End Date", text="End Date")
        self.loans_tree.grid(row=7, column=0, columnspan=4, padx=5, pady=5)

        self.populate_loans_tree()

    def save_loan(self):
        try:
            conn = sqlite3.connect('bank.db')
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO Loans (ClientID, LoanAmount, InterestRate, StartDate, EndDate)
                              VALUES (?, ?, ?, ?, ?)''',
                           (self.loan_client_id_entry.get(), self.loan_amount_entry.get(),
                            self.interest_rate_entry.get(), self.start_date_entry.get(), self.end_date_entry.get()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Loan saved successfully.")
            self.populate_loans_tree()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_loan(self):
        try:
            conn = sqlite3.connect('bank.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM Loans WHERE LoanID = ?', (self.loan_id_entry.get(),))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Loan deleted successfully.")
            self.populate_loans_tree()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_loan(self):
        try:
            conn = sqlite3.connect('bank.db')
            cursor = conn.cursor()
            cursor.execute('''UPDATE Loans SET ClientID=?, LoanAmount=?, InterestRate=?, StartDate=?, EndDate=? WHERE LoanID=?''',
                           (self.loan_client_id_entry.get(), self.loan_amount_entry.get(),
                            self.interest_rate_entry.get(), self.start_date_entry.get(), self.end_date_entry.get(), self.loan_id_entry.get()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Loan updated successfully.")
            self.populate_loans_tree()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def search_loans(self):
        try:
            conn = sqlite3.connect('bank.db')
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM Loans WHERE ClientID LIKE ?''',
                           (f'%{self.loan_client_id_entry.get()}%',))
            rows = cursor.fetchall()
            conn.close()
            self.loans_tree.delete(*self.loans_tree.get_children())
            for row in rows:
                self.loans_tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def populate_loans_tree(self):
        try:
            conn = sqlite3.connect('bank.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Loans')
            rows = cursor.fetchall()
            conn.close()
            self.loans_tree.delete(*self.loans_tree.get_children())
            for row in rows:
                self.loans_tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Error", str(e))
