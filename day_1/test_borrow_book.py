# Imports
from borrow_book import borrow_book

# tests for the borrow_book function
# each test follows the arrange‑act‑assert structure

def test_borrow_available_book():
    # arrange: the requested title is in the list
    available_books = ["Moby Dick", "1984", "Pride and Prejudice"]
    # act: borrow the available book
    result = borrow_book("Moby Dick", available_books)
    # assert: confirm the returned message is correct
    assert result == "Moby Dick has been borrowed."

def test_borrow_unavailable_book():
    # arrange: the requested title is not in the list
    available_books = ["Moby Dick", "1984", "Pride and Prejudice"]
    # act: attempt to borrow a book that isn't available
    result = borrow_book("The Great Gatsby", available_books)
    # assert: the function should report the book is not available
    assert result == "The Great Gatsby is not available."

def test_book_list_updates():
    # arrange: list contains the book to be borrowed
    available_books = ["Moby Dick", "1984", "Pride and Prejudice"]
    # act: borrow the book
    borrow_book("Moby Dick", available_books)
    # assert: the list should no longer contain the borrowed title
    assert "Moby Dick" not in available_books 

def test_borrow_book_empty_list():
    # arrange: there are no books in the inventory
    available_books = []
    # act: try to borrow any title
    result = borrow_book("Moby Dick", available_books)
    # assert: should return a not‑available message
    assert result == "Moby Dick is not available."