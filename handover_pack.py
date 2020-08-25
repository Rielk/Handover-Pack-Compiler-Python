# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 14:16:28 2020

The Handover Pack class for the compilation assiter

@author: William
"""
from backend import get_paths

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
            self.paths = get_paths(self.cust_num)
            if self.paths != None:
                break
            
