import random
import string


def generate_password():
    min_length = 8
    max_length = 16

    lowercase_letters = string.ascii_lowercase
    uppercase_letters = string.ascii_uppercase
    digits = string.digits
    all_chars = lowercase_letters + uppercase_letters + digits

    password = [
        random.choice(uppercase_letters),
        random.choice(digits),
        random.choice(digits)
    ]

    remaining_length = random.randint(min_length, max_length) - len(password)
    password += random.choices(all_chars, k=remaining_length)

    random.shuffle(password)

    return ''.join(password)
