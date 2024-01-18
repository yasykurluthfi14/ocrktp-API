from datetime import datetime, timedelta
import random
import string

authorization_codes = {}

def generate_authorization_code():
    authorization_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    return authorization_code

def generate_authorization_data():
    authorization_code = generate_authorization_code()
    expiry_time = datetime.now() + timedelta(minutes=10)
    authorization_codes[authorization_code] = expiry_time
    return authorization_code, expiry_time

def is_valid_authorization(authorization_code, expiry_time):
    current_time = datetime.now()
    if authorization_code in authorization_codes and expiry_time is not None and current_time < expiry_time:
        return True
    return False

