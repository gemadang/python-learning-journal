import unittest

def password_valid(password):
    password_len = len(password) > 7

    if not password_len:
        return False

    password_upper = False
    password_lower = False
    password_digit = False
    password_special = False

    for letter in password:
        if letter.isupper():
            password_upper = True
        if letter.islower():
            password_upper = True
        if letter.isdigit():
            password_digit = True 
        if letter in ""!

    return password_upper and password_lower and password_digit and password_special

class TestPassword(unittest.TestCase):


if __name__ == "__main__":
    unittest.main()