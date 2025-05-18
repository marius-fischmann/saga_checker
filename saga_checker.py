import logging
import requests
import hashlib
import os
import time
import random
from twilio.rest import Client

logging.basicConfig(level=logging.INFO)

def main():
    logging.info("Saga Checker Script wurde gestartet.")
    url = "https://www.saga.hamburg/immobiliensuche?Kategorie=APARTMENT"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept-Language": "de-DE,de;q=0.9"
    }

    try:
        time.sleep(random.randint(1, 5))  # leichte Verzögerung
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        content = response.text
        current_hash = hashlib.sha256(content.encode()).hexdigest()

        hash_file = "saga_hash.txt"
        old_hash = ""
        if os.path.exists(hash_file):
            with open(hash_file, "r") as f:
                old_hash = f.read().strip()

        if current_hash != old_hash:
            logging.info("Seiteninhalt hat sich geändert!")
            with open(hash_file, "w") as f:
                f.write(current_hash)
            send_sms("🚨 Die Saga-Webseite hat sich geändert.")
        else:
            logging.info("Keine Änderung festgestellt.")

    except Exception as e:
        logging.error(f"Fehler: {e}")

def send_sms(message_text):
    client = Client(
        os.getenv("TWILIO_ACCOUNT_SID"),
        os.getenv("TWILIO_AUTH_TOKEN")
    )
    client.messages.create(
        body=message_text,
        from_=os.getenv("TWILIO_FROM"),
        to=os.getenv("TWILIO_TO")
    )

if __name__ == "__main__":
    main()
