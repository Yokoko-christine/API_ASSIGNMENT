# Function Specification: `borrow_book()`

## Purpose
This function lets a user borrow a book from the library if it's available.

---

## Function Signature
```python
borrow_book(book_title, available_books)
```

---

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `book_title` | `string` | The title of the book the user wants to borrow. |
| `available_books` | `list of strings` | A list of book titles currently available in the library. |

---

## Returns

- **If the book is available:**
  - Returns a message: `"You have borrowed '<book_title>'."`
  - Removes the book from `available_books`.

- **If the book is not available:**
  - Returns a message: `"Sorry, '<book_title>' is not available."`

---

## Example Behavior

### ✅ Borrowing an available book
```python
available_books = ["Moby Dick", "1984", "Pride and Prejudice"]

message = borrow_book("1984", available_books)

print(message)          # "You have borrowed '1984'."
print(available_books)  # ["Moby Dick", "Pride and Prejudice"]
```

### ❌ Borrowing an unavailable book
```python
message = borrow_book("The Hobbit", available_books)

print(message)  # "Sorry, 'The Hobbit' is not available."
```

---

## What Students Should Test

1. Borrowing a book that **is** available.
2. Trying to borrow a book that is **not** available.
3. Checking that the book list **updates correctly** after borrowing.
4. Borrowing a book when the list is **empty**.