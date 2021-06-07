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
## Helper functions ##
"""
Returns if the val is nan
"""
def is_nan(val):
    return not (val == val)

"""
Convert a pandas dataframe to a dict of lists
Where keys are column names and lists are the column values, with nans removed
"""
def convert_to_dict_of_lists_no_nans(df):
    dict_of_lists = df.to_dict(orient='list')
    dict_of_lists_no_nans = {key: [x for x in list_ if not is_nan(x)]
                             for key, list_ in dict_of_lists.items()}
    return dict_of_lists_no_nans

"""
Returns string of hh-mm-ss
"""
from datetime import datetime
def get_date_time():
    now = datetime.now() # current date and time
    date_time = now.strftime("%m-%d-%Y_%H-%M-%S")
    return date_time

"""
Splits input string by delimiter
Brittleness warning: May need to adjust this!
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
    return pattern1.match(statement) or pattern2.match(statement)

"""
Returns True if statement contains any of words in keywords
Else return False
Also handles edge cases of short keywords
Brittleness warning: May need to adjust this!
HACKY! SHORT WORDS SHOULD LIKE THIS SHOULD ONLY BE COUNTED AS IN THE STATEMENT IF THERE IS NO LETTER BEFORE OR AFTER IT
EG. "asd " is okay, " fasd" is not okay
"""
def contains(statement, keywords):
    keywords_check_letter_before_or_after = ["id", "ied", "tic", "si", "asd"]

    for word in keywords:
        # Clean word. Only keep alphanumeric, dash, underscores, space, slash
        word = re.sub(r'[^a-zA-Z0-9-_ /]', '', word).lower()

        ## Edge case 1: ensure that there is no letter before or after keyword
        if word in keywords_check_letter_before_or_after:
            if not has_letter_before_or_after(statement, word) and word in statement:
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
