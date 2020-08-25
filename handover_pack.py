# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 14:16:28 2020

The Handover Pack class for the compilation assiter

@author: William
"""
import backend
import traceback
import re
from datetime import datetime

class Handover_Pack():
    def __init__(self):
        #Identify Customer number for the pack
        while True:
            self.cust_num = input("Customer Number: ")
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
                break
        self.__init_file_structure__()
        
        #Establish Completed sections dictionary
        self.check_existing()
        self.section_status()
        self.errors = {}
        
    def __init_file_structure__(self):
        self.paths[1] = self.paths["Pack"].joinpath("1.0  Important Technical Information")
        self.paths[1.1] = self.paths[1].joinpath("1.1  Health & Safety Guidelines.pdf")
        self.paths[2] = self.paths["Pack"].joinpath("2.0  General Information")
        self.paths[2.1] = self.paths[2].joinpath("2.1  System Summary & General Information.pdf")
        self.paths[3] = self.paths["Pack"].joinpath("3.0  Guarantees & Datasheets")
        self.paths[3.1] = self.paths[3].joinpath("3.1  Mypower Installation Warranty.pdf")
        self.paths[3.2] = self.paths[3].joinpath("3.2  Module Warranty.pdf")
        self.paths[3.3] = self.paths[3].joinpath("3.3  Module Datasheet.pdf")
        self.paths[3.4] = self.paths[3].joinpath("3.4  Inverter datasheet.pdf")
        self.paths[3.41] = self.paths[3].joinpath("3.4a  Inverter Extended Warranty.pdf")
        self.paths[3.5] = self.paths[3].joinpath("3.5  SolarEdge product warranty.pdf")
        self.paths[3.6] = self.paths[3].joinpath("3.6  SolarEdge Optimiser datasheet.pdf")
        self.paths[4] = self.paths["Pack"].joinpath("4.0  Electrical")
        self.paths[4.1] = self.paths[4].joinpath("4.1  Installation schematic.pdf")
        self.paths[4.2] = self.paths[4].joinpath("4.2  Commissioning test report (AC Cert).pdf")
        self.paths[4.3] = self.paths[4].joinpath("4.3  Commissioning test report (DC Cert).pdf")
        self.paths[4.4] = self.paths[4].joinpath("4.4  DNO commissioning form (G99 Form A3-1).pdf")
        self.paths[4.5] = self.paths[4].joinpath("4.5  Inverter & wiring sign off.pdf")
        self.paths[4.6] = self.paths[4].joinpath("4.6  DNO commissioning notification.pdf")
        self.paths[4.7] = self.paths[4].joinpath("4.7  DNO acceptance.pdf")
        self.paths[5] = self.paths["Pack"].joinpath("5.0  Predicted Output")
        self.paths[5.1] = self.paths[5].joinpath("5.1  Summary Report.pdf")
        self.paths[5.2] = self.paths[5].joinpath("5.2  Predicted Output Comparison Tool.pdf")
        self.paths[6] = self.paths["Pack"].joinpath("6.0  MCS Certificate (if applicable)")
        self.paths[6.1] = self.paths[6].joinpath("6.1  MCS certificate.pdf")
        self.paths[7] = self.paths["Pack"].joinpath("7.0  Building Regulations - Work Notification")
        self.paths[7.1] = self.paths[7].joinpath("7.1  NAPIT Work notification details.pdf")
        self.paths[7.2] = self.paths[7].joinpath("7.2  Structural survey certificate.pdf")
        for i in range(1,8):
            self.paths[i].mkdir(exist_ok=True)
     
    def check_existing(self):
        self.checklist = {1:False, 2:False, 3:False, 4:False, 5:False, 6:False, 7:False,
                          1.1:False, 2.1:False, 3.1:False, 3.2:False, 3.3:False, 3.4:False, 3.41:False,
                          3.5:False, 3.6:False, 4.1:False, 4.2:False, 4.3:False, 4.4:False, 4.5:False,
                          4.6:False, 4.7:False, 5.1:False, 5.2:False, 6.1:False, 7.1:False, 7.2:False}
        for index in self.checklist:
            self.checklist[index] = self.paths[index].exists()
        self.section_status()
     
    def section_status(self):
        itter = {1:[1.1],
                 2:[2.1],
                 3:[3.1, 3.2, 3.3, 3.4, 3.41, 3.5, 3.6],
                 4:[4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7],
                 5:[5.1, 5.2],
                 6:[6.1],
                 7:[7.1, 7.2]}
        for section in itter:
            done = True
            for subsection in itter[section]:
                if not self.checklist[subsection]:
                    done = False
            self.checklist[section] = done
     
    def end_of_run_dump(self):
        dt = datetime.now()
        if self.errors:
            backend.dump_dict(self.paths["Pack"].joinpath("RunErrors, {}.txt".format(dt.strftime("%d %b %y, %H-%M-%S"))), self.errors)
        backend.dump_dict(self.paths["Pack"].joinpath("Checklist, {}.txt".format(dt.strftime("%d %b %y, %H-%M-%S"))), self.checklist)
    
    def run(self):
        for x in range(1, 8):
            if not self.checklist[x]:
                exec("self.section_{}()".format(x))
        self.end_of_run_dump()
    
    def section_1(self):
        try:
            backend.copy_file(self.paths["Data"].joinpath("Health & Safety Guidelines.pdf"), self.paths[1.1], overwrite=True)
            self.checklist[1.1] = True
        except FileNotFoundError:
            print("Couldn't find 'Health & Safety Guidelines.pdf' in the Data path.")
        except:
            self.errors[1.1] = traceback.format_exc()
        self.section_status()
    
    def section_2(self):
        path = self.paths["Customer"].joinpath("1. Quotes info & PV Sol")
        pdfs = [x for x in path.iterdir() if ".pdf" in x.parts[-1]]
        pdfs = [x for x in pdfs if re.search("quote",str(x.parts[-1]),re.IGNORECASE) or re.search("quotation",str(x.parts[-1]),re.IGNORECASE)]
        pdfs = [x for x in pdfs if not re.search("cover",str(x.parts[-1]),re.IGNORECASE)]
        text = backend.pdf_to_str(pdfs[0])
        print(text)
    
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
