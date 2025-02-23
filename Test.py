import sqlite3

# Connect to the database
conn = sqlite3.connect('bank.db')
cursor = conn.cursor()

# 1️⃣ Insert Data into Clients Table
cursor.executemany('''
    INSERT INTO Clients (ClientFirstName, ClientLastName, ClientAddress, PhoneNumber, Email, ClientType) 
    VALUES (?, ?, ?, ?, ?, ?)
''', [
    ('John', 'Doe', '123 Main St', '123-456-7890', 'john.doe@email.com', 'Individual'),
    ('Jane', 'Smith', '456 Elm St', '987-654-3210', 'jane.smith@email.com', 'Business'),
    ('Mike', 'Johnson', '789 Pine St', '555-888-9999', 'mike.johnson@email.com', 'Individual')
])

# 2️⃣ Insert Data into Accounts Table
cursor.executemany('''
    INSERT INTO Accounts (ClientID, AccountType, Balance, OpenDate) 
    VALUES (?, ?, ?, ?)
''', [
    (1, 'Savings', 5000.00, '2024-01-10'),
    (2, 'Checking', 1500.00, '2024-01-15'),
    (3, 'Business', 10000.00, '2024-02-01')
])

# 3️⃣ Insert Data into Transactions Table
cursor.executemany('''
    INSERT INTO Transactions (AccountID, Amount, TransactionDate, Type) 
    VALUES (?, ?, ?, ?)
''', [
    (1, 1000.00, '2024-02-05', 'Deposit'),
    (2, -500.00, '2024-02-10', 'Withdrawal'),
    (3, 2000.00, '2024-02-15', 'Transfer')
])

# 4️⃣ Insert Data into Employees Table
cursor.executemany('''
    INSERT INTO Employees (EmployeeFirstName, EmployeeLastName, Position, Department, HireDate) 
    VALUES (?, ?, ?, ?, ?)
''', [
    ('Alice', 'Brown', 'Manager', 'Finance', '2023-06-10'),
    ('Bob', 'Green', 'Teller', 'Customer Service', '2022-09-15'),
    ('Charlie', 'White', 'Loan Officer', 'Loans', '2021-12-20')
])

# 5️⃣ Insert Data into Branches Table
cursor.executemany('''
    INSERT INTO Branches (BranchName, BranchAddress, ManagerID) 
    VALUES (?, ?, ?)
''', [
    ('Downtown Branch', '101 Main St', 1),
    ('Uptown Branch', '202 Elm St', 2),
    ('Westside Branch', '303 Pine St', 3)
])

# 6️⃣ Insert Data into Loans Table
cursor.executemany('''
    INSERT INTO Loans (ClientID, LoanAmount, InterestRate, StartDate, EndDate) 
    VALUES (?, ?, ?, ?, ?)
''', [
    (1, 5000.00, 5.5, '2024-01-20', '2025-01-20'),
    (2, 10000.00, 6.0, '2024-02-15', '2026-02-15'),
    (3, 7500.00, 4.8, '2024-03-10', '2025-03-10')
])

# Commit and close the connection
conn.commit()
conn.close()

print("✅ Sample data inserted successfully into all tables!")
