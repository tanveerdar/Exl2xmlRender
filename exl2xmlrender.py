from __future__ import print_function
import inputs as ins
import pandas as pd
import os
import jinja2
from jinja2 import Environment, FileSystemLoader


"""
"""


def open_excel_wb(file_name):
    try:
        print ("Opening excel workbook %s" % file_name)
        wbdf = pd.read_excel(file_name, sheet_name= None)
        return wbdf
    except IOError as e:
        print("Can't Open file %s with error %s " % (file_name, e))
    except:
       print("Undefined error opening excel file %s " % file_name)


def bldtask_get(workbook, sheet_name):
    active_sheet = workbook[sheet_name]
    print("+---------- Creating Build tasks ----------+")
    include_rows = active_sheet.loc[active_sheet['Include'].isin(['yes'])]
    inc_rows = include_rows.iloc[0:,1:]
    task_lists = inc_rows.values
    return task_lists

def exl_to_dict(workbook, sheet_name):
    print("+--- Importing worksheet %s" % sheet_name)
    active_sheet = workbook[sheet_name]
    active_dict = {}
    int_dict = active_sheet.to_dict(orient='records')
    active_dict[sheet_name] = int_dict
    return active_dict

def render_template(templ_path,templ_file,item):
    template_loader = FileSystemLoader(templ_path)
    template_env = Environment(loader=template_loader, trim_blocks=True, lstrip_blocks=True)
    try:
        template = template_env.get_template(templ_file)
        xml_payload = template.render(config=item)
        return xml_payload
    except jinja2.TemplateNotFound as e:
        print("Template file %s not found with error %s" % (template, e))
    except jinja2.TemplateSyntaxError as e:
        err_message = "Template %s has syntax error" % template
        err_lineno = str(e.message) + " line number : " + str(e.lineno)
        print(err_message + " " + err_lineno)
    except :
        print("ERROR: Undefined error while rendering template %s" % template)


"""
Generic Constants to be used
"""

template_path = ins.templates
XL_FILE = ins.excel_file
LOGFILE = "xl2acilog.log"
CURDIR = os.getcwd()
PATH = CURDIR + '/testscripts/Pandas'



"""
==================================================
Python Pandas Modules for Excel to XML Rendering
==================================================

"""


"""
Open Excel WorkBook leveraging Pandas
"""
print ('\n')
workbook = open_excel_wb('data.xlsx')
tasks = bldtask_get(workbook,'build_tasks')
print ('\n')


xml_files_list = []
for task in tasks:
    obj_type, worksheet_name, template_file_name = task[:3]
    print("================================================================================")
    print ('Template File name in XML = %s' % template_file_name)
    print ('Worksheet Name = %s' % worksheet_name)
    print ('Object type to be configured = %s' % obj_type)
    print("================================================================================")
    print('\n')
    datadict = exl_to_dict(workbook, worksheet_name)
    #print ('%s (worksheet) ------>to--------> (Dictionary)  %s \n' % (worksheet_name, datadict))
    print("================================================================================")
    print('\n')
    #print (datadict[worksheet_name])
    print("================================================================================")

    try:
        print ("+--- Generating %s Configuration in XML" % obj_type)
        print("================================================================================")
        print('\n')
        for item in datadict[worksheet_name]:
            xml_data = render_template(template_path,template_file_name, item)
            print (xml_data)
    except:
        print("+--- Undefined error quitting further processing ")
