contacts = {}

def add_contact():
    name = input("Name: ").strip()
    phone = input("Phone: ").strip()
    email = input("Email: ").strip()
    if not name:
        print("Name cannot be empty.")
        return
    contacts[name.lower()] = {"name": name, "phone": phone, "email": email}
    print("Contact saved.")

def view_contacts():
    if not contacts:
        print("No contacts saved.")
        return
    for contact in contacts.values():
        print(f'{contact["name"]} | Phone: {contact["phone"]} | Email: {contact["email"]}')

def search_contact():
    name = input("Name to search: ").strip().lower()
    contact = contacts.get(name)
    print(contact if contact else "Contact not found.")

def delete_contact():
    name = input("Name to delete: ").strip().lower()
    if contacts.pop(name, None):
        print("Contact deleted.")
    else:
        print("Contact not found.")

while True:
    print("\\n--- Contact Book ---")
    print("1. Add  2. View all  3. Search  4. Delete  5. Exit")
    choice = input("Choose: ").strip()
    if choice == "1": add_contact()
    elif choice == "2": view_contacts()
    elif choice == "3": search_contact()
    elif choice == "4": delete_contact()
    elif choice == "5": break
    else: print("Invalid choice.")
