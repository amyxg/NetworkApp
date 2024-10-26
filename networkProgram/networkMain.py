import pandas as pd
import networkFunctions as f
from address_analysis import classful_address_analysis

def main():
    decimal_df = pd.DataFrame()
    binary_df = pd.DataFrame()
    
    while True:
        f.menu()
        userChoice = f.getValidInt("Enter a number from the menu: ", 1, 9)   
        match userChoice:
            case 1: 
                while True:
                    print()
                    decimal_df = pd.concat([decimal_df, f.binToDec()], ignore_index=True)
                    if not f.resetOption():
                        break  
            case 2: 
                while True:
                    print()
                    binary_df = pd.concat([binary_df, f.decToBin()], ignore_index=True)
                    if not f.resetOption():
                        break  
            case 3: 
                print()
                classful_address_analysis()
            case 4: 
                print()
                #print("4 SELECTED")
            case 5: 
                print()
                #print("5 SELECTED")
            case 6: 
                print()
                #print("6 SELECTED")
            case 7: 
                print()
                #print("7 SELECTED")
            case 8: 
                print()
                #print("8 SELECTED")
        if userChoice == 9: 
            print()
            decimal_df.to_csv("decimal_guess.csv", index=False)
            binary_df.to_csv("binary_guess.csv", index=False)
            print("Exiting program..\nGoodbye..")
            break 
                       

if __name__ == "__main__":
    main()