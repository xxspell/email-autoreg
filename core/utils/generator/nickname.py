import random
from datetime import datetime
from typing import Tuple, Any


def load_wordlist(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        words = [line.strip() for line in file if line.strip()]
    return words


def generate_username():
    first_names = load_wordlist('data/wordlist/names.txt')
    last_names = load_wordlist('data/wordlist/surnames.txt')
    words = load_wordlist('data/wordlist/words.txt')

    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    word = random.choice(words)

    current_year = datetime.now().year
    formats = [
        lambda: str(random.randint(0, 99)),  # Single-digit number
        lambda: random.randint(1, 28),  # Day
        lambda: random.randint(1, 12),  # Month
        lambda: random.randint(current_year - 50, current_year),  # Year
        lambda: random.randint(1, 28) + random.randint(1, 12),  # Day and month
        lambda: random.randint(1, 12) + random.randint(current_year - 50, current_year),  # Month and year
        lambda: random.randint(1, 28) + random.randint(1, 12) + random.randint(current_year - 50, current_year),
        # Day, month and year
    ]

    random_number = random.choice(formats)()
    username_formats = [
        f"{first_name}.{last_name}",  # john.doe
        f"{first_name}.{word}",  # john.sky
        f"{first_name}.{random_number}",  # john.2000
        f"{first_name}{last_name}{random_number}",  # johndoe1998
        f"{first_name}.{random_number}.{word}",  # john.22.sky
        f"{last_name}.{random_number}",  # doe.02
        f"{random_number}.{first_name}",  # 1998.john
        f"{word}.{last_name}",  # sky.doe
        f"{first_name}.{random_number}",  # john.12.02
        f"{first_name}.{last_name}.{random_number}",  # john.doe.1995
        f"{word}.{random_number}",  # sky.1985
        f"{last_name}.{random_number}",  # doe.05.1980
        f"{random_number}.{first_name}.{word}",  # 2003.john.sky
        f"{last_name}.{first_name}",  # doe.john
        f"{last_name}.{random_number}.{first_name}",  # doe.1995.john
        f"{word}{random_number}{last_name}",  # sky.1990.doe
        f"{first_name}.{random_number}.{last_name}",  # john.1988.doe
    ]

    username = random.choice(username_formats)

    while ".." in username:
        username = username.replace("..", ".")

    while "-" in username:
        username = username.replace("-", ".")

    dot_count = username.count(".")
    # dots_to_remove = random.randint(0, dot_count)
    dots_to_remove = dot_count
    while dots_to_remove > 0:
        dot_index = username.find(".", random.randint(0, len(username) - 1))
        if dot_index != -1:
            username = username[:dot_index] + username[dot_index + 1:]
            dots_to_remove -= 1

    return username


def generate_email(domain) -> tuple[str, str]:
    local = generate_username()
    return f"{local}@{domain}", local
