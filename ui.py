# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 00:04:46 2020

Deals with user interface for the compilation assiter

@author: William
"""
import os
import backend
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

def request_warranty_path(paths):
    path = paths["Data"].joinpath("Mypower Warranty Path.txt")
    if path.exists():
        with open(path, "r") as file:
            paths["Warranty"] = Path(file.read())
    try:
        paths["Warranty"]
    except KeyError:
        paths["Warranty"] = None
    while True:
        if paths["Warranty"] == None:
            path = input("Unable to find the Mypower Installation Warranty. Please input the path to the Mypower Installation Warranty. \"None\" to skip.:\n")
            if path == "None":
                return paths
            else:
                paths["Warranty"] = Path(path)
        if paths["Warranty"].exists():
            break
        else:
            print("\nCouldn't find the given directory path to the Mypower Installation Warranty")
            paths["Warranty"] = None
    with open(path, "w+") as file:
        file.write(str(paths["Warranty"]))
    return paths

def request_solaredge_warranty_path(paths):
    path = paths["Data"].joinpath("SolarEdge Warranty Path.txt")
    if path.exists():
        with open(path, "r") as file:
            paths["SolarEdge Warranty"] = Path(file.read())
    try:
        paths["SolarEdge Warranty"]
    except KeyError:
        paths["SolarEdge Warranty"] = None
    while True:
        if paths["SolarEdge Warranty"] == None:
            path = input("Unable to find the SolarEdge Installation Warranty. Please input the path to the SolarEdge Installation Warranty. \"None\" to skip.:\n")
            if path == "None":
                return paths
            else:
                paths["SolarEdge Warranty"] = Path(path)
        if paths["SolarEdge Warranty"].exists():
            break
        else:
            print("\nCouldn't find the given directory path to the SolarEdge Installation Warranty")
            paths["SolarEdge Warranty"] = None
    with open(path, "w+") as file:
        file.write(str(paths["SolarEdge Warranty"]))
    return paths

def choose_from_file(paths, find, abort=None, abort_msg=None):
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
            if abort_msg:
                print(abort_msg)
            else:
                print()
            return None
        else:
            if not os.path.isdir(lst[choice]):
                os.startfile(str(lst[choice]))
                while True:
                    confirm = input("Confirm Choice (y/n):\n")
                    if confirm == "y":
                        return lst[choice]
                    elif confirm == "n":
                        print("\nReturning to file selection\n")
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
                print("\nCouldn't convert {} to a number. Please input only numbers with \".\" to indicate the decimal place.".format(val))
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

def request_int(request):
    while True:
        val = input("Please input the {}. Enter \"None\" to skip:\n".format(request))
        if val == "None":
            print()
            return None
        else:
            try:
                val = int(val)
            except ValueError:
                print("\nCouldn't convert {} to an integer. Please input an integer".format(val))
                continue
            return val

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
                return None, True
            elif choice == 1:
                print("\nUsing old value for "+name+"\n")
                return old, True
            elif choice == 2:
                print("\nUsing new value for "+name+"\n")
                return new, True
    else:
        return old, False

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
        files = [x for x in path.iterdir() if ".pdf" in x.parts[-1] or os.path.isdir(x)]
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

def define_module(dic, paths):
    while True:
        name = input("What is the name of the new module? Enter \"None\" to cancel and pick an existing module.:\n")
        lower_dic = dict((k.lower(), (k,v)) for k,v in dic.items())
        if name == "None":
            print()
            return dic, None, None
        elif name.lower() in lower_dic:
            while True:
                confirm = input("A module already exists with the name \"{}\". Modify this module? (y/n):\n".format(lower_dic[name.lower()][0]))
                if confirm == "y":
                    mod = lower_dic[name.lower()][1]
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

    path = paths["Tech Area"].joinpath("PV Modules")
    while True:
        files = [x for x in path.iterdir() if ".pdf" in x.parts[-1] or os.path.isdir(x)]
        new_path = choose_from_file(files, "Module's Datasheet", "Move up to parent Directory")
        if new_path == None:
            path = path.parent
        elif ".pdf" in new_path.parts[-1]:
            datasheet = new_path
            break
        else:
            path = new_path

    path = paths["Tech Area"].joinpath("PV Modules")
    while True:
        files = [x for x in path.iterdir() if ".pdf" in x.parts[-1] or os.path.isdir(x)]
        new_path = choose_from_file(files, "Module's Warranty", "Move up to parent Directory")
        if new_path == None:
            path = path.parent
        elif ".pdf" in new_path.parts[-1]:
            warranty = new_path
            break
        else:
            path = new_path

    mod = {"Datasheet":datasheet,
           "Warranty":warranty}
    dic[name] = mod
    return dic, name, mod

def define_optimiser(dic, paths):
    while True:
        name = input("What is the name of the new optimiser? Enter \"None\" to cancel and pick an existing optimiser.:\n")
        lower_dic = dict((k.lower(), (k,v)) for k,v in dic.items())
        if name == "None":
            print()
            return dic, None, None
        elif name.lower() in lower_dic:
            while True:
                confirm = input("An optimiser already exists with the name \"{}\". Modify this optimiser? (y/n):\n".format(lower_dic[name.lower()][0]))
                if confirm == "y":
                    opt = lower_dic[name.lower()][1]
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

    path = paths["Tech Area"].joinpath("Optimisers")
    while True:
        files = [x for x in path.iterdir() if ".pdf" in x.parts[-1] or os.path.isdir(x)]
        new_path = choose_from_file(files, "Optimisers's Datasheet", "Move up to parent Directory")
        if new_path == None:
            path = path.parent
        elif ".pdf" in new_path.parts[-1]:
            datasheet = new_path
            break
        else:
            path = new_path

    opt = {"Datasheet":datasheet}
    dic[name] = opt
    return dic, name, opt

def find_in_folder(paths, request_full, request_short=None, option_for_none=False, n=None, file_types=[".pdf"]):
    if n:
        path = backend.open_folder_n(paths["Customer"], n)
    else:
        path = paths["Customer"]
    if request_short == None:
        request_short = request_full
    while True:
        files = [x for x in path.iterdir() if any(ext in x.parts[-1] for ext in file_types) or os.path.isdir(x)]
        if path == paths["Customer"]:
            new_path = choose_from_file(files, request_full, "{} not present".format(request_short))
        else:
            print("Move up to Customer Directory if {} not present".format(request_short))
            new_path = choose_from_file(files, "{}".format(request_full), "Move up to parent Directory")

        if new_path == None and path == paths["Customer"] and option_for_none:
            while True:
                print("Is the {} required and just not on file at the minute?(y/n):".format(request_short), end="")
                se = input()
                if se == "y":
                    ret = None
                    break
                elif se == "n":
                    ret = True
                    break
                else:
                    print("Please enter \"y\" or \"n\"")
            print()
            break
        elif new_path == None and path == paths["Customer"]:
            ret = None
            break
        elif new_path == None:
            path = path.parent
        elif any(ext in new_path.parts[-1] for ext in file_types):
            ret = new_path
            break
        else:
            path = new_path
    print()
    return ret
