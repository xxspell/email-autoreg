import os

from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
if OPENROUTER_API_KEY is None:
    raise ValueError(f"Environment variable 'OPENROUTER_API_KEY' was not found in the .env file.")

SLOWED_MODE = os.environ.get("SLOWED_MODE")
if SLOWED_MODE is None:
    raise ValueError(f"Environment variable 'SLOWED_MODE' was not found in the .env file.")
