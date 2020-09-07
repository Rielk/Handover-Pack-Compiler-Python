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

def make_choice(choices, find):
    print(find)
    lst = [None]
    lst.extend(choices)
    while True:
        for i, name in enumerate(lst):
            if name != None:
                print(str(i)+". "+ name)
            else:
                print(str(i)+". Cancel")
        try:
            choice = int(input("Which of these choices is correct:\n"))
        except ValueError:
            print("\nUnrecognised input, please input an integer option from the below list\n")
            continue
        if choice >= len(lst):
            print("\nUnrecognised input, please input an integer option from the below list\n")
            continue
        elif choice == 0:
            print("\nContinuing without choice\n")
            return False
        else:
            return lst[choice]

def request_float(request):
    while True:
        val = input("Please input the {}. Enter \"None\" to skip:\n".format(request))
        if val == "None":
            print()
            return None
        else:
            try:
                val = float(val)
            except ValueError:
                print("\nCouldn't convert {} to a number. Please input only numbers with \".\" to indicate the decimal place.")
                continue
            while True:
                confirm = input("Confirm input ({}) (y/n):".format(val))
                if confirm == "y":
                    print()
                    return val
                elif confirm == "n":
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
      
def define_inverter(dic):
    while True:
        name = input("What is the name of the new component? Enter \"None\" to cancel and pick an existing component.:\n")
        if name == "None":
            return dic, None
        elif name in dic:
            while True:
                confirm = input("A component already exists with that name. Modify this component? (y/n):")
                if confirm == "y":
                    break
                elif confirm == "n":
                    name = None
                    break
                else:
                    print("Please enter \"y\" or \"n\"")
            if name != None:
                break
    
