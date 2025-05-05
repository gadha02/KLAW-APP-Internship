def fibanocci():
    n=int(input("Enter the number of terms : "))
    x,y=1,1
    print("1 \n1")

    for i in range(2,n):
        fib=x+y
        print(fib,"  ")
        x=y
        y=fib
        
fibanocci()
            
