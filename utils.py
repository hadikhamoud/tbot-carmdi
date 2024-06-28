import os
import re
import yaml


ACCEPTED_CAR_CODES = set(["A","B","Y","G","N","O","S","T","K","Z","M","C","D","J","M","P"])
CAR_NUMBER_REGEX = re.compile(r'^\d+\s([A-Za-z\u0600-\u06FF]{1,2})$')
PHONE_NUMBER_REGEX = re.compile(r'^\d{6}$')
TEL_PROP_INDEX = 15


def read_config(fp = 'config.yaml'):
    with open(fp, 'r') as file:
        return yaml.safe_load(file)

def match_user_input(text):
    if CAR_NUMBER_REGEX.match(text):
        return "car"
    elif PHONE_NUMBER_REGEX.match(text):
        return "phone"
    else:
        return None
    
def match_car_code(text):
    if text.split()[1].upper() in ACCEPTED_CAR_CODES:
        return True
    else:
        return False

def check_user_input(text):
    matched_input = match_user_input(text)
    if matched_input == "car":
        # if match_car_code(text):
        return "car valid"
    if matched_input == "phone":
        return "phone valid"
    
    return "invalid"

