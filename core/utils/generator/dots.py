import random
from itertools import combinations

from core.utils.generator.nickname import generate_username


def generate_dot_variants(email: str) -> list:
    local_part, domain = email.split('@')
    positions = range(1, len(local_part))
    variants = [local_part]

    for r in range(1, len(positions) + 1):
        for dots_positions in combinations(positions, r):

            new_local = list(local_part)

            for pos in sorted(dots_positions, reverse=True):
                new_local.insert(pos, '.')
            variants.append(''.join(new_local))

    return [f"{variant}@{domain}" for variant in variants]


def dots_email_generator(emails_file: str, count: int):
    with open(emails_file, 'r') as f:
        base_emails = f.read().splitlines()

    all_variants = []
    for email in base_emails:
        all_variants.extend(generate_dot_variants(email))

    random.shuffle(all_variants)

    if len(all_variants) < count:

        all_variants = (all_variants * (count // len(all_variants) + 1))[:count]
    else:

        all_variants = all_variants[:count]

    for email in all_variants:
        local = generate_username()
        yield email, local
