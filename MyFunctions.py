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

from copy import copy

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
Handle edge cases of illnesses
Return fixed illnesses list
"""
def manipulate_illness_list(illnesses):
    illnesses = copy(illnesses)

    ## EOS/Personality
    if "Schizophrenia Spectrum and Other Psychotic Disorders" in illnesses and "Personality" in illnesses:
        illnesses.remove("Schizophrenia Spectrum and Other Psychotic Disorders")      
    
    return illnesses
