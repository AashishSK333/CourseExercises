from idlelib.configdialog import is_int

inputArthemeticOperation = False
list1 = ["+", "-", "*", "/"]

def requestNumber(inputOperation):
    firstNumber = input("Enter First Number : " )
    secondNumber = input ("Enter Second Number: ")

    if is_int(firstNumber) and is_int(secondNumber):
        if inputOperation == "+":
            return firstNumber + secondNumber
        elif inputOperation == "-":
            return firstNumber - secondNumber
        elif inputOperation == "*":
            return firstNumber * secondNumber
        elif inputOperation == "/":
            return firstNumber/secondNumber
    else:
        print("Invalid input")

while (inputArthemeticOperation == False):

    inputOperation = input("Enter the arithmetic operation that you want to perform : ")

    if inputOperation in list1:
        inputOperation = True        
    else:
        print("Invalid entry!!")
        break

output = requestNumber(inputOperation)

print("Calculation on input number is: ")