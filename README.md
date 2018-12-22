# RCIP
Data Processing of Psychological Assessment Data

This repository contains Python code for data wrangling RCIP research data, in hopes of creating a predictive model for the changes in psychological health. This includes:

1. Processing raw diagnosis description in note form into explicit illness diagnosis by finding key diagnosis vocabulary. This Python script uses over 15 different categories of psychological illness, including depression, anxiety, and psychological trauma. 

2. One hot encoding of psychological illnesses for ease of analyzing the data. It also accounts for rule-outs and querying of different diagnoses to ensure only confident diagnoses are recorded.

## Example of One-hot Encoding Diagnosis and Identifying Main Diagnosis

![alt text](images/Diagnosis_Processing.png?raw=true "Diagnosis_Processing")

## Example of Rule-Outs in Diagnosis

![alt text](images/Rule_Out.png?raw=true "Rule_Out")
