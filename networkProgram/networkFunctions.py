import pandas as pd
import random
import os

def menu():
    """
    Displays main menu for users

    Returns
    -------
    None.
    """
    print()
    print("-----Main Menu-----")
    print("1. Binary to Decimal Conversion")
    print("2. Decimal to Binary Conversion")
    print("3. Classful Address Analysis")
    print("4. Custom Address Map Analysis")
    print("5. Wildcard Mask Determination")
    print("6. Network Address Analysis")
    print("7. Host Address Analysis")
    print("8. Subnetting")
    print("9. Exit\n")

def getValidInt(prompt, minValue, maxValue):
    """
    Check and get int value

    Parameters
    ----------
    prompt : string
        asks users for xyz.
    minValue : int
        minimum value in main menu (1).
    maxValue : int
        minimum value in main menu (9).

    Returns
    -------
    userChoice : int
        value that user inputs for main menu option(s).
    """
    while True:
        try:
            userChoice = int(input(prompt))
            if minValue <= userChoice <= maxValue:
                return userChoice
            else:
                print(f"Please enter a number between {minValue} and {maxValue}.")
        except ValueError:
            print("Invalid input! Please enter a valid integer.")

def displayBitRep(random_binary=None):
    """
    Bit representation showing position values for each bit 

    Parameters
    ----------
    random_binary : string, optional
        DESCRIPTION. The default is None. Later on will have string of bianry value (01010010)

    Returns
    -------
    None.
    """
    print("| Power of 2  | 2^7  | 2^6  | 2^5  | 2^4  | 2^3  | 2^2  | 2^1  | 2^0  |")
    print("-"*70)
    
    print(f"| Decimal     | {128:>4} | {64:>4} | {32:>4} | {16:>4} | {8:>4} | {4:>4} | {2:>4} | {1:>4} |")
    print("| Place Value |      |      |      |      |      |      |      |      |")
    print("-"*70)
    # Shows user the updated table with binary inputs
    if random_binary:
        print(f"| Binary      | {random_binary[0]:>4} | {random_binary[1]:>4} | {random_binary[2]:>4} | {random_binary[3]:>4} | {random_binary[4]:>4} | {random_binary[5]:>4} | {random_binary[6]:>4} | {random_binary[7]:>4} |")
        print("-"*70)

def binToDec():
    """
    Returns
    -------
    decimal_guess : dataframe
        "Random Binary": [random_binary],
        "Random Decimal": [random_decimal],
        "Result": [result]
    """
    # generate a random number between 0 and 255
    random_decimal = random.randint(0, 255)
    # convert random_decimal number to binary 
    random_binary = format(random_decimal, '08b')

    displayBitRep()
    print("What is the Decimal value for the Binary number below.")
    print(random_binary)

    # Ask user to guess the decimal value
    user_guess = int(input("\nEnter a decimal number (e.g., 0-255): "))

    # Evaluate user's guess
    if user_guess == random_decimal:
        print("Well done!")
        print("Your answer is correct.")
        print("See table below\n")
        
        print(f"The binary representation of {random_decimal} is:")
        displayBitRep(random_binary)
        result = "Correct"
    else:
        print("Answer incorrect!") 
        print(f"The correct Decimal value for {random_binary} is {random_decimal}")
        print("See table below\n")
        
        print(f"The binary representation of {random_decimal} is:")
        displayBitRep(random_binary)
        result = "Wrong"

    # Save data to dataframe
    decimal_guess = pd.DataFrame({
        "Random Binary": [random_binary],
        "Random Decimal": [random_decimal],
        "Result": [result]
    })

    return decimal_guess

def decToBin():
    """
    Returns
    -------
    binary_guess : dataframe
        "Random Decimal": [random_decimal],
        "Random Binary": [random_binary],
        "Result": [result]
    """
    displayBitRep()
    # Generate random decimal number
    random_decimal = random.randint(0, 255)
    random_binary = format(random_decimal, '08b')

    print("What is the Binary value for the Decimal number below.")
    print(random_decimal)
    
    # Ask user to guess the binary value
    user_guess = input("Enter the binary value for the decimal number: ")

    # Evaluate user's guess
    if user_guess == random_binary:
        print("Well done!")
        print("Your answer is correct.")
        result = "Correct"
    else:
        print("Answer incorrect!") 
        print(f"The correct Decimal value for {random_decimal} is {random_binary}")
        result = "Wrong"

    # Save data to dataframe
    binary_guess = pd.DataFrame({
        "Random Decimal": [random_decimal],
        "Random Binary": [random_binary],
        "Result": [result]
    })
    return binary_guess

def resetOption():
    """
    reset option for user to redo problem or go back to main menu

    Returns
    -------
    bool
        True if the user wants to reset and generate another problem,
        False if the user wants to go back to the main menu.

    """
    while True:
        resetChoice = input("\n1) Reset (generate another problem)\n2) Back to main menu\nEnter your choice: ")
        if resetChoice == "1":
            return True
        elif resetChoice == "2":
            return False
        else:
            print("Invalid choice. Please try again.")

def classfulAddressAnalysis():
    print("Option 3 selected")
    # display random subnet address
    subnet1 = random.randint(1, 255)
    subnet2 = random.randint(1, 255)
    subnet3 = random.randint(1, 255)
    subnet4 = random.randint(1, 255)
    # randomSubnetAddy = 255.255.255.255
    # list of questions for user onn subnet
    subnetQuestions = ["Enter Address Class and leading Bit Pattern (separate by /):", "What is the prefix Length?", "What is the host address?", "Enter network bits and host bit:"]
    for i in subnetQuestions:
        print(i)