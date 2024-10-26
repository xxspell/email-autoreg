
import os
import aiofiles

async def save_to_csv(filename="accounts.csv", account=None):

    file_exists = os.path.isfile(filename)

    async with aiofiles.open(filename, mode='a', newline='', encoding='utf-8') as file:

        if not file_exists:
            await file.write("email,user\n")

        if account:
            await file.write(f"{account['email']},{account['user']}\n")



def load_proxies(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return [line.strip() for line in file if line.strip()]
    return []
