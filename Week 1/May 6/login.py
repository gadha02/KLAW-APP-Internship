username_correct="admin"
password_correct="12345678"

def login():
    username=input("Username : ")
    password=input("Password : ")

    if(username == username_correct and password == password_correct):
        print("Login successful")
    elif(username != username_correct and password != password_correct):
        print("Incorrect username and password")
    elif(username != username_correct):
        print("Incorrect username")
    else:
        print("Incorrect password")

login()