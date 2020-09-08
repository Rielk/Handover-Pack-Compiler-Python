# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 00:04:46 2020

Deals with user interface for the compilation assiter

@author: William
"""
import os
from pathlib import Path

def request_comm_site_path(comm_path=None):
    """"
    Verifies that the provided path to the Communication site is valid and requests a path is none is given
    Returns a valid path or None is the path is invalid
    """
    if comm_path==None:
        comm_path = Path(input("Unable to find the file directory for the Communication site. Please input the path to the file directory containing the 'Enquiries & Orders' and 'Technical Area' folders:\n"))
    if comm_path.exists():
        if comm_path.joinpath("Enquiries & Orders").exists():
            if comm_path.joinpath("Technical Area").exists():
                return comm_path
            else:
                print("\nCouldn't find 'Technical Area' in given directory")
        else:
            print("\nCouldn't find 'Enquiries & Orders' in given directory")
    else:
        print("\nCouldn't find the given directory path")
    return None

def choose_from_file(paths, find, abort=None, abort_msg=""):
    print("Which file looks like the {}?".format(find))
    lst = [abort]
    lst.extend(paths)
    while True:
        for i, name in enumerate(lst):
            if name == None:
                print(str(i)+". None of these appear to be correct. Continue with missing file.")
            elif name == abort:
                print(str(i)+". "+abort)
            else:
                print(str(i)+". \""+str(name.parts[-1])+"\"")
        try:
            choice = int(input("Which of these files appears to have the correct name:\n"))
        except ValueError:
            print("\nUnrecognised input, please input an integer option from the below list\n")
            continue
        if choice >= len(lst):
            print("\nUnrecognised input, please input an integer option from the below list\n")
            continue
        elif lst[choice] == None:
            print("\nContinuing with missing file\n")
            return None
        elif lst[choice] == abort:
            print(abort_msg)
            return None
        else:
            if lst[choice].with_suffix("") != lst[choice]:
                os.startfile(str(lst[choice]))
                while True:
                    confirm = input("Confirm Choice (y/n):\n")
                    if confirm == "y":
                        return lst[choice]
                    elif confirm == "n":
                        print("Returning to file selection\n")
                        break
                    else:
                        print("Please enter \"y\" or \"n\"")
            else:
                print()
                return lst[choice]
            
def choose_from_list(lst, find):
    print(find)
    while True:
        for i, name in enumerate(lst):
            if name == None:
                print(str(i)+". Cancel")
            else:
                print(str(i)+". \""+str(name)+"\"")
        try:
            choice = int(input("Which of these is correct:\n"))
        except ValueError:
            print("\nUnrecognised input, please input an integer option from the below list\n")
            continue
        if choice >= len(lst):
            print("\nUnrecognised input, please input an integer option from the below list\n")
            continue
        elif lst[choice] == None:
            print("\nContinuing with no choice\n")
            return None
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
      
def define_inverter(dic, paths):
    while True:
        name = input("What is the name of the new inverter? Enter \"None\" to cancel and pick an existing inverter.:\n")
        lower_dic = dict((k.lower(), (k,v)) for k,v in dic.items())
        if name == "None":
            print()
            return dic, None, None
        elif name.lower() in lower_dic:
            while True:
                confirm = input("An inverter already exists with the name \"{}\". Modify this inverter? (y/n):\n".format(lower_dic[name.lower()][0]))
                if confirm == "y":
                    inv = lower_dic[name.lower()][1]
                    if name != lower_dic[name.lower()][0]:
                        while True:
                            change  = input("Change name to \"{}\"? (y/n):\n".format(name))
                            if change == "y":
                                print("\nName changed from \"{}\" to \"{}\".".format(lower_dic[name.lower()][0], name))
                                dic.pop(lower_dic[name.lower()][0], None)
                                break
                            elif change == "n":
                                print("\nUsing name \"{}\".\n".format(lower_dic[name.lower()][0]))
                                name = lower_dic[name.lower()][0]
                                break
                            else:
                                print("\nPlease enter \"y\" or \"n\"")                        
                    break
                elif confirm == "n":
                    name = None
                    break
                else:
                    print("\nPlease enter \"y\" or \"n\"")
        if name != None:
            break

    while True:
        se = input("Is this a Solaredge Inverter? (y/n):\n")
        if se == "y":
            SolarEdge = True
            break
        elif se == "n":
            SolarEdge = False
            break
        else:
            print("\nPlease enter \"y\" or \"n\"")
    print()
    path = paths["Tech Area"].joinpath("Inverters")
    while True:
        files = [x for x in path.iterdir() if ".pdf" in x.parts[-1] or x.with_suffix("") == x]
        new_path = choose_from_file(files, "Inverter's Datasheet", "Move up to parent Directory")
        if new_path == None:
            path = path.parent
        elif ".pdf" in new_path.parts[-1]:
            datasheet = new_path
            break
        else:
            path = new_path
            
    inv = {"Datasheet":datasheet,
           "SolarEdge Warranty":SolarEdge}
    dic[name] = inv
    return dic, name, inv
