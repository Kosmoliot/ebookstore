#========Imports========#
# Importing 'tabulate' to dipslay a list of books
# Importing sqlite3 to create and manipulate database
from tabulate import tabulate
import sqlite3


#========Global Variables========#
# Creating 'ebookstore' database under 'db' variable
# Creating a cursor object to execute SQL statements
db = sqlite3.connect('ebookstore')
cursor = db.cursor()


#========Functions========#

# Function to create a table called 'books'
# Using 'IF NOT EXISTS' we check if a 'books' table already exists
# Using 'COUNT(*)' to check if table is empty, and populating it with
# book data
def create_db():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books(id INTEGER PRIMARY KEY, 
        title, author, quantity)
    ''')
    
    # Checking if table is empty
    cursor.execute('''SELECT COUNT(*) FROM books''')
    row_qty = cursor.fetchall()[0][0]

    if row_qty == 0:
        cursor.execute('''INSERT INTO books
            VALUES(3001, 'A Tale of Two Cities', 'Charles Dickens', 30),
            (3002, 'Harry Potter and the Philosophers Stone', 'J.K. Rowling', 40),
            (3003, 'The Lion, the Witch and the Wardrobe', 'C.S. Lewis', 40),
            (3004, 'The Lord of the Rings', 'J.R.R. Tolkien', 37),
            (3005, 'Alice in Wonderland', 'Lewis Caroll', 12);
        ''')


# Function to create a new entry inside 'books' table
# First with 'SELECT MAX(id)' we find the highest id number and increasing it 
# by 1 to use it as a new book's id. Asking user to enter book data and using 
# 'try/except' to check for correct int entry. Checking if title already exists 
# and breaking while loop if it is. Saving changes with db.commit()
def enter_b():
    while True:
        entry_exists = False    # Loop break variable
        max_id = cursor.execute('''SELECT MAX(id) FROM books''')
        new_id = max_id.fetchone()[0] + 1
        new_author = input("Please enter book's author: ")
        new_title = input("Please enter book's title: ")
        
        try:
            new_qty = int(input("Please enter book's quantity: "))
        except ValueError:
            print("Incorrect entry, please try again.")
            break
        
        # Checking if entry already exists
        for row in cursor.execute('''SELECT title FROM books'''):
            if row[0] == new_title:
                entry_exists = True
        
        if entry_exists:
            print("There's already a book with such title, try again.")
            break
        else:
            cursor.execute(f'''INSERT INTO books
                VALUES({new_id}, '{new_title}', '{new_author}', {new_qty});
            ''')
            db.commit()
            break
        

# Function to choose a book from the list of ids that we print using 'view_all'
# function. Using 'try/except' to catch incorrect value error. Return book's id
# if the book is in the database, if not returns None
def choose_b():
    view_all()
    try:
        edit_id = int(input("\nPlese enter book's id: "))
        cursor.execute(f'''SELECT id FROM books WHERE id = {edit_id}''')
        id_check = cursor.fetchone()
        return id_check
    except ValueError:
        print("\nID should be a number.\n")
        

# Function to display book editing menu and request input depending on user's
# choice. Saving changes to database with db.commit()
def edit_opt(book_id):
    while True:
        user_choice = int(input("""\nWhat would you like to update:
1\t-\tTitle
2\t-\tAuthor
3\t-\tQuantity
0\t-\tExit
: """))
        if user_choice == 1:
            new_title = input("Please enter new title: ")
            cursor.execute(f'''UPDATE books SET title = "{new_title}" WHERE id = {book_id}''')
        
        elif user_choice == 2:
            new_auth = input("Please enter new author: ")
            cursor.execute(f'''UPDATE books SET author = "{new_auth}" WHERE id = {book_id}''')

        elif user_choice == 3:
            try:
                new_qty = int(input("Please enter new quantity: "))
                cursor.execute(f'''UPDATE books SET quantity = {new_qty} WHERE id = {book_id}''')
            except ValueError:
                print("Incorrect entry, please try again.")
                break
        
        elif user_choice == 0:
            db.commit()
            break


# Main 'book update' function which calls a function 'choose_b' to choose a 
# book and if id matches one in database calls functtion to edit chosen book.
def update_b():
    id_check = choose_b()
    if id_check != None:
        edit_opt(id_check[0])
    else:
        print("Incorrect entry, please try again.")
        

# Function to delete a book
def delete_b():
    id_check = choose_b()
    if id_check != None:
        cursor.execute(f'''SELECT title FROM books WHERE id = {id_check[0]}''')
        book_title = cursor.fetchone()
        cursor.execute(f'''DELETE FROM books WHERE id = {id_check[0]}''')
        print(f"\nBook called \'{book_title[0]}\' has been deleted.")
    else:
        print("There's no such book, try again.")


# Function to find a book by 'author' or 'title'. Function will print a menu
# for the user to choose search option nad will call 'search_results' func to 
# find all the results and print them using 'print_tabulate' function.
def search_b():
    while True:
        user_choice = int(input("""\nWhat would you like to use for search:
1\t-\tTitle
2\t-\tAuthor
0\t-\tExit
: """))
        if user_choice == 1:
            search_title = input("Please enter a title: ")
            search_results('title', search_title)

        elif user_choice == 2:
            search_auth = input("Please enter an author: ")
            search_results('author', search_auth)
        
        elif user_choice == 0:
            db.commit()
            break


# Function to find results in the table and print them using tabulate.
def search_results(search_option, search_entry):
    print("\nThese are results:\n")
    cursor.execute(f'''SELECT * FROM books WHERE {search_option} = "{search_entry}"''')
    book_results = cursor.fetchall()
    print_table(book_results)
    
    
# Function to print all table content using 'tabulate'
def view_all():
    cursor.execute('''SELECT * FROM books''')
    book_list = cursor.fetchall()
    print_table(book_list)


# Function to use tabulate to print a table that is passed as an argument
def print_table(print_item):
    print(tabulate(
    print_item, headers = ['ID', 'Title', 'Author','Qty'],
    tablefmt = "fancy_grid"))
    

#========Main Menu========#
# Function to display main menu and request user's input and close database if
# user chooses to 'exit'
def main_menu():
    while True:
        try:

            user_choice = int(input("""\nWhat would you like to do:
1\t-\tEnter new book
2\t-\tUpdate book
3\t-\tDelete book
4\t-\tSearch book
5\t-\tView all
0\t-\tExit
: """))
            if user_choice == 1:
                enter_b()
                
            elif user_choice == 2:
                update_b()
                
            elif user_choice == 3:
                delete_b()
                
            elif user_choice == 4:
                search_b()
                
            elif user_choice == 5:
                view_all()                      
            
            elif user_choice == 0:
                db.commit()
                db.close()
                print("\nGoodbye")
                break
            else:
                print("\nOops - incorrect input")
        except ValueError:
            print("\nEntry should be a number from the menu options.\n")

#========Init========#
create_db()
main_menu()