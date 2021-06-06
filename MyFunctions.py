# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.11.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# +
from copy import deepcopy

from openpyxl.styles import PatternFill

redFill = PatternFill(start_color='FFFF0000',
                   end_color='FFFF0000',
                   fill_type='solid')
blueFill = PatternFill(start_color='00FFFF',
                   end_color='00FFFF',
                   fill_type='solid')

# +
## Low-level functions ##
"""
Returns string of hh-mm-ss
"""
from time import gmtime, strftime
def getTime():
    return strftime("%H-%M-%S", gmtime())

"""
Splits input string by delimiter
Returns list of these strings 
"""
import re
def split(string):
    return re.split(', |; |\. |  ', string)

"""
Add column with to sheet to max column of sheet
Labels first row with column_header
"""
def add_column(sheet, column_header):
    max_col = sheet.max_column
    sheet.cell(row=1, column=max_col+1).value = column_header

"""
Returns True if statement both
1. Contains word
2. Has a letter immediately before or after
"""
def has_letter_before_or_after(statement, word):
    pattern1 = re.compile(".*\w+{}.*".format(word))
    pattern2 = re.compile(".*{}\w+.*".format(word))
    if pattern1.match(statement) or pattern2.match(statement):
        return True
    return False

"""
Returns True if statement contains any of words in keywords
Else return False
Also handles edge cases of short keywords
"""
def contains(statement, keywords):
    keywords_check_letter_before_or_after = ["id", "ied", "tic", "si", "asd"]

    for word in keywords:
        ## Edge case 1: ensure that there is no letter before or after keyword
        if (word in keywords_check_letter_before_or_after and
            has_letter_before_or_after(statement, word) and
            word in statement):
                return True

        ## Edge case 2: avoid specific psychos psychosomatic mixup
        elif word == "psychos" and word in statement and "psychosomatic" not in statement: 
            return True

        ## Regular word
        elif word in statement:
            return True

    return False

"""
Shortens diagnostic_type
admission => addx
discharge => dcdx
"""
def get_shortened_diagnostic_type(diagnostic_type):
    mapping = {"admission": "addx", "discharge": "dcdx"}
    return mapping[diagnostic_type]

"""
Create a dictionary of column names
"""   
def get_column_names(sheet):
    column_names = {}
    i = 0
    for i, col in enumerate(sheet.iter_cols(1, sheet.max_column)):
        column_names[col[0].value] = i
    return column_names

"""
Handle edge cases of illnesses
Return fixed illnesses list
"""
def manipulate_illness_list(illnesses):
    illnesses = deepcopy(illnesses)

    ## EOS/Personality
    if "Schizophrenia Spectrum and Other Psychotic Disorders" in illnesses and "Personality" in illnesses:
        illnesses.remove("Schizophrenia Spectrum and Other Psychotic Disorders")      
    
    return illnesses

"""
Input list of strings
Split each string and add to list
Return list of all splits
"""
def combine_split_strings(strings):
    actual_strings = [s for s in strings if s is str]

    split_up_strings = []
    for s in actual_strings:
        split_up_strings += split(s.lower())
    return split_up_strings


# -

## Module 5: Read all four info columns, One hot encode symptoms
"""
For each symptom in diagnosis, label the corresponding column with a 1
"""
def ohe_symptoms(sheet, ignore_keywords, symptom_keywords):
    column_names = get_column_names(sheet)
    
    for row_cells in sheet.iter_rows(min_row=2, max_row=sheet.max_row):
        
        ## Get all diagnosis info
        ref_reason = row_cells[column_names['ref_reason']].value
        chief_complaint = row_cells[column_names['chief_complaint']].value
        admission_diagnosis = row_cells[column_names['admission_diagnosis']].value
        discharge_diagnosis = row_cells[column_names['discharge_diagnosis']].value
        
        all_info = []
        all_info.extend((ref_reason, chief_complaint, admission_diagnosis, discharge_diagnosis))
        
        split_all_info = combine_split_strings(all_info)
        
        all_reasons = []
        for info in split_all_info:
            info_reasons = []
            ## add all symptoms associated with each statement
            for symptom in symptom_keywords:
                if not contains(info, ignore_keywords) and contains(info, symptom_keywords[symptom]):
                    info_reasons.append(symptom)
                    row_cells[column_names['{}'.format(symptom)]].value = 1
            all_reasons = all_reasons + info_reasons
