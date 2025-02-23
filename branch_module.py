import sqlite3
from tkinter import ttk, messagebox

class BranchModule:
    def __init__(self, frame):
        self.frame = frame
        self.create_branches_form()

    def create_branches_form(self):
        ttk.Label(self.frame, text="BranchID").grid(row=0, column=0, padx=5, pady=5)
        self.branch_id_entry = ttk.Entry(self.frame)
        self.branch_id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="Branch Name").grid(row=1, column=0, padx=5, pady=5)
        self.branch_name_entry = ttk.Entry(self.frame)
        self.branch_name_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="Branch Address").grid(row=2, column=0, padx=5, pady=5)
        self.branch_address_entry = ttk.Entry(self.frame)
        self.branch_address_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="ManagerID").grid(row=3, column=0, padx=5, pady=5)
        self.branch_manager_id_entry = ttk.Entry(self.frame)
        self.branch_manager_id_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Button(self.frame, text="Save", command=self.save_branch).grid(row=4, column=0, padx=5, pady=5)
        ttk.Button(self.frame, text="Delete", command=self.delete_branch).grid(row=4, column=1, padx=5, pady=5)
        ttk.Button(self.frame, text="Update", command=self.update_branch).grid(row=4, column=2, padx=5, pady=5)
        ttk.Button(self.frame, text="Search", command=self.search_branches).grid(row=4, column=3, padx=5, pady=5)

        self.branches_tree = ttk.Treeview(self.frame, columns=("BranchID", "Branch Name", "Branch Address", "ManagerID"), show="headings")
        self.branches_tree.heading("BranchID", text="BranchID")
        self.branches_tree.heading("Branch Name", text="Branch Name")
        self.branches_tree.heading("Branch Address", text="Branch Address")
        self.branches_tree.heading("ManagerID", text="ManagerID")
        self.branches_tree.grid(row=5, column=0, columnspan=4, padx=5, pady=5)

        self.populate_branches_tree()

    def save_branch(self):
        try:
            conn = sqlite3.connect('bank.db')
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO Branches (BranchName, BranchAddress, ManagerID) VALUES (?, ?, ?)''',
                           (self.branch_name_entry.get(), self.branch_address_entry.get(), self.branch_manager_id_entry.get()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Branch saved successfully.")
            self.populate_branches_tree()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_branch(self):
        try:
            conn = sqlite3.connect('bank.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM Branches WHERE BranchID = ?', (self.branch_id_entry.get(),))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Branch deleted successfully.")
            self.populate_branches_tree()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_branch(self):
        try:
            conn = sqlite3.connect('bank.db')
            cursor = conn.cursor()
            cursor.execute('''UPDATE Branches SET BranchName=?, BranchAddress=?, ManagerID=? WHERE BranchID=?''',
                           (self.branch_name_entry.get(), self.branch_address_entry.get(), self.branch_manager_id_entry.get(), self.branch_id_entry.get()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Branch updated successfully.")
            self.populate_branches_tree()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def search_branches(self):
        try:
            conn = sqlite3.connect('bank.db')
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM Branches WHERE BranchName LIKE ? AND BranchAddress LIKE ?''',
                           (f'%{self.branch_name_entry.get()}%', f'%{self.branch_address_entry.get()}%'))
            rows = cursor.fetchall()
            conn.close()
            self.branches_tree.delete(*self.branches_tree.get_children())
            for row in rows:
                self.branches_tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def populate_branches_tree(self):
        try:
            conn = sqlite3.connect('bank.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Branches')
            rows = cursor.fetchall()
            conn.close()
            self.branches_tree.delete(*self.branches_tree.get_children())
            for row in rows:
                self.branches_tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Error", str(e))
