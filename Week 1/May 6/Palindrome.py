def palindrome():
    str = input("Enter a string : ")
    if str == str[::-1]:
        print("The string is palindrome ")
    else:
        print("The string is not palindrome")

palindrome()