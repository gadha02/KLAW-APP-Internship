import pickle
import os

def new_contact(contacts):
    print("Enter the details \n")
    name = input("Name : ")
    number = input("Phone number : ")
    contacts[name] = number
    print("Contact added successfully")

def load_contacts():
    if os.path.exists("contacts.pkl"):
        with open("contacts.pkl", "rb") as file:
            return pickle.load(file)
    return {}

def save_contacts(contacts):
    with open("contacts.pkl", "wb") as file:
        pickle.dump(contacts, file)

def edit_contact(contacts):
    name = input("Enter contact name: ")
    if name not in contacts:
        print("Contact not found")
        return

    op = int(input(" 1. Edit name \n 2. Edit number \n 3. Edit both name and number \n 4. Cancel \n Choose option : "))
    match op:
        case 1:
            new_name=input("Enter new name : ")
            contacts[new_name] = contacts.pop(name)
            print("Contact edited successfully")

        case 2:
            new_number=int(input("Enter new number : "))
            contacts[name] = new_number
            print("Contact edited successfully")

        case 3: 
            new_name=input("Enter new name : ")
            new_number=int(input("Enter new number : "))
            contacts[new_name] = contacts.pop(name)
            contacts[new_name] = new_number
            print("Contact edited successfully")
            
        case 4:
            return

# Delete a contact
def delete_contact(contacts):
    name = input("Enter contact name: ")
    if name in contacts:
        del contacts[name]
        print("Contact deleted successfully")
    else:
        print("Contact not found")

# Display all contacts
def display(contacts):
    if not contacts:
        print("No contacts to display.")
    else:
        for name, number in contacts.items():
            print(f"{name}: {number}")

# Main menu
def menu():
    contacts = load_contacts()
    while True:
        op = int(input("\n 1. Add contact \n 2. Edit contact \n 3. Delete contact \n 4. Display contacts \n 5. Exit \n Choose option: "))

        match op:
            case 1:
                new_contact(contacts)
            case 2:
                edit_contact(contacts)
            case 3:
                delete_contact(contacts)
            case 4:
                display(contacts)
            case 5:
                save_contacts(contacts)
                print("Contacts saved")
                break

menu()
