import sqlite3

def create_database():
    # Connect to SQLite database (it will create the file if it doesn't exist)
    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()

    # Create Clients table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Clients (
            ClientID INTEGER PRIMARY KEY AUTOINCREMENT,
            ClientFirstName TEXT NOT NULL,
            ClientLastName TEXT NOT NULL,
            ClientAddress TEXT NOT NULL,
            PhoneNumber TEXT NOT NULL,
            Email TEXT NOT NULL,
            ClientType TEXT NOT NULL
        )
    ''')

    # Create Accounts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Accounts (
            AccountID INTEGER PRIMARY KEY AUTOINCREMENT,
            ClientID INTEGER NOT NULL,
            AccountType TEXT NOT NULL,
            Balance REAL NOT NULL,
            OpenDate DATE NOT NULL,
            FOREIGN KEY (ClientID) REFERENCES Clients(ClientID)
        )
    ''')

    # Create Transactions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Transactions (
            TransactionID INTEGER PRIMARY KEY AUTOINCREMENT,
            AccountID INTEGER NOT NULL,
            Amount REAL NOT NULL,
            TransactionDate DATE NOT NULL,
            Type TEXT NOT NULL,
            FOREIGN KEY (AccountID) REFERENCES Accounts(AccountID)
        )
    ''')

    # Create Employees table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Employees (
            EmployeeID INTEGER PRIMARY KEY AUTOINCREMENT,
            EmployeeFirstName TEXT NOT NULL,
            EmployeeLastName TEXT NOT NULL,
            Position TEXT NOT NULL,
            Department TEXT NOT NULL,
            HireDate DATE NOT NULL
        )
    ''')

    # Create Branches table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Branches (
            BranchID INTEGER PRIMARY KEY AUTOINCREMENT,
            BranchName TEXT NOT NULL,
            BranchAddress TEXT NOT NULL,
            ManagerID INTEGER,
            FOREIGN KEY (ManagerID) REFERENCES Employees(EmployeeID)
        )
    ''')

    # Create Loans table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Loans (
            LoanID INTEGER PRIMARY KEY AUTOINCREMENT,
            ClientID INTEGER NOT NULL,
            LoanAmount REAL NOT NULL,
            InterestRate REAL NOT NULL,
            StartDate DATE NOT NULL,
            EndDate DATE NOT NULL,
            FOREIGN KEY (ClientID) REFERENCES Clients(ClientID)
        )
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Call the function to create the database and tables
create_database()
