
def palindromCheck(inString):
    x = no_spaces_string(inString)
    
    # Reverse the string
    reversed_string = x[::-1]

    if (x == reversed_string):
        return True
    else:
        return False

def no_spaces_string(string1):
    # Remove spaces from the string
    no_space_string = string1.replace(" ", "")
    
    return no_space_string


inputString = input("Input a string: ")

print(palindromCheck(inputString.lower()))