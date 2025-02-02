# Library Management System

This is a **Library Management System** built with **Streamlit** and a **MySQL database**. The system allows users to add books, register borrowers, borrow books, return books, view popular books, and check overdue books.

## Features

1. **Add a New Book**  
   Users can add new books to the system by specifying the title, author, genre, and the number of copies.

2. **Register a Borrower**  
   Register a borrower by adding their name and email address.

3. **Borrow a Book**  
   Borrowers can choose a book from the available list and borrow it. A due date will be assigned.

4. **Return a Book**  
   Users can return books, and the system will update the available copies of that book.

5. **View Most Popular Books**  
   The most popular books are displayed based on the number of times they were borrowed.

6. **View Overdue Books**  
   Displays a list of overdue books along with the borrower information.

## Technologies Used

- **Streamlit**: For building the web interface.
- **MySQL**: For storing and managing data (books, borrowers, transactions).
- **Python**: Backend logic for data handling and connecting to the database.

## How to Run Locally

### Prerequisites

1. Install Python 3.x and the required libraries.
2. Have MySQL installed and running.

### Steps to Set Up

1. Clone this repository:
   ```bash
   git clone https://github.com/mouadsifaw/LibraryDash.git
