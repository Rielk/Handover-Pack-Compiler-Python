# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 17:53:49 2020

Functions to establish directory path names

@author: William
"""
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

def get_paths():
    #Establish Path to files
    main_path = Path.cwd().parent
    data_path = main_path.joinpath("Data")
    if not data_path.exists():
        print("Path to Data directory not found. Assistor has been run from the wrong place. Aborting")
        return None
    
    #Check data for existing, saved path to communication site directory
    path = data_path.joinpath("Communication_Site_Path.txt")
    if path.exists():
        with open(path, "r") as file:
            comm_path = Path(file.read())
    else:
        comm_path = None
    
    #Test path and request a new one until a valid path is provided
    while True:
        comm_path = request_comm_site_path(comm_path)
        if comm_path != None:
            break
    #Save the valid path for future use
    with open(path, "w+") as file:
        file.write(str(comm_path))
    
    EaO_path = comm_path.joinpath("Enquiries & Orders")    
    TA_path = comm_path.joinpath("Technical Area").joinpath("SOLAR PV")
    
    #Identify Customer number for the pack
    while True:
        cust_num = input("Customer Number: ")
        if len(cust_num) < 4:
            print("The Customer number is an integer at least 4 digits long. {} is invalid".format(cust_num))
            continue
        try:
            int(cust_num[:4])
            break
        except ValueError:
            print("The Customer number starts with a 4 digit integer. {} is invalid".format(cust_num[:4]))
    #Find Customer's directory path inside Enquiries and Orders then update EaO_path to that directory
    for path in EaO_path.iterdir():
        if path.parts[-1][0:len(cust_num)] == cust_num:
            EaO_path = path
            abort = False
            break
    else:
        abort = True
        print("Cannot find that customer number '{}' in the Enquiries and Orders directory".format(cust_num))
    
    if not abort:
        #Create the directory for the pack to be created into
        pack_path = main_path.joinpath("Handover Packs").joinpath(EaO_path.parts[-1])
        pack_path.mkdir(parents=True, exist_ok=True)
        
        return {"Main":main_path,
                "Data":data_path,
                "Comm Site":comm_path,
                "Customer":EaO_path,
                "Tech Area":TA_path,
                "Pack":pack_path}
    else:
        return None