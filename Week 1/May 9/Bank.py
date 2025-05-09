class BankAccount:
    def __init__(self):
        self.balance = 0

    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited: {amount}")
        print(f"Current balance: {self.balance}")

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            print(f"Withdrawn: {amount}")
            print(f"Current balance: {self.balance}")

        else:
            print("Insufficient balance.")

    def show_balance(self):
        return self.balance
    
s = BankAccount()

while(True):
    print("1. Deposit Amount \n2. Withdraw Amount \n3. Show Balance \n4. Exit")
    op = int(input("Enter your choice: "))

    match op:
        case 1:
            amount=(input("Enter amount to deposit : "))
            s.deposit(int(amount))

        case 2:
            amount=(input("Enter amount to withdraw : "))
            s.withdraw(int(amount))

        case 3:
            print("Current balance : ", s.show_balance())

        case 4:
            break   
       
    