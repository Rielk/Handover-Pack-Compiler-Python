# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 17:53:49 2020

Backend functions for the Handover Pack class and compilation assiter

@author: William
"""
from pathlib import Path
import pdfplumber
import shutil
import json
import re
import ui

def get_paths(cust_num):
    #Establish Path to files
    main_path = Path.cwd().parent
    data_path = main_path.joinpath("Data")
    if not data_path.exists():
        print("Path to Data directory not found. Assistor has been run from the wrong place. Aborting")
        return None
    
    #Check data for existing, saved path to communication site directory
    path = data_path.joinpath("Communication Site Path.txt")
    if path.exists():
        with open(path, "r") as file:
            comm_path = Path(file.read())
    else:
        comm_path = None
    
    #Test path and request a new one until a valid path is provided
    while True:
        comm_path = ui.request_comm_site_path(comm_path)
        if comm_path != None:
            break
    #Save the valid path for future use
    with open(path, "w+") as file:
        file.write(str(comm_path))
    
    EaO_path = comm_path.joinpath("Enquiries & Orders")    
    TA_path = comm_path.joinpath("Technical Area").joinpath("SOLAR PV")
    
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
        
        if pack_path.joinpath("File Paths.txt").exists():
            with open(pack_path.joinpath("File Paths.txt"), "r") as file:
                path_dict = json.load(file)
            ret = {}
            for key in path_dict:
                if path_dict[key] == None:
                    val = None
                else:
                    val = Path(path_dict[key])
                    if not val.exists():
                        continue
                ret[key] = val
            return ret
        
        return {"Main":main_path,
                "Data":data_path,
                "Comm Site":comm_path,
                "Customer":EaO_path,
                "Tech Area":TA_path,
                "Pack":pack_path}
    else:
        return None

def dump_dict(path, dic):
    with open(path, "w") as file:
        first = None
        for index in dic:
            if not first==str(index)[0] and first!=None:
                file.write("\n")
            file.write(str(index)+":"+str(dic[index])+"\n")
            first = str(index)[0]

def pdf_to_str(path):
    with pdfplumber.open(path) as pdf:
        page_list = pdf.pages
        text = [page.extract_text(x_tolerance=3, y_tolerance=3) for page in page_list]
    return text

def find_in_str(find, string, n):
    search = re.search(find, string, re.IGNORECASE)
    if search and type(n)==int:
        ret = string[search.end():search.end()+n].strip(" ")
    elif search and type(n)==str:
        ret = string[search.end():search.end()+re.search(n, string[search.end():], re.IGNORECASE).end()-len(n)].strip(" ")
    elif search:
        raise TypeError("n must be an integer number of digits or a string to search up to")
    else:
        ret = None
    return ret

def copy_file(from_path, to_path, overwrite=False):
    if not to_path.exists() or overwrite:
        shutil.copyfile(str(from_path), str(to_path))
        return True
    else: return False
    
def open_folder_n(path, n):
    for folder in path.iterdir():
        if folder.parts[-1].startswith("{}.".format(n)):
            return folder
    
def archive(path, paths):
    i = 0
    name = paths["Archive"].joinpath(path.parts[-1])
    while name.exists():
        i+=1
        name = paths["Archive"].joinpath(path.with_suffix("").parts[-1]+"("+str(i)+")"+path.suffix)
    shutil.move(path, name)
    