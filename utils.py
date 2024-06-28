import os
import re

ACCEPTED_CAR_CODES = set(["A","B","Y","G","N","O","S","T","K","Z","M","C","D","J","M","P"])
CAR_NUMBER_REGEX = re.compile(r'^\d+\s[a-zA-Z]$')
PHONE_NUMBER_REGEX = re.compile(r'^\d{6}$')

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
        if match_car_code(text):
            return "car valid"
    if matched_input == "phone":
        return "phone valid"
    
    return "invalid"

