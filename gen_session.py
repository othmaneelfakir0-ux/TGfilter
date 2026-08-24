"""Run this ONCE locally to generate TELETHON_SESSION.
It asks for api_id / api_hash and your phone, sends you a Telegram code.
Prints the session string to put in GitHub Secrets."""
import os
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

api_id = int(input("API_ID: "))
api_hash = input("API_HASH: ").strip()

with TelegramClient(StringSession(), api_id, api_hash) as client:
    s = client.session.save()
    print("\n=== COPY THIS INTO GITHUB SECRET 'TELETHON_SESSION' ===")
    print(s)
    print("=========================================================")
