# Library Management System
books = []

while True:
    print("\n=== LIBRARY MANAGEMENT SYSTEM ===")
    print("1. Add book\n2. View books\n3. Search book\n4. Remove book\n5. Exit")
    choice = input("Choose an option: ").strip()

    if choice == "1":
        title = input("Book title: ").strip()
        if title:
            books.append(title)
            print("Book added successfully.")
        else:
            print("Book title cannot be empty.")
    elif choice == "2":
        if not books:
            print("No books available.")
        else:
            for number, title in enumerate(books, 1):
                print(f"{number}. {title}")
    elif choice == "3":
        query = input("Enter title to search: ").strip().lower()
        matches = [title for title in books if query in title.lower()]
        print("\n".join(matches) if matches else "Book not found.")
    elif choice == "4":
        query = input("Enter exact title to remove: ").strip().lower()
        for title in books:
            if title.lower() == query:
                books.remove(title)
                print("Book removed.")
                break
        else:
            print("Book not found.")
    elif choice == "5":
        print("Goodbye!")
        break
    else:
        print("Please choose 1 to 5.")
