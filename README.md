
# Autoreger duck.com email addresses

This project automates the registration of duck.com email addresses. It uses OpenRouter AI's API to solve CAPTCHAs, simulates user behavior to avoid detection, and saves registered accounts to a CSV file.

## Requirements

- Python 3.10+
- Libraries listed in `pyproject.toml`
- An OpenRouter API key
- A Gmail account with configured forwarding to the target domain and credentials saved in `data/client_secret.json` and `data/gmail_token.json`.  This Gmail account will be used to retrieve verification codes.
- Wordlists for username generation (included in the `data/wordlist` directory)


## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your_username/email-autoreg.git  # Replace with your repo URL
   cd email-autoreg


2. **Create and activate a virtual environment (recommended):**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Linux/macOS
   .venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies:**

   ```bash
   pip install poetry
   poetry install
   ```

4. **Set up your environment variables:**

   - Create a `.env` file in the root directory of the project.
   - Add your OpenRouter API key to the `.env` file:

   ```
   OPENROUTER_API_KEY=your_openrouter_api_key
   ```

   -  Create a `data` directory and place your `gmail_token.json` and `client_secret.json` files inside as specified in the `core/mail/main.py` file.

5. **Prepare proxy list (Optional):**

   Create a `proxies.txt` file in the root directory and add your proxies, one per line, in the format `protocol://login:password@ip:port` (e.g., `socks://admin:admin@127.0.0.1:8080`). If you don't use proxies, the script will prompt you for the path, and you can just press Enter to skip it.

## Usage

You can run the script with command-line arguments or interactively.

**Command-line arguments:**

```bash
python main.py --domain your_domain.com --num_accounts 10 --max_connections 5 --proxy_path proxies.txt
```

- `--domain`: The domain part of the email addresses to be created (e.g., `your_domain.com`).
- `--num_accounts`: The number of accounts to create.
- `--max_connections`: The maximum number of concurrent connections. Use a different Gmail account if you experience connection issues or use lower value.
- `--proxy_path`:  Path to your proxy list file. (Optional.  If omitted, will prompt for input.)

**Interactive mode:**

If you run the script without arguments, it will prompt you for the required information.

```bash
python main.py
```

## Output

Registered accounts will be saved to `accounts.csv` in the project root.  Logs will be written to both the console and `application.log`.
