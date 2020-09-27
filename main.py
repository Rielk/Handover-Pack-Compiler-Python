# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 16:08:54 2020

Main file for the handover pack compilation assiter

@author: William
"""
from handover_pack import Handover_Pack
import json

hp = Handover_Pack()
if hp.cust_num == "":
    with open(hp.paths["Main"].joinpath("Pending files.txt"), "r") as file:
        try:
            pending = json.load(file)
        except:
            pending = {}
    for num in pending:
        print("Running for pack {}".format(num))
        num = num[:4]
        hp = Handover_Pack(num)
        hp.run()
else:
    hp.run()
