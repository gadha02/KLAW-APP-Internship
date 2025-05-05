a= int(input("Enter number 1 : "))
b= int(input("Enter number 2 : "))

while(True):
   op=int(input("1. Addition \n 2. Subtraction \n 3. Multiplication \n 4. Division \n 5.Exit \n Select operation :"))
   match op:
        case 1:
          print("Sum = ", a+b)
        case 2:
          print("Difference = ", a-b)
        case 3:
          print("Product = ", a*b)
        case 4:
          print("Quotient = ", a/b)
        case 5:
          break
    
