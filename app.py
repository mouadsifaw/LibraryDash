import streamlit as st
import mysql.connector
import pandas as pd
from datetime import datetime, timedelta

# Database connection
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Mouad@1412',
    'database': 'LibraryDB'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

st.title("📖 Library Management System")

# 📚 **1. Add a New Book**
st.subheader("➕ Add a New Book")
title = st.text_input("Book Title")
author = st.text_input("Author")
genre = st.text_input("Genre")
copies = st.number_input("Number of Copies", min_value=1, value=1)

if st.button("Add Book"):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Books (Title, Author, Genre, AvailableCopies) VALUES (%s, %s, %s, %s)",
                   (title, author, genre, copies))
    conn.commit()
    conn.close()
    st.success(f"✅ '{title}' added successfully!")

# 👤 **2. Add a Borrower**
st.subheader("🆕 Register a Borrower")
borrower_name = st.text_input("Borrower Name")
borrower_email = st.text_input("Email")

if st.button("Register Borrower"):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Borrowers (Name, Email) VALUES (%s, %s)", (borrower_name, borrower_email))
    conn.commit()
    conn.close()
    st.success(f"✅ Borrower '{borrower_name}' registered!")

# 📖 **3. Borrow a Book**
st.subheader("📙 Borrow a Book")
conn = get_db_connection()
books = pd.read_sql("SELECT BookID, Title FROM Books WHERE AvailableCopies > 0", conn)
borrowers = pd.read_sql("SELECT BorrowerID, Name FROM Borrowers", conn)
conn.close()

book_options = {row["Title"]: row["BookID"] for _, row in books.iterrows()}
borrower_options = {row["Name"]: row["BorrowerID"] for _, row in borrowers.iterrows()}

book_choice = st.selectbox("Select a Book", list(book_options.keys()))
borrower_choice = st.selectbox("Select a Borrower", list(borrower_options.keys()))
due_date = st.date_input("Due Date", min_value=datetime.today() + timedelta(days=7))

if st.button("Borrow Book"):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(""" 
        INSERT INTO Transactions (BookID, BorrowerID, DueDate) 
        VALUES (%s, %s, %s)""", 
        (book_options[book_choice], borrower_options[borrower_choice], due_date))
    cursor.execute("UPDATE Books SET AvailableCopies = AvailableCopies - 1 WHERE BookID = %s", 
                   (book_options[book_choice],))
    conn.commit()
    conn.close()
    st.success(f"✅ '{book_choice}' borrowed by {borrower_choice} until {due_date}!")

# 📜 **4. Return a Book**
st.subheader("🔄 Return a Book")
conn = get_db_connection()
borrowed_books = pd.read_sql(""" 
    SELECT T.TransactionID, B.Title, Br.Name
    FROM Transactions T
    JOIN Books B ON T.BookID = B.BookID
    JOIN Borrowers Br ON T.BorrowerID = Br.BorrowerID
    WHERE T.ReturnDate IS NULL 
""", conn)
conn.close()

return_options = {f"{row['Title']} (Borrowed by {row['Name']})": row["TransactionID"] for _, row in borrowed_books.iterrows()}
return_choice = st.selectbox("Select a Book to Return", list(return_options.keys()))

if st.button("Return Book"):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Transactions SET ReturnDate = CURDATE() WHERE TransactionID = %s", (return_options[return_choice],))
    cursor.execute(""" 
        UPDATE Books 
        SET AvailableCopies = AvailableCopies + 1 
        WHERE BookID = (SELECT BookID FROM Transactions WHERE TransactionID = %s)
    """, (return_options[return_choice],))
    conn.commit()
    conn.close()
    st.success(f"✅ {return_choice} returned successfully!")

# 📊 **5. View Popular Books**
st.subheader("📈 Most Popular Books")
conn = get_db_connection()
df1 = pd.read_sql("""
    SELECT B.Title, COUNT(T.TransactionID) AS TimesBorrowed
    FROM Transactions T
    JOIN Books B ON T.BookID = B.BookID
    GROUP BY B.Title
    ORDER BY TimesBorrowed DESC
""", conn)
conn.close()

st.bar_chart(df1.set_index("Title"))

# 🕒 **6. View Overdue Books with Fine Calculation**
st.subheader("⚠️ Overdue Books and Fines")
conn = get_db_connection()
df2 = pd.read_sql("""
    SELECT 
        B.Title, 
        Br.Name AS BorrowerName, 
        DATEDIFF(CURDATE(), T.DueDate) AS DaysOverdue,
        DATEDIFF(CURDATE(), T.DueDate) * 1 AS FineAmount  -- Assuming $1 fine per day
    FROM Transactions T
    JOIN Books B ON T.BookID = B.BookID
    JOIN Borrowers Br ON T.BorrowerID = Br.BorrowerID
    WHERE T.ReturnDate IS NULL AND T.DueDate < CURDATE()
""", conn)
conn.close()

st.write("These books are overdue, and fines are calculated based on the number of days overdue (assuming $1/day).")
st.table(df2)
