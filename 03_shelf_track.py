'''
PART1
import sqlite3
create a datevase table called ebookstore and a table called book with the following columns: id(primary key), title, authorID, qty
create a menu that allows the user to do the following:
1. Enter book
2. Update book
3. Delete book
4. Search book
5. Exit
create a function for each of the menu options that performs the corresponding database operations. Use parameterized queries to prevent SQL injection. Make sure to handle exceptions and close the database connection properly.
PART2
create another table called author with the following columns: id(primary key), name, country
add a foreign key constraint to the book table that references the authorID column in the author table
update the menu to allow the user to do the following:
5. view details of all books
add function for view details of all books. use the zip() function to display the book details along with the corresponding author details. Make sure to handle exceptions and close the database connection properly.
'''

import sqlite3 #importing the sqlite3 module to work with SQLite databases

DATABASE_NAME = 'ebookstore.db'   #name of the database file
initial_books = [
    (3001, "A Tale of Two Cities", 1290, 30),
    (3002, "Harry Potter and the Sorcerer's Stone", 8937, 40),
    (3003, "The Lion, the Witch and the Wardrobe", 2356, 25),
    (3004, "The Lord of the Rings", 6380, 37),
    (3005, "Alice in Wonderland", 5620, 12) #initial book data to populate the book table
]

authors = [
    (1290, "Charles Dickens", "England"),
    (8937, "J.K. Rowling", "England"),
    (2356, "C.S. Lewis", "Ireland"),
    (6380, "J.R.R. Tolkien", "South Africa"),
    (5620, "Lewis Carroll", "England") #initial author data to populate the author table
]

# Create the ebookstore database and book table
def create_book_table():
    conn = sqlite3.connect('ebookstore.db')
    try:
        c = conn.cursor()
        c.execute('''
        CREATE TABLE IF NOT EXISTS book (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            authorID INTEGER,
            qty INTEGER,
            FOREIGN KEY (authorID) REFERENCES author(id)
        )
    ''')
        c.executemany( 
            """
            INSERT OR IGNORE INTO book (id, title, authorID, qty)
            VALUES (?, ?, ?, ?)
            """,
            initial_books, #usuing executemany to insert multiple rows of initial book data into the book table
        )
        conn.commit()
    finally:
        conn.close()

# Create the author table
def create_author_table():
    conn = sqlite3.connect('ebookstore.db')
    try:
        c = conn.cursor()
        c.execute('''
        CREATE TABLE IF NOT EXISTS author (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            country TEXT NOT NULL
        )
    ''')
        c.executemany(
            """
            INSERT OR IGNORE INTO author (id, name, country)
            VALUES (?, ?, ?)
            """,
            authors,
        )
        conn.commit() #adding the author data to the author table
    finally:
        conn.close()

#createing functions for menu options
def enter_book():
    conn = sqlite3.connect('ebookstore.db')
    c = conn.cursor() #c is the cursor object used to execute SQL commands and interact with the database
    
    title = input("Enter book title: ")
    authorID = int(input("Enter author ID: "))
    qty = int(input("Enter quantity: "))
    
    try:
        c.execute('INSERT INTO book (title, authorID, qty) VALUES (?, ?, ?)', (title, authorID, qty))
        conn.commit()
        print("Book entered successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

def update_book():
    conn = sqlite3.connect('ebookstore.db')
    c = conn.cursor()
    
    book_id = int(input("Enter book ID to update: "))
    new_title = input("Enter new title: ")
    new_authorID = int(input("Enter new author ID: "))
    new_qty = int(input("Enter new quantity: "))
    author_name = input("Enter new author name: ")
    author_country = input("Enter new author country: ") #had to add author name and country input here to make sure the author details are saved even if this author id is new.
    
    try:
        c.execute(
            'UPDATE book SET title = ?, authorID = ?, qty = ? WHERE id = ?',
            (new_title, new_authorID, new_qty, book_id)
        )

        #make sure the author details are saved even if this author id is new.
        c.execute(
            '''
            INSERT INTO author (id, name, country)
            VALUES (?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET 
                name = excluded.name,
                country = excluded.country
            ''',
            (new_authorID, author_name, author_country) #on conflict of author id, update the name and country to the new values provided by the user. This ensures that if the user updates a book with a new author id, the corresponding author details are also updated in the author table. had issue with this at first when running the program.
        )
        conn.commit()
        print("Book updated successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

def delete_book():
    conn = sqlite3.connect('ebookstore.db')
    c = conn.cursor()
    
    book_id = int(input("Enter book ID to delete: "))
    
    try:
        c.execute('DELETE FROM book WHERE id = ?', (book_id,))
        conn.commit()
        print("Book deleted successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

def search_book():
    conn = sqlite3.connect('ebookstore.db')
    c = conn.cursor()
    
    search_title = input("Enter book title to search: ")
    
    try:
        c.execute('SELECT * FROM book WHERE title LIKE ?', ('%' + search_title + '%',)) #using a parameterized query with a wildcard to search for books that contain the search term in their title. This allows for partial matches and is more flexible than an exact match. Helps woith error handling as well since it won't throw an error if the user enters a search term that doesn't match any book titles
        results = c.fetchall()
        for row in results:
            print(row)
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

def view_all_books():
    conn = sqlite3.connect('ebookstore.db')
    c = conn.cursor()

    try:
        c.execute('SELECT id, title, authorID, qty FROM book ORDER BY id')
        books = c.fetchall()

        if not books:
            print("No books found.")
            return

        #build matching author details list in the same order as books
        author_details = []
        for _, _, author_id, _ in books:
            c.execute('SELECT name, country FROM author WHERE id = ?', (author_id,))
            author_row = c.fetchone()
            if author_row is None:
                author_row = ("Unknown author", "Unknown country")
            author_details.append(author_row)

        #zip() pairs each book row with its matching author row
        for (book_id, title, author_id, qty), (author_name, country) in zip(books, author_details):
            print(
                f"Title: {title}\n"
                f"Author: {author_name}\n"
                f"Country: {country}\n" #using zip to display the book details along with the corresponding author details in a formatted way. Each book's title, author name, and country are printed together for better readability.
            ) #using this instead of inner join to practice using zip() as requested in the prompt. An inner join would have been more efficient for this task, but I wanted to follow the instructions and use zip() to pair the book details with the author details after fetching them separately from the database.
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

def exit():
    print("Exiting the program.")
    quit()

#making the main menu
def main_menu():
    while True:
        print("\nMenu:")
        print("1. Enter book")
        print("2. Update book")
        print("3. Delete book")
        print("4. Search book")
        print("5. View all books") #added option for viewing all books with author details
        print("0. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            enter_book()
        elif choice == '2':
            update_book()
        elif choice == '3':
            delete_book()
        elif choice == '4':
            search_book()
        elif choice == '5':
            view_all_books()
        elif choice == '0':
            exit()
        else:
            print("Invalid choice. Please try again.")
if __name__ == "__main__": #insure that the database tables are created and the main menu is displayed when the script is run directly
    create_book_table()
    create_author_table() #added the author table 
    main_menu()
