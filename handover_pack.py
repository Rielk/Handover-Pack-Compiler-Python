# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 14:16:28 2020

The Handover Pack class for the compilation assiter

@author: William
"""
import backend
import traceback
import find
import json
from docx import Document
from datetime import datetime

class Handover_Pack():
    def __init__(self):
        #Identify Customer number for the pack
        while True:
            self.cust_num = input("Customer Number: ").strip(" ")
            if len(self.cust_num) < 4:
                print("The Customer number starts with a 4 digits integer. {} is invalid".format(self.cust_num))
                continue
            try:
                int(self.cust_num[:4])
            except ValueError:
                print("The Customer number starts with a 4 digit integer. {} is invalid".format(self.cust_num[:4]))
                continue
            self.paths = backend.get_paths(self.cust_num)
            if self.paths != None:
                print()
                break
        self.__init_file_structure__()
        self.__init_values__()
        
        #Establish Completed sections dictionary
        self.check_existing()
        self.section_status()
        self.errors = {}
        
    def __init_values__(self):
        if self.paths["Pack"].joinpath("Pack Values.txt").exists():
            with open(self.paths["Pack"].joinpath("Pack Values.txt"), "r") as file:
                path_dict = json.load(file)
            self.values = path_dict
        else:
            self.values = {"Business Name":None,
                           "Address":None,
                           "System Size":None,
                           "Predicted Output":None,
                           "Install Date":None,
                           "Serial Numbers":None}
        
    def __init_file_structure__(self):
        self.structure = {1:[1.1],
                          2:[2.1],
                          3:[3.1, 3.2, 3.3, 3.4, 3.41, 3.5, 3.6],
                          4:[4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7],
                          5:[5.1, 5.2],
                          6:[6.1],
                          7:[7.1, 7.2]}
        with open(self.paths["Data"].joinpath("Folder Structure.txt"), "r") as file:
            temp_dict = json.load(file)
        for i in self.structure:
            key = str(i)
            try:
                self.paths[key]
            except:
                self.paths[key] = self.paths["Pack"].joinpath(temp_dict[key])
            self.paths[key].mkdir(exist_ok=True)
            for j in self.structure[i]:
                key2 = str(j)
                try:
                    self.paths[key2]
                except:
                    self.paths[key2] = self.paths[key].joinpath(temp_dict[key2])
                self.paths[key].mkdir(exist_ok=True)
        self.paths["Checklists"] = self.paths["Pack"].joinpath("Checklists")
        self.paths["RunErrors"] = self.paths["Pack"].joinpath("RunErrors")
        self.paths["Archive"] = self.paths["Pack"].joinpath("Archive")
        self.paths["Checklists"].mkdir(exist_ok=True)
        self.paths["RunErrors"].mkdir(exist_ok=True)
        self.paths["Archive"].mkdir(exist_ok=True)
     
    def check_existing(self):
        self.checklist = {1:False, 2:False, 3:False, 4:False, 5:False, 6:False, 7:False,
                          1.1:False, 2.1:False, 3.1:False, 3.2:False, 3.3:False, 3.4:False, 3.41:False,
                          3.5:False, 3.6:False, 4.1:False, 4.2:False, 4.3:False, 4.4:False, 4.5:False,
                          4.6:False, 4.7:False, 5.1:False, 5.2:False, 6.1:False, 7.1:False, 7.2:False}
        for index in self.checklist:
            self.checklist[index] = self.paths[str(index)].exists()
        self.section_status()
     
    def section_status(self):
        for section in self.structure:
            done = True
            for subsection in self.structure[section]:
                if not self.checklist[subsection]:
                    done = False
            self.checklist[section] = done
     
    def end_of_run_dump(self):
        dt = datetime.now()
        if self.errors:
            backend.dump_dict(self.paths["RunErrors"].joinpath("RunErrors, {}.txt".format(dt.strftime("%d %b %y, %H-%M-%S"))), self.errors)
        backend.dump_dict(self.paths["Checklists"].joinpath("Checklist, {}.txt".format(dt.strftime("%d %b %y, %H-%M-%S"))), self.checklist)
        path_dict = {}
        for key in self.paths:
            if self.paths[key] == None or self.paths[key] == False:
                val = None
            else:
                val = str(self.paths[key])
            path_dict[key] = val
        with open(self.paths["Pack"].joinpath("File Paths.txt"), "w") as file:
            json.dump(path_dict, file, indent=3, separators=(',\n', ': '), sort_keys=True)
        with open(self.paths["Pack"].joinpath("Pack Values.txt"), "w") as file:
            json.dump(self.values, file, indent=3, sort_keys=True)
    
    def run(self):
        for x in range(1, 8):
            if not self.checklist[x]:
                exec("self.section_{}()".format(x))
        self.end_of_run_dump()
    
    def section_1(self):
        try:
            if not self.checklist[1.1]:
                try:
                    backend.copy_file(self.paths["Data"].joinpath("Health & Safety Guidelines.pdf"), self.paths["1.1"], overwrite=True)
                    self.checklist[1.1] = True
                except FileNotFoundError:
                    print("Couldn't find 'Health & Safety Guidelines.pdf' in the Data path.\n")
        except:
            print("Error caught in completion of section 1. See RunErrors for details.\n")
            self.errors[1.1] = traceback.format_exc()
        self.section_status()
    
    def section_2(self):
        try:
            self.paths, self.cust_num, quote_pdf = find.Quotation(self.paths, self.cust_num)
            if not quote_pdf:
                print("Missing the Quotation pdf, cannot complete section 2.")
                return None
            self.paths, self.cust_num, schem_pdf = find.Final_Schematic(self.paths, self.cust_num)
            if not schem_pdf:
                print("Missing the Final Schematic pdf, cannot complete section 2.")
                return None
            
            if not self.checklist[2.1]:
                self.paths, self.values["Install Date"] = find.Install_Date(self.paths)
                self.paths, self.values["Serial Numbers"] = find.Serial_Numbers(self.paths)
                
                quote_text = backend.pdf_to_str(quote_pdf)
                if not self.values["Business Name"]:
                    self.values["Business Name"] = backend.find_in_str("Business name", quote_text[0], "\n")
                if not self.values["Address"]:
                    self.values["Address"] = self.values["Business Name"].strip(".")+", "+backend.find_in_str("Address", quote_text[0], "\n")
                if not self.values["System Size"]:
                    self.values["System Size"] = float(backend.find_in_str("System Size:", quote_text[1], "kWp\n"))
                if not self.values["Predicted Output"]:
                    self.values["Predicted Output"] = float(backend.find_in_str("estimated generation:", quote_text[1], "kWh\n").replace(",",""))
                try:
                    path = self.paths["2"].joinpath("2.1  System Summary & General Information.docx")
                    backend.copy_file(self.paths["Data"].joinpath("Information Template.docx"), path, overwrite=True)
                    document = Document(path) 
                    document.paragraphs[4].runs[0].text = "{:.2f} kWp".format(self.values["System Size"])
                    document.tables[1].rows[1].cells[1].paragraphs[0].runs[0].text = "{:.2f}".format(self.values["System Size"])
                    document.tables[1].rows[2].cells[1].paragraphs[0].runs[0].text = "{:,.0f} kW".format(self.values["Predicted Output"])
                    
                    #Format Address in Box
                    lst = self.values["Address"].split(",")
                    text = []
                    lines = 0
                    for i in range(0, len(lst), 2): 
                        lines += 1
                        text.append(lst[i]+","+lst[i+1]+",\n")
                    lst = text
                    text = lst[0]
                    for st in lst[1:]:
                        text += st
                    text = text.strip(",\n")
                    document.tables[0].rows[1].cells[0].paragraphs[3].runs[0].text = text
                    for i in range(lines-1):
                        p = document.tables[0].rows[1].cells[0].paragraphs[4]._element
                        p.getparent().remove(p)
                        p._p = p._element = None                    
                    document.tables[0].rows[1].cells[0].paragraphs[8-lines].runs[0].text = "Job ref: "+self.cust_num
                    #End of Address formatting
                    
                    document.save(path)
                    backend.archive(path, self.paths)
                except FileNotFoundError:
                    print("Couldn't find 'Information Template.docx' in the Data path.\nSkipping Section 2\n")
                    return None
        except:
            print("Error caught in completion of section 2. See RunErrors for details.\n")
            self.errors[2.1] = traceback.format_exc()
        self.section_status()
        
    
    def section_3(self):
        pass
    
    def section_4(self):
        pass
    
    def section_5(self):
        pass
    
    def section_6(self):
        pass
    
    def section_7(self):
        pass
