from idlelib.configdialog import is_int

inputIsNumber = False
list1 = [0,1,1]

def fibbonaci(num):
    if num == 1:
        return list1
    else:
        for i in range(2, int(num)):
            nextNum = list1[-1] + list1[-2]
            list1.append(nextNum)
    return list1

while (inputIsNumber == False):
    inputNum = input("Enter a number to generate Fibbonaci series: ")

    if is_int(inputNum):
        fibbonaci(inputNum)
        inputIsNumber = True
    else:
        print("Invalid entry!!")

print (list1)


#from idlelib.configdialog import is_int

#digitNum = False
#factorialNumber = 1

#while(digitNum ==  False):
#   inputNum = input("Enter a number: ")

#   if is_int(inputNum):
#       digitNum = True
#   else:
#       print("Sorry, input a correct value of integer!!")

#if inputNum != 0 and inputNum > 0:
#   for i in range(1, int(inputNum)+1):
#       factorialNumber = factorialNumber*i
#else:
#   print("Requested factorial of negative number!!")

#print(factorialNumber)
