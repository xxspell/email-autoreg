import re
from bs4 import BeautifulSoup
from simplegmail import Gmail
from core.utils.log import xlogger


def get_verification_code(forwarded_recipient):
    gmail = Gmail(client_secret_file='data/client_secret.json', creds_file='data/gmail_token.json')
    labels = gmail.list_labels()

    farming_label = list(filter(lambda x: x.name == 'Farming', labels))[0]
    query = f"to:{forwarded_recipient}"
    xlogger.debug(f"Receiving emails filtered by {forwarded_recipient} from inbox...")
    messages = gmail.get_messages(query=query, include_spam_trash=True)
    xlogger.debug(f"Messages received: {len(messages)}")

    for message in messages:
        sender = message.sender
        subject = message.subject
        if "support@duck.com" in sender and "Confirm your forwarding address" in subject:
            message.mark_as_read()
            message.add_label(farming_label)
            message.remove_label("INBOX")
            body = message.plain or message.html

            if not body:
                xlogger.debug("Email body is empty.")
                return None

            decoded_html = re.sub(r"=3D", "=", body)

            xlogger.debug(f"Decoded HTML: {decoded_html}")

            match = re.search(r"one-time passphrase in your open DuckDuckGo tab:\s*([^\n]+)", decoded_html)
            if match:
                phrase = match.group(1).strip()
                xlogger.debug(f"Found phrase: {phrase}")
                return phrase

            soup = BeautifulSoup(decoded_html, 'html.parser')
            phrase = soup.find('p')
            if phrase is None:
                xlogger.debug("Element <p> not found in the parsed HTML.")
                return None

            phrase_text = phrase.get_text(strip=True)
            xlogger.debug(f"Phrase from <p>: {phrase_text}")

            return phrase_text

    xlogger.debug("No phrase found.")
    return None