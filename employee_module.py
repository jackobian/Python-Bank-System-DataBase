import sqlite3
from tkinter import ttk, messagebox

class EmployeeModule:
    def __init__(self, frame):
        self.frame = frame
        self.create_employees_form()

    def create_employees_form(self):
        ttk.Label(self.frame, text="EmployeeID").grid(row=0, column=0, padx=5, pady=5)
        self.employee_id_entry = ttk.Entry(self.frame)
        self.employee_id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="First Name").grid(row=1, column=0, padx=5, pady=5)
        self.employee_first_name_entry = ttk.Entry(self.frame)
        self.employee_first_name_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="Last Name").grid(row=2, column=0, padx=5, pady=5)
        self.employee_last_name_entry = ttk.Entry(self.frame)
        self.employee_last_name_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="Position").grid(row=3, column=0, padx=5, pady=5)
        self.employee_position_entry = ttk.Entry(self.frame)
        self.employee_position_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="Department").grid(row=4, column=0, padx=5, pady=5)
        self.employee_department_entry = ttk.Entry(self.frame)
        self.employee_department_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="Hire Date").grid(row=5, column=0, padx=5, pady=5)
        self.employee_hire_date_entry = ttk.Entry(self.frame)
        self.employee_hire_date_entry.grid(row=5, column=1, padx=5, pady=5)

        ttk.Button(self.frame, text="Save", command=self.save_employee).grid(row=6, column=0, padx=5, pady=5)
        ttk.Button(self.frame, text="Delete", command=self.delete_employee).grid(row=6, column=1, padx=5, pady=5)
        ttk.Button(self.frame, text="Update", command=self.update_employee).grid(row=6, column=2, padx=5, pady=5)
        ttk.Button(self.frame, text="Search", command=self.search_employees).grid(row=6, column=3, padx=5, pady=5)

        self.employees_tree = ttk.Treeview(self.frame, columns=("EmployeeID", "First Name", "Last Name", "Position", "Department", "Hire Date"), show="headings")
        self.employees_tree.heading("EmployeeID", text="EmployeeID")
        self.employees_tree.heading("First Name", text="First Name")
        self.employees_tree.heading("Last Name", text="Last Name")
        self.employees_tree.heading("Position", text="Position")
        self.employees_tree.heading("Department", text="Department")
        self.employees_tree.heading("Hire Date", text="Hire Date")
        self.employees_tree.grid(row=7, column=0, columnspan=4, padx=5, pady=5)

        self.populate_employees_tree()

    def save_employee(self):
        try:
            conn = sqlite3.connect('bank.db')
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO Employees (EmployeeFirstName, EmployeeLastName, Position, Department, HireDate)
                              VALUES (?, ?, ?, ?, ?)''',
                           (self.employee_first_name_entry.get(), self.employee_last_name_entry.get(),
                            self.employee_position_entry.get(), self.employee_department_entry.get(),
                            self.employee_hire_date_entry.get()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Employee saved successfully.")
            self.populate_employees_tree()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_employee(self):
        try:
            conn = sqlite3.connect('bank.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM Employees WHERE EmployeeID = ?', (self.employee_id_entry.get(),))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Employee deleted successfully.")
            self.populate_employees_tree()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_employee(self):
        try:
            conn = sqlite3.connect('bank.db')
            cursor = conn.cursor()
            cursor.execute('''UPDATE Employees SET EmployeeFirstName=?, EmployeeLastName=?, Position=?, Department=?, HireDate=?
                              WHERE EmployeeID=?''',
                           (self.employee_first_name_entry.get(), self.employee_last_name_entry.get(),
                            self.employee_position_entry.get(), self.employee_department_entry.get(),
                            self.employee_hire_date_entry.get(), self.employee_id_entry.get()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Employee updated successfully.")
            self.populate_employees_tree()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def search_employees(self):
        try:
            conn = sqlite3.connect('bank.db')
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM Employees WHERE EmployeeFirstName LIKE ? AND EmployeeLastName LIKE ?''',
                           (f'%{self.employee_first_name_entry.get()}%', f'%{self.employee_last_name_entry.get()}%'))
            rows = cursor.fetchall()
            conn.close()
            self.employees_tree.delete(*self.employees_tree.get_children())
            for row in rows:
                self.employees_tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def populate_employees_tree(self):
        try:
            conn = sqlite3.connect('bank.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Employees')
            rows = cursor.fetchall()
            conn.close()
            self.employees_tree.delete(*self.employees_tree.get_children())
            for row in rows:
                self.employees_tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Error", str(e))
