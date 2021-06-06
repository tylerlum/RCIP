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

from utilities import (is_nan, convert_to_dict_of_lists_no_nans, get_time, split, 
                       has_letter_before_or_after, contains, manipulate_illness_list)

## Import data
filename = "NEW_INPUT.xlsx"
DATA_DF = pd.read_excel(filename, sheet_name="ResearchInChildAndAd_DATA_2018-", engine='openpyxl')
ILLNESS_DF = pd.read_excel(filename, sheet_name="Illness Keywords", engine='openpyxl')
MRR_DF = pd.read_excel(filename, sheet_name="MRR Keywords", engine='openpyxl')
# SYMPTOMS_DF = pd.read_excel(filename, sheet_name="Symptoms", engine='openpyxl')

# +
## Setup keywords
IGNORE_KEYWORDS = ['query', 'vs', 'r/o', 'rule out', 'versus']

ILLNESS_TO_KEYWORDS = convert_to_dict_of_lists_no_nans(ILLNESS_DF)
ILLNESSES = list(ILLNESS_TO_KEYWORDS.keys())

REASON_FOR_REFERRAL_TO_KEYWORDS = convert_to_dict_of_lists_no_nans(MRR_DF)
REASONS_FOR_REFERRAL = list(REASON_FOR_REFERRAL_TO_KEYWORDS.keys())

# SYMPTOM_KEYWORDS = convert_to_dict_of_lists_no_nans(SYMPTOMS_DF)
# SYMPTOMS = list(SYMPTOM_KEYWORDS.keys())
# -

## Setup important words
FULL_DIAGNOSTIC_TYPES = ['admission', 'discharge']
DIAGNOSTIC_TYPES = ['addx', 'dcdx']

# +
## Module 1: Add columns headers and set binary values to 0

# Non-binary column headers
for dt in DIAGNOSTIC_TYPES:
    DATA_DF[f"main_{dt}"] = ""

# Binary column headers
illness_headers = [f"{dt}_{illness}" for dt in DIAGNOSTIC_TYPES for illness in ILLNESSES]
mrr_headers = [f"mrr_{reason}" for reason in REASONS_FOR_REFERRAL]
# symptom_headers = [f"{symptom}" for symptom in SYMPTOMS]
binary_column_headers = illness_headers + mrr_headers  # + symptom_headers

for column_header in binary_column_headers:
    DATA_DF[column_header] = 0
# -

## Module 2: Fill in main diagnosis
for full_dt, dt in zip(FULL_DIAGNOSTIC_TYPES, DIAGNOSTIC_TYPES):
    for i, row in DATA_DF.iterrows():
        diagnosis_statement_str = row[f'{full_dt}_diagnosis']

        # Skip nans
        if is_nan(diagnosis_statement_str):
            continue

        # Get main diagnosis by iterating through diagnosis_statements until we get a valid statement
        diagnosis_statements = split(diagnosis_statement_str.lower())
        all_illnesses = []
        for diagnosis_statement in diagnosis_statements:
            # Skip statements with IGNORE_KEYWORDS
            if contains(diagnosis_statement, IGNORE_KEYWORDS):
                continue

            # Get illnesses
            illnesses = [illness for illness, keywords in ILLNESS_TO_KEYWORDS.items()
                         if contains(diagnosis_statement, keywords)]
            illnesses = manipulate_illness_list(illnesses)  # Handle edge cases

            # Should only be 1 illness, but put in list otherwise
            # Break after first one is found, as we are only looking for the main diagnosis
            if len(illnesses) == 1:
                DATA_DF.at[i, f'main_{dt}'] = illnesses[0]
                break
            elif len(illnesses) >= 1:
                DATA_DF.at[i, f'main_{dt}'] = str(illnesses)
                break
            # If none found, look at the next diagnosis
            else:  # len(illnesses) == 0
                continue

## Module 3: Read diagnoses, one hot encode illnesses
for full_dt, dt in zip(FULL_DIAGNOSTIC_TYPES, DIAGNOSTIC_TYPES):
    for i, row in DATA_DF.iterrows():
        diagnosis_statement_str = row[f'{full_dt}_diagnosis']

        # Skip nans
        if is_nan(diagnosis_statement_str):
            continue

        # Get illnesses by iterating through diagnosis_statements
        diagnosis_statements = split(diagnosis_statement_str.lower())
        for diagnosis_statement in diagnosis_statements:
            # Skip statements with IGNORE_KEYWORDS
            if contains(diagnosis_statement, IGNORE_KEYWORDS):
                continue

            # Get illnesses
            illnesses = [illness for illness, keywords in ILLNESS_TO_KEYWORDS.items()
                         if contains(diagnosis_statement, keywords)]
            illnesses = manipulate_illness_list(illnesses)  # Handle edge cases

            # Populate the binary illness values in the df
            for illness in illnesses:
                DATA_DF.at[i, f'{dt}_{illness}'] = 1

## Module 4: Read ref_reason + chief_complaint, one hot encode mrr
for i, row in DATA_DF.iterrows():
    str1 = row['ref_reason']
    str2 = row['chief_complaint']

    # Skip nans
    if is_nan(str1) and is_nan(str2):
        continue
    elif is_nan(str1):
        ref_reason_statement_str = str2
    elif is_nan(str2):
        ref_reason_statement_str = str1
    else:
        ref_reason_statement_str = f"{str1}, {str2}"

    # Get ref_reasons by iterating through ref_reason_statements
    ref_reason_statements = split(ref_reason_statement_str.lower())
    for ref_reason_statement in ref_reason_statements:
        # Skip statements with IGNORE_KEYWORDS
        if contains(ref_reason_statement, IGNORE_KEYWORDS):
            continue

        # Get ref_reasons
        ref_reasons = [rr for rr, keywords in REASON_FOR_REFERRAL_TO_KEYWORDS.items()
                       if contains(ref_reason_statement, keywords)]

        # Populate the binary illness values in the df
        for rr in ref_reasons:
            DATA_DF.at[i, f'mrr_{rr}'] = 1

        # Populate Other if no other reason is given
        if len(ref_reasons) == 0:
            DATA_DF.at[i, 'mrr_Other'] = 1

# +
## Module 5: Read all four info columns, one hot encode symptoms
# for i, row in DATA_DF.iterrows():
#     ref_reason_statement_str = row['ref_reason'].lower()
#     chief_complaint_statement_str = row['chief_complaint'].lower()
#     admission_diagnosis_statement_str = row['admission_diagnosis'].lower()
#     discharge_diagnosis_statement_str = row['discharge_diagnosis'].lower()

#     all_statements = (split(ref_reason_statement_str) +
#                       split(chief_complaint_statement_str) +
#                       split(admission_diagnosis_statement_str) +
#                       split(discharge_diagnosis_statement_str))

#     for statement in all_statements:
#         symptoms = [s for s in SYMPTOMS
#                     if not contains(statement, IGNORE_KEYWORDS) and
#                     contains(statement, SYMPTOM_TO_KEYWORDS[s])]

#         for s in symptoms:
#             DATA_DF.at[i, str(s)] = 1
# -

## Output file
DATA_DF.to_excel("output-{}.xlsx".format(get_time()), engine='openpyxl')
