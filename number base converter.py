# Number base conversion script written by Jasper Law.
# Supports up to 36 symbols (0-9 and A-Z)
# To do: add support for custom symbol sets
# To do: add input validation based on the symbol set


# initial base
base = input("Input your base: ")
# number to convert, in given base
number = input("Input your number: ")
# base to convert to
newBase = input("Input the new base: ")
# convert bases from str to int
base, newBase = int(base), int(newBase)
# strip leading (irrelevant) zeros from initial number
number = number.lstrip("0")
# I am using decimal as my intermediary base. The initial number is converted to this, and then to the target base.
decimalNumber = 0
# The result of the conversion
newNumber = ""
letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


# Convert any integer number from any base into base 10
# Input: number:int, base:int
# Output: decimalNumber:int
def anyToDecimal(number,base):
    # to convert to base 10, we multiply each digit by the initial base, to the power of its position in the number.
    # starting with the largest digit...
    currentExp = len(number)
    decimalNumber = 0
    for i in range(currentExp):
        currentExp -= 1
        # if the digit is a letter, convert it to a number
        if number[i].upper() in letters:
            for n in range(len(letters)):
                if number[i].upper() == letters[n]:
                    # and then add it to the decimal converted result
                    decimalNumber += (n+10) * base ** currentExp
        # If the digit is a number, multiply it by the initial base, to the pwoer of its position in the number
        # and then add that to the deicmal converted result
        else:
            decimalNumber += int(number[i]) * base ** currentExp
    return decimalNumber


# Convert any integer number from base 10 to any base
# Input: decimalNUmber:Int, newBase:Int
# Output: newNumber:string
# String is used in output for two reaons:
# - to seperate each symbol with a space, as the size of each symbol is unknown.
# - to represent more symbols than just numbers (I.e so we can use letters)
def decimalToAny(decimalNumber, newBase):
    if newBase == 1:
        return "1"*decimalNumber
    
    # To store the result of the conversion
    newNumber = ""
    # Find the largest possible base exponent that will fit into our number
    # By incrementing up from 1
    # Very inefficient.
    currentExp = 0
    while newBase ** currentExp <= decimalNumber:
        currentExp += 1
    # Once an exponent has been found that will not fit into our number, step back one.
    currentExp -= 1

    # Convert from the intermedairy base to the target base
    # While there is still number to be converted
    while decimalNumber != 0:
        # To keep track of how many of the current base exponent will fit into the number
        currentExpCount = 0
        # While the base to the power of the current exponent still fits into our number
        while decimalNumber >= newBase ** currentExp:
            # Take it out of the number, and increment the exp counter variable
            currentExpCount += 1
            decimalNumber -= newBase ** currentExp
        # If this exponent was fitted into the number
        if currentExpCount > 0:
            # Add the number times it fitted to the result
            # As a letter, if big enough
            if 10 <= currentExpCount <= (len(letters) + 9):
                newNumber += letters[currentExpCount-10] + " "
            # Or as a number, if small enough/too big
            # May want to change this process for full hex conversion
            else:
                newNumber += str(currentExpCount) + " "
            # newNumber += str(currentExpCount) + " "
        # If this exponent was not fitted into the number
        else:
            # Add a placeholder zero to the result
            newNumber += "0 "
        # Move onto the next largest exponent
        currentExp -= 1

    # If we ran out of number before all possible exponents were tested for fitting
    # We must be missing some placeholder zeros
    # So add the remaining placeholder zeros to the rezult
    while currentExp >= 0:
        newNumber += "0 "
        currentExp -= 1

    return newNumber




# If the number does not need to be converted
if base != newBase:
    # Convert numbers that are not already in the intermediary base to it.
    if base != 10:
        decimalNumber = anyToDecimal(number,base)
        # Print out the result of the intermediary base conversion
        print("Your number in decimal:", decimalNumber)

    # If the input was already in the intermediary base, we don't need to convert it
    else:
        decimalNumber = int(number)

    # If the base to convert to is decimal, we don't need to convert it from the intermediary base
    if newBase == 10:
        newNumber = str(decimalNumber)
    # If the base to convert to differs from the intermediary base
    else:
        newNumber = decimalToAny(decimalNumber, newBase)
        # Print out the result of the conversion
        print("Your number in base",str(newBase) + ":",newNumber)
