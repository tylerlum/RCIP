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

import pandas as pd
import numpy as np

from MyFunctions import *

## Import data
filename = "NEW_INPUT.xlsx"
data_df = pd.read_excel(filename, sheet_name="ResearchInChildAndAd_DATA_2018-", engine='openpyxl')
illness_df = pd.read_excel(filename, sheet_name="Illness Keywords", engine='openpyxl')
mrr_df = pd.read_excel(filename, sheet_name="MRR Keywords", engine='openpyxl')
# symptoms_df = pd.read_excel(filename, sheet_name="Symptoms", engine='openpyxl')

# +
def is_nan(val):
    return not (val == val)

def convert_to_dict_of_lists_no_nans(df):
    dict_of_lists = df.to_dict(orient='list')
    
    # Remove nans
    for key in dict_of_lists.keys():
        list_ = dict_of_lists[key]
        dict_of_lists[key] = [x for x in list_ if not is_nan(x)]
    return dict_of_lists


# +
## Setup keywords
IGNORE_KEYWORDS = ['query', 'vs', 'r/o', 'rule out', 'versus']

ILLNESS_TO_KEYWORDS = convert_to_dict_of_lists_no_nans(illness_df)
ILLNESSES = list(ILLNESS_TO_KEYWORDS.keys())

REASON_FOR_REFERRAL_TO_KEYWORDS = convert_to_dict_of_lists_no_nans(mrr_df)
REASONS_FOR_REFERRAL = list(REASON_FOR_REFERRAL_TO_KEYWORDS.keys())

# SYMPTOM_KEYWORDS = convert_to_dict_of_lists_no_nans(symptoms_df)
# SYMPTOMS = list(SYMPTOM_KEYWORDS.keys())
# -

## Setup important words
DIAGNOSTIC_TYPES = ['admission', 'discharge']
SHORT_DIAGNOSTIC_TYPES = ['addx', 'dcdx']

# +
## Module 1: Add columns headers and set binary values to 0

# Non-binary column headers
for dt in SHORT_DIAGNOSTIC_TYPES:
    data_df[f"main_{dt}"] = ""

# Binary column headers
illness_headers = [f"{dt}_{illness}" for dt in SHORT_DIAGNOSTIC_TYPES for illness in ILLNESSES]
mrr_headers = [f"mrr_{reason}" for reason in REASONS_FOR_REFERRAL]
# symptom_headers = [f"{symptom}" for symptom in SYMPTOMS]
binary_column_headers = illness_headers + mrr_headers  # + symptom_headers
    
for column_header in binary_column_headers:
    data_df[column_header] = 0
# -

## Module 2: Fill in main diagnosis
for full_dt, dt in zip(DIAGNOSTIC_TYPES, SHORT_DIAGNOSTIC_TYPES):
    for i, row in data_df.iterrows():
        diagnosis_str = row[f'{full_dt}_diagnosis']

        # Skip nans
        if is_nan(diagnosis_str):
            continue

        # Get main diagnosis by iterating through diagnosis_list until we get a valid diagnosis
        diagnosis_list = split(diagnosis_str.lower())
        all_illnesses = []
        for diagnosis in diagnosis_list:
            # Get illnesses
            illnesses = [illness for illness in ILLNESSES
                         if not contains(diagnosis, IGNORE_KEYWORDS) and
                         contains(diagnosis, ILLNESS_TO_KEYWORDS[illness])]
            
            illnesses = manipulate_illness_list(illnesses)  # Handle edge cases
            
            # Should only be 1 illness, but put in list otherwise
            # Break after first one is found, as this is only looking for the main diagnosis
            if len(illnesses) == 1:
                data_df.at[i, f'main_{dt}'] = illnesses[0]
                break
            elif len(illnesses) >= 1:
                data_df.at[i, f'main_{dt}'] = str(illnesses)
                break
            
            # If none found, look at the next diagnosis
            else:  # len(illnesses) == 0
                continue

## Module 3: Read diagnoses, one hot encode symptoms
for full_dt, dt in zip(DIAGNOSTIC_TYPES, SHORT_DIAGNOSTIC_TYPES):
    for i, row in data_df.iterrows():
        diagnosis_str = row[f'{full_dt}_diagnosis']

        # Skip nans
        if is_nan(diagnosis_str):
            continue

        # Get main diagnosis by iterating through diagnosis_list until we get a valid diagnosis
        diagnosis_list = split(diagnosis_str.lower())
        for diagnosis in diagnosis_list:
            # Get illnesses
            illnesses = [illness for illness in ILLNESSES
                         if not contains(diagnosis, IGNORE_KEYWORDS) and
                         contains(diagnosis, ILLNESS_TO_KEYWORDS[illness])]

            illnesses = manipulate_illness_list(illnesses)  # Handle edge cases

            # Populate the binary illness values in the df
            for illness in illnesses:
                data_df.at[i, f'{dt}_{illness}'] = 1

## Module 4: Read ref_reason + chief_complaint, one hot encode symptoms
for i, row in data_df.iterrows():
    str1 = row['ref_reason']
    str2 = row['chief_complaint']

    # Skip nans
    if is_nan(str1) and is_nan(str2):
        continue
    elif is_nan(str1):
        ref_reason_str = str2
    elif is_nan(str2):
        ref_reason_str = str1
    else:
        ref_reason_str = f"{str1}, {str2}"

    # Get main diagnosis by iterating through diagnosis_list until we get a valid diagnosis
    ref_reason_list = split(ref_reason_str.lower())
    ref_reasons = []
    for ref_reason in ref_reason_list:
        # Get illnesses
        ref_reasons = [r for r in REASONS_FOR_REFERRAL
                       if not contains(ref_reason, IGNORE_KEYWORDS) and
                       contains(ref_reason, REASON_FOR_REFERRAL_TO_KEYWORDS[r])]
        
        # Populate the binary illness values in the df
        for rr in ref_reasons:
            data_df.at[i, f'mrr_{rr}'] = 1
            
        # Populate Other if no other reason is given
        if len(ref_reasons) == 0:
            data_df.at[i, 'mrr_Other'] = 1

# +
## Module 5: Read all four info columns, one hot encode symptoms
# ohe_symptoms(data_sheet, IGNORE_KEYWORDS, SYMPTOM_KEYWORDS)

for i, row in data_df.iterrows():
    ref_reason_str = row['ref_reason'].lower()
    chief_complaint_str = row['chief_complaint'].lower()
    admission_diagnosis_str = row['admission_diagnosis'].lower()
    discharge_diagnosis_str = row['discharge_diagnosis'].lower()
    
    all_statements = (split(ref_reason_str) + split(chief_complaint_str) +
                      split(admission_diagnosis_str) + split(discharge_diagnosis_str))
    
    for statement is all_statements:
        symptoms = [s for s in SYMPTOMS
                    if not contains(statement, IGNORE_KEYWORDS) and
                    contains(statement, SYMPTOM_TO_KEYWORDS[s])]
        
        for s in symptoms:
            data_df.at[i, str(s)] = 1
# -

## Output file
workbook.save("output-{}.xlsx".format(getTime()))


