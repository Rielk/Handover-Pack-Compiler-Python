# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 13:06:00 2020

The pdf finding algorithms for the compilation assiter

@author: William
"""
import re
import ui
import os
import json
import backend
import datetime
from pathlib import Path

def Quotation(paths, cust_num):
    try:
        paths["Quotation"]
    except KeyError:
        paths["Quotation"] = None
    if paths["Quotation"] == None:
        path = backend.open_folder_n(paths["Customer"], 1)
        pdfs = [x for x in path.iterdir() if ".pdf" in x.parts[-1]]
        pdfs = [x for x in pdfs if re.search("quote",str(x.parts[-1]),re.IGNORECASE) or re.search("quotation",str(x.parts[-1]),re.IGNORECASE)]
        pdfs = [x for x in pdfs if not re.search("cover",str(x.parts[-1]),re.IGNORECASE)]
        quote_pdf = ui.choose_from_file(pdfs, "Quotation")
        if quote_pdf:
            text = backend.pdf_to_str(quote_pdf)
            cust_num, _ = ui.check_conflicting_data(cust_num, backend.find_in_str("Quotation Reference", text[0], "\n"), "Customer Number")
        if cust_num == None or quote_pdf == None:
            print("Confusion on Quotation file, continuing without it\n")
            paths["Quotation"] = False
        else:
            paths["Quotation"] = quote_pdf
    else:
        quote_pdf = paths["Quotation"]
    return paths, cust_num, quote_pdf

def Final_Schematic(paths, cust_num):
    try:
        paths["Final Schematic"]
    except KeyError:
        paths["Final Schematic"] = None
    if paths["Final Schematic"] == None:
        path = backend.open_folder_n(paths["Customer"], 6).joinpath("Final Schematic for build")
        pdfs = [x for x in path.iterdir() if ".pdf" in x.parts[-1]]
        schem_pdf = ui.choose_from_file(pdfs, "Final Schematic")
        if schem_pdf:
            text = backend.pdf_to_str(schem_pdf)
            cust_num, _ = ui.check_conflicting_data(cust_num, backend.find_in_str("Reference:", text[0], "-"), "Customer Number")
        if cust_num == None or schem_pdf == None:
            print("Confusion on Final Schematic file, continuing without it\n")
            paths["Final Schematic"] = False
        else:
            paths["Final Schematic"] = schem_pdf
    else:
        schem_pdf = paths["Final Schematic"]
    return paths, cust_num, schem_pdf

def Install_Date(paths, values):
    try:
        values["Install Date"]
    except KeyError:
        values["Install Date"] = None
    if values["Install Date"] == None:
        os.startfile(str(backend.open_folder_n(paths["Customer"], 2).joinpath("Install Photos")))
        while True:
            inp = re.split("\D+", input("Find the Install Date in Photos(day/month/year). Enter \"None\" to skip:\n"))
            if inp == "None":
                print("Continuing without an Install Date")
                values["Install Date"] == False
                print()
                return values
            else:
                date_str = inp
                if len(date_str) != 3:
                    print("Input has the wrong number of integers to format to a date. Please input all values in numerical format (eg. 21/1/20 or 4.12.2019)")
                    continue
                else:
                    if len(date_str[2]) != 4:
                        date_str[2] = str(datetime.date.today().year)[0:2]+date_str[2]
                    try:
                        date = datetime.date(int(date_str[2]),int(date_str[1]),int(date_str[0]))
                    except ValueError:
                        print("Couldn't format \"{}\" into a date. Please input all values in numerical format (eg. 21/1/20 or 4.12.2019)".format(inp))
                        continue
                    while True:
                        confirm = input("Confirm Date ({}) (y/n):".format(date.strftime("%d %b %Y")))
                        if confirm == "y":
                            print()
                            values["Install Date"] = date.strftime("%d/%m/%Y")
                            return values
                        elif confirm == "n":
                            break
                        else:
                            print("Please enter \"y\" or \"n\"")
    else:
        return values

def Serial_Numbers(paths, values):
    try:
        values["Serial Numbers"]
    except KeyError:
        values["Serial Numbers"] = None
    if values["Serial Numbers"] == None:
        os.startfile(str(backend.open_folder_n(paths["Customer"], 2).joinpath("Install Photos")))
        lst = []
        while True:
            while True:
                print("Current Serial Numbers: {}".format(lst))
                inp = input("Find the Serial Numbers for the inverters from Photos(enter one at a time). Enter \"None\" to skip this step. Enter \"Done\" to finish. Enter \"Clear\" to clear all Serial Numbers and restart:\n").strip(" ")
                if inp == "None":
                    if len(lst) == 0:
                        print("\nContinuing without Serial Numbers")
                        values["Serial Numbers"] == False
                        print()
                        return values
                    else:
                        print("\nUse \"Clear\" to reset Serial Numbers before continuing with \"None\"\n")
                elif inp == "Done":
                    if len(lst) == 0:
                        print("\nNo Serial Numbers entered. To continue without Serial Numbers, enter \"None\".\n")
                        continue
                    else:
                        print()
                        break
                elif inp == "Clear":
                    print("\nClearing all Serial Numbers, restarting with none.\n")
                    lst = []
                else:
                    print()
                    lst.append(inp)
            while True:
                print("There is/are {} Serial Number(s):".format(len(lst)))
                for l in lst:
                    print(l)
                confirm = input("Confirm Serial Numbers (y/n):")
                if confirm == "y":
                    print()
                    values["Serial Numbers"] = lst
                    return values
                elif confirm == "n":
                    print()
                    break
                else:
                    print("Please enter \"y\" or \"n\"")
    else:
        return values

def Inverter_Information(paths, values):
    try:
        values["Inverters"]
    except KeyError:
        values["Inverters"] = None
    try:
        values["SolarEdge Warranty"]
    except KeyError:
        values["SolarEdge Warranty"] = None
    try:
        paths["Inverter Datasheets"]
    except KeyError:
        paths["Inverter Datasheets"] = None

    if paths["Data"].joinpath("Inverter Types.txt").exists():
        with open(paths["Data"].joinpath("Inverter Types.txt"), "r") as file:
            temp_dict = json.load(file)
        inv_types = {}
        for key in temp_dict:
            dic = {"Datasheet":Path(temp_dict[key]["Datasheet"]),
                    "SolarEdge Warranty":temp_dict[key]["SolarEdge Warranty"]}
            inv_types[key] = dic
    else:
        inv_types = {}

    current_inv_list = []
    start = True
    while True:
        if values["Inverters"] == None:
            if start:
                start = False
                os.startfile(str(paths["Quotation"]))
                try:
                    os.startfile(str(paths["Final Schematic"]))
                except KeyError:
                    pass
            while True:
                lst = ["Add/Modify Existing Inverter"]
                if current_inv_list:
                    lst.append("Cancel")
                else:
                    lst.append("Unknown, leave missing")
                lst.extend([x for x in inv_types])
                if current_inv_list:
                    print("Current Inverters: {}".format([name for name,_ in current_inv_list]))
                name = ui.choose_from_list(lst, "Choose an inverter from ths list:")
                if name == "Add/Modify Existing Inverter":
                    inv_types, name, inv = ui.define_inverter(inv_types, paths)
                    if inv != None:
                        break
                elif name == "Unknown, leave missing" or name == "Cancel":
                    print()
                    name = False
                    inv = False
                    break
                else:
                    inv = inv_types[name]
                    break
        else:
            current_inv_list = []
            for name in values["Inverters"]:
                try:
                    current_inv_list.append((name,inv_types[name]))
                except KeyError:
                    lowered_inv_types = dict((k.lower(), (k,v)) for k,v in inv_types.items())
                    if name.lower() in lowered_inv_types:
                        current_inv_list.append(lowered_inv_types[name.lower()])
                    else:
                        print("Unknown Inverter stored in \"Pack Values\". Re-enter Inverter Information.")
                        values["Inverters"] = None
                        return Inverter_Information(paths, values)
            name = False

        while True:
            if name:
                another = input("Add another inverter? (y/n):\n")
                if another == "y":
                    print()
                    break
                elif another == "n":
                    print()
                    break
                else:
                    print("Please enter \"y\" or \"n\"")
            else:
                another = None
                break
        if another != None:
            current_inv_list.append((name,inv))
        if another == "n":
            break
        if another == None:
            break

    if current_inv_list:
        values["Inverters"] = [name for name,_ in current_inv_list]
        if sum([inv["SolarEdge Warranty"] for _,inv in current_inv_list]):
            values["SolarEdge Warranty"] = True
        else:
            values["SolarEdge Warranty"] = False
        paths["Inverter Datasheets"] = [inv["Datasheet"] for _,inv in current_inv_list]
    else:
        values["Inverters"] = False
        values["SolarEdge Warranty"] = None
        paths["Inverter Datasheets"] = None

    temp_dict = {}
    for key in inv_types:
        dic = {"Datasheet":str(inv_types[key]["Datasheet"]),
                "SolarEdge Warranty":inv_types[key]["SolarEdge Warranty"]}
        temp_dict[key] = dic
    with open(paths["Data"].joinpath("Inverter Types.txt"), "w") as file:
        json.dump(temp_dict, file, indent=3, sort_keys=True)
    return paths, values

def Module_Information(paths, values):
    try:
        values["Module"]
        paths["Module Warranty"]
        paths["Module Datasheet"]
    except KeyError:
        values["Module"] = None
        paths["Module Warranty"] = None
        paths["Module Datasheet"] = None

    if values["Module"] == None:
        pass

    return paths, values
