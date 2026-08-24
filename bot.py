"""Polls the private chat with a bot since last check, forwards messages
matching KEYWORD to Saved Messages. Designed for GitHub Actions cron."""
import asyncio, json, os, sys
from telethon import TelegramClient
from telethon.sessions import StringSession

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION = os.environ["TELETHON_SESSION"]
SOURCE = os.environ["SOURCE_BOT"]      # e.g. "some_bot" (username) or numeric chat id
KEYWORD = os.environ["KEYWORD"].lower()
STATE_FILE = "state.json"

async def main():
    client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)
    await client.start()

    me = await client.get_me()
    entity = await client.get_entity(SOURCE)

    # load last seen message id
    last_id = 0
    if os.path.exists(STATE_FILE):
        last_id = json.load(open(STATE_FILE)).get("last_id", 0)

    msgs = await client.get_messages(entity, limit=100, min_id=last_id)
    new_last = last_id
    sent = 0
    for m in reversed(msgs):  # oldest first
        new_last = max(new_last, m.id)
        text = m.raw_text or ""
        if text and KEYWORD in text.lower():
            header = f"🔔 Keyword '{KEYWORD}' from @{getattr(entity,'username',SOURCE)}:"
            await client.send_message("me", f"{header}\n\n{text}")
            sent += 1

    json.dump({"last_id": new_last}, open(STATE_FILE, "w"))
    print(f"Checked chat of {SOURCE}: {len(msgs)} new msgs, forwarded {sent} matching '{KEYWORD}'.")
    await client.disconnect()
    if sent == 0:
        # keep Actions log quiet-ish but exit 0; state committed by workflow
        pass

asyncio.run(main())
