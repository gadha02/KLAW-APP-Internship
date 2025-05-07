input=input("Enter the input : ")

with open("input.txt","w") as file:
    file.write(input)

file = open("input.txt", "r")
print (file.read())
file.close()
