def temperature():
    temp=int(input("Enter temperature : "))
    unit=int(input("1. in celcius \n2. in farenheit \nSelect unit : "))

    match unit:
        case 1 :
            F=(temp * 9/5)+32
            print("Temperature in farenheit is ",F)
        case 2:
            C=(temp - 32)*5/9
            print("Temperature in celcius is ",C)

temperature()
