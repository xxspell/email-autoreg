import random

from core.utils.generator.nickname import generate_username


def tags_email_generator(emails_file: str, count: int, tags_file: str = "data/wordlist/surnames.txt"):

    with open(emails_file, 'r') as f:
        base_emails = f.read().splitlines()

    with open(tags_file, 'r') as f:
        tags = f.read().splitlines()

    if not tags:
        tags = [str(i) for i in range(1000)]

    all_variants = []
    for email in base_emails:
        local_part, domain = email.split('@')

        for tag in tags:
            all_variants.append(f"{local_part}+{tag}@{domain}")

    random.shuffle(all_variants)

    if len(all_variants) < count:
        all_variants = (all_variants * (count // len(all_variants) + 1))[:count]
    else:
        all_variants = all_variants[:count]

    for email in all_variants:
        local = generate_username()
        yield email, local

