import tkinter as tk
from tkinter import ttk
from client_module import ClientModule
from account_module import AccountModule
from transaction_module import TransactionModule
from employee_module import EmployeeModule
from branch_module import BranchModule
from loan_module import LoanModule
from report_module import ReportModule


class BankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bank Management System")

        menubar = tk.Menu(root)
        root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=root.quit)

        tab_control = ttk.Notebook(root)

        self.clients_tab = ttk.Frame(tab_control)
        self.accounts_tab = ttk.Frame(tab_control)
        self.transactions_tab = ttk.Frame(tab_control)
        self.employees_tab = ttk.Frame(tab_control)
        self.branches_tab = ttk.Frame(tab_control)
        self.loans_tab = ttk.Frame(tab_control)
        self.reports_tab = ttk.Frame(tab_control)

        tab_control.add(self.clients_tab, text='Clients')
        tab_control.add(self.accounts_tab, text='Accounts')
        tab_control.add(self.transactions_tab, text='Transactions')
        tab_control.add(self.employees_tab, text='Employees')
        tab_control.add(self.branches_tab, text='Branches')
        tab_control.add(self.loans_tab, text='Loans')
        tab_control.add(self.reports_tab, text='Reports')

        tab_control.pack(expand=1, fill="both")

        # Initialize forms
        ClientModule(self.clients_tab)
        AccountModule(self.accounts_tab)
        TransactionModule(self.transactions_tab)
        EmployeeModule(self.employees_tab)
        BranchModule(self.branches_tab)
        LoanModule(self.loans_tab)
        ReportModule(self.reports_tab)


if __name__ == "__main__":
    root = tk.Tk()
    app = BankApp(root)
    root.mainloop()
