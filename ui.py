# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 00:04:46 2020

Deals with user interface for the compilation assiter

@author: William
"""
import os
def choose_from_file(pdfs, find):
    print("Which file looks like the {}?".format(find))
    lst = [None]
    lst.extend(pdfs)
    while True:
        for i, name in enumerate(lst):
            if name != None:
                print(str(i)+". \""+str(name.parts[-1])+"\"")
            else:
                print(str(i)+". None of these appear to be correct. File is missing.")
        try:
            choice = int(input("Which of these files appears to have the correct name:\n"))
        except ValueError:
            print("\nUnrecognised input, please input an integer option from the below list\n")
            continue
        if choice >= len(lst):
            print("\nUnrecognised input, please input an integer option from the below list\n")
            continue
        elif choice == 0:
            print("\nContinuing with missing file\n")
            return None
        else:
            os.startfile(str(lst[choice]))
            while True:
                confirm = input("Confirm Choice (y/n):\n")
                if confirm == "y":
                    print()
                    return lst[choice]
                elif confirm == "n":
                    print("Returning to file selection\n")
                    break
                else:
                    print("Please enter \"y\" or \"n\"")

def check_conflicting_data(old, new, name):
    if old != new:
        while True:
            print("New value for "+name+" doesn't match existing value for "+name+". Please identify the correct value.")
            print("0. Unknown, ignore for now and come back to it.")
            print("1. {}".format(old))
            print("2. {}".format(new))
            try:
                choice = int(input("Which of these value is correct:\n"))
            except ValueError:
                print("\nUnrecognised input, please input an integer option from the below list\n")
                continue
            if choice >= 3:
                print("\nUnrecognised input, please input an integer option from the below list\n")
                continue
            if choice == 0:
                print("\nContinuing with missing value\n")
                return None
            elif choice == 1:
                print("\nUsing old value for "+name+"\n")
                return old
            elif choice == 2:
                print("\nUsing new value for "+name+"\n")
                return new
    else:
        return old
        
