# Autoreger duck.com email addresses

This project automates the registration of duck.com email addresses. It uses OpenRouter AI's API to solve CAPTCHAs, simulates user behavior to avoid detection, and saves registered accounts to a CSV file.

## Requirements

- Python 3.10+
- Libraries listed in `pyproject.toml`
- An OpenRouter API key
- Proxies
- A Gmail account with configured forwarding to the target domain and credentials saved in `data/client_secret.json` and `data/gmail_token.json`. This Gmail account will be used to retrieve verification codes.
- Wordlists for username generation (included in the `data/wordlist` directory)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/xxspell/email-autoreg.git
   cd email-autoreg
   ```

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
   - Create a `data` directory and place your `gmail_token.json` and `client_secret.json` files inside as specified in the `core/mail/main.py` file.

5. **Prepare proxy list (Optional):**
   Create a `proxies.txt` file in the root directory and add your proxies, one per line, in the format `protocol://login:password@ip:port` (e.g., `socks://admin:admin@127.0.0.1:8080`).

## Usage

The script supports three modes of email generation and can be run with command-line arguments or interactively.

### Email Generation Modes

1. **Domain Mode**: Generates new email addresses using a specified domain
2. **Dots Mode**: Generates variations of existing email addresses by adding dots in different positions
3. **Tags Mode**: Generates variations of existing email addresses by adding tags 
   > ⚠️ **Important Note**: Duck.com currently does not support registration with tagged email addresses (e.g., `name+tag@domain.com`). This mode is included for future compatibility if the policy changes or for use with other services.

## Important Notes and Limitations

1. **Tags Mode Limitation**: Duck.com does not currently allow registration using email addresses with tags (format: `name+tag@domain.com`). While this mode is included in the script, it won't work with Duck.com registration. Consider using domain mode or dots mode instead.

2. **Rate Limiting**: To avoid detection and blocking, it's recommended to use reasonable delays between requests and not create too many accounts at once.

3. **Proxy Quality**: The success rate heavily depends on the quality of your proxies. Using residential proxies is recommended.


### Command-line Arguments

```bash
# Domain Mode
python main.py --domain_mode --domain your_domain.com --num_accounts 10 --max_connections 5 --proxy_path proxies.txt

# Dots Mode
python main.py --dots_mode --emails_file dots_emails.txt --num_accounts 10 --max_connections 5 --proxy_path proxies.txt

# Tags Mode
python main.py --tags_mode --emails_file tags_emails.txt --num_accounts 10 --max_connections 5 --proxy_path proxies.txt
```

Arguments:
- `--domain_mode`, `--dots_mode`, `--tags_mode`: Select the email generation mode
- `--domain`: Domain for new email addresses (used in domain mode)
- `--emails_file`: File containing existing email addresses (used in dots and tags modes)
- `--num_accounts`: Number of accounts to create
- `--max_connections`: Maximum concurrent connections
- `--proxy_path`: Path to proxy list file
- `--export`: Export duck.com email from accounts.csv to a specified file

### Interactive Mode

Run without arguments for interactive mode:
```bash
python main.py
```

The script will prompt you to:
1. Select the generation mode
2. Provide necessary information based on the selected mode
3. Specify number of accounts and connections

### File Formats

1. **Emails File** (for dots and tags modes):
   ```
   email1@domain.com
   email2@domain.com
   ```
   
2. **Proxies File**:
   ```
   socks5:\\login@pass:pool-proxies.com
   ```
   

## Output

- Registered accounts are saved to `accounts.csv` in the project root
- Logs are written to both the console and `application.log`
