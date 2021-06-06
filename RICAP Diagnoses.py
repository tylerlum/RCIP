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

import openpyxl

import MyFunctions

# +
## Import data
filename = "FULLWITHOUTTYLERSSTUFFResearchInChildAndAd_DATA_2018-12-14_1531.xlsx"
workbook = openpyxl.load_workbook(filename)

## Get sheets
data_sheet = workbook["ResearchInChildAndAd_DATA_2018-"]
illness_keywords_sheet = workbook["Illness Keywords"]
mrr_sheet = workbook["MRR Keywords"]
symptoms_sheet = workbook["Symptoms"]

# +
## Setup keywords
IGNORE_KEYWORDS = ['query', 'vs', 'r/o', 'rule out', 'versus']

## Get illnesses
ILLNESS_KEYWORDS = read_in_illness_keywords(illness_keywords_sheet)
ILLNESSES = get_key_list(ILLNESS_KEYWORDS)

## Get reasons for referral
REASON_FOR_REFERRAL_KEYWORDS = read_in_mrr_keywords(mrr_sheet)
REASONS_FOR_REFERRAL = get_key_list(REASON_FOR_REFERRAL_KEYWORDS)

## Get other symptoms
SYMPTOM_KEYWORDS = read_in_symptom_keywords(symptoms_sheet)
SYMPTOMS = get_key_list(SYMPTOM_KEYWORDS)
# -

## Module 0: Add columns headers
set_illness_headers(data_sheet, 'admission', ILLNESSES)
set_illness_headers(data_sheet, 'discharge', ILLNESSES)
set_mrr_headers(data_sheet, REASONS_FOR_REFERRAL)
set_symptom_headers(data_sheet, SYMPTOMS)

## Module 1: Set binary values to 0
set_illnesses_to_zero(data_sheet, "admission", ILLNESSES)
set_illnesses_to_zero(data_sheet, "discharge", ILLNESSES)
set_mrr_to_zero(data_sheet, REASONS_FOR_REFERRAL)
set_symptoms_to_zero(data_sheet, SYMPTOMS)

## Module 2: Fill in main diagnosis
set_main_diagnosis(data_sheet, "admission", IGNORE_KEYWORDS, ILLNESS_KEYWORDS)
set_main_diagnosis(data_sheet, "discharge", IGNORE_KEYWORDS, ILLNESS_KEYWORDS)

## Module 3: Read diagnoses, one hot encode symptoms
ohe_illnesses(data_sheet, 'admission', IGNORE_KEYWORDS, ILLNESS_KEYWORDS)
ohe_illnesses(data_sheet, 'discharge', IGNORE_KEYWORDS, ILLNESS_KEYWORDS)

## Module 4: Read ref_reason + chief_complaint, one hot encode symptoms
ohe_mrr(data_sheet, IGNORE_KEYWORDS, REASON_FOR_REFERRAL_KEYWORDS)

## Module 5: Read all four info columns, one hot encode symptoms
ohe_symptoms(data_sheet, IGNORE_KEYWORDS, SYMPTOM_KEYWORDS)

## Output file
workbook.save("output-{}.xlsx".format(getTime()))
