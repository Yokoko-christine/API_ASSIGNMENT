def borrow_book(book_title, available_books):
    # Check if the requested book is in the available books list
    if book_title in available_books:
        # Notify the user that they've successfully borrowed the book
        print(f"You have borrowed '{book_title}'. Enjoy reading!")
        # Remove the book from the available books list
        available_books.remove(book_title)
        # Return confirmation message
        return f"{book_title} has been borrowed."
    else:
        # Return message if the book is not available
        return f"{book_title} is not available."