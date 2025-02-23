import sqlite3
from tkinter import ttk, messagebox

class ReportModule:
    def __init__(self, frame):
        self.frame = frame
        self.create_report_forms()

    def create_report_forms(self):
        self.create_monthly_transaction_report_form()
        self.create_client_account_summary_form()

    # 📌 **Monthly Transaction Report**
    def create_monthly_transaction_report_form(self):
        frame = ttk.LabelFrame(self.frame, text="Monthly Transaction Report")
        frame.pack(padx=10, pady=10, fill="both", expand=True)

        ttk.Label(frame, text="Month (MM):").grid(row=0, column=0, padx=5, pady=5)
        self.month_entry = ttk.Entry(frame)
        self.month_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Year (YYYY):").grid(row=1, column=0, padx=5, pady=5)
        self.year_entry = ttk.Entry(frame)
        self.year_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(frame, text="Generate", command=self.generate_monthly_transaction_report).grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        self.monthly_transactions_tree = ttk.Treeview(frame, columns=("TransactionID", "AccountID", "Amount", "TransactionDate", "Type"), show="headings")
        self.monthly_transactions_tree.heading("TransactionID", text="TransactionID")
        self.monthly_transactions_tree.heading("AccountID", text="AccountID")
        self.monthly_transactions_tree.heading("Amount", text="Amount")
        self.monthly_transactions_tree.heading("TransactionDate", text="TransactionDate")
        self.monthly_transactions_tree.heading("Type", text="Type")
        self.monthly_transactions_tree.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    def generate_monthly_transaction_report(self):
        try:
            month = self.month_entry.get()
            year = self.year_entry.get()

            conn = sqlite3.connect('bank.db')
            cursor = conn.cursor()

            cursor.execute('''
                SELECT TransactionID, AccountID, Amount, TransactionDate, Type
                FROM Transactions
                WHERE strftime('%m', TransactionDate) = ? AND strftime('%Y', TransactionDate) = ?
            ''', (month, year))

            rows = cursor.fetchall()
            conn.close()

            self.monthly_transactions_tree.delete(*self.monthly_transactions_tree.get_children())
            for row in rows:
                self.monthly_transactions_tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # 📌 **Client Account Summary**
    def create_client_account_summary_form(self):
        frame = ttk.LabelFrame(self.frame, text="Client Account Summary")
        frame.pack(padx=10, pady=10, fill="both", expand=True)

        ttk.Label(frame, text="ClientID:").grid(row=0, column=0, padx=5, pady=5)
        self.summary_client_id_entry = ttk.Entry(frame)
        self.summary_client_id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(frame, text="Generate", command=self.generate_client_account_summary).grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        self.client_account_summary_tree = ttk.Treeview(frame, columns=("AccountID", "AccountType", "Balance", "OpenDate"), show="headings")
        self.client_account_summary_tree.heading("AccountID", text="AccountID")
        self.client_account_summary_tree.heading("AccountType", text="AccountType")
        self.client_account_summary_tree.heading("Balance", text="Balance")
        self.client_account_summary_tree.heading("OpenDate", text="OpenDate")
        self.client_account_summary_tree.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    def generate_client_account_summary(self):
        try:
            client_id = self.summary_client_id_entry.get()

            conn = sqlite3.connect('bank.db')
            cursor = conn.cursor()

            cursor.execute('''
                SELECT AccountID, AccountType, Balance, OpenDate
                FROM Accounts
                WHERE ClientID = ?
            ''', (client_id,))

            rows = cursor.fetchall()
            conn.close()

            self.client_account_summary_tree.delete(*self.client_account_summary_tree.get_children())
            for row in rows:
                self.client_account_summary_tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Error", str(e))
