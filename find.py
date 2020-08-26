# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 13:06:00 2020

The pdf finding algorithms for the compilation assiter

@author: William
"""
import re
import ui
import backend

def Quotation(paths, cust_num):
    try:
        paths["Quotation"]
    except KeyError:
        paths["Quotation"] = None
    if paths["Quotation"] == None:
        path = paths["Customer"].joinpath("1. Quotes info & PV Sol")
        pdfs = [x for x in path.iterdir() if ".pdf" in x.parts[-1]]
        pdfs = [x for x in pdfs if re.search("quote",str(x.parts[-1]),re.IGNORECASE) or re.search("quotation",str(x.parts[-1]),re.IGNORECASE)]
        pdfs = [x for x in pdfs if not re.search("cover",str(x.parts[-1]),re.IGNORECASE)]
        quote_pdf = ui.choose_from_file(pdfs, "Quotation")
        if quote_pdf:
            text = backend.pdf_to_str(quote_pdf)
            cust_num = ui.check_conflicting_data(cust_num, backend.find_in_str("Quotation Reference", text[0], "\n"), "Customer Number")
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
        path = paths["Customer"].joinpath("6. DNO & Power").joinpath("Final Schematic for build")
        pdfs = [x for x in path.iterdir() if ".pdf" in x.parts[-1]]
        schem_pdf = ui.choose_from_file(pdfs, "Final Schematic")
        if schem_pdf:
            text = backend.pdf_to_str(schem_pdf)
            cust_num = ui.check_conflicting_data(cust_num, backend.find_in_str("Reference:", text[0], "-"), "Customer Number")
        if cust_num == None or schem_pdf == None:
            print("Confusion on Final Schematic file, continuing without it\n")
            paths["Final Schematic"] = False
        else:
            paths["Final Schematic"] = schem_pdf
    else:
        schem_pdf = paths["Final Schematic"]
    return paths, cust_num, schem_pdf
