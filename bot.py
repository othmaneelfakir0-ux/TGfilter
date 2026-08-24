"""Polls the private chat with a bot since last check, forwards messages
matching KEYWORD to your alerts channel. Designed for GitHub Actions cron."""
import asyncio, json, os
from telethon import TelegramClient
from telethon.sessions import StringSession

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION = os.environ["TELETHON_SESSION"]
SOURCE = os.environ["SOURCE_BOT"]      # e.g. "some_bot" (username) or numeric chat id
KEYWORD = os.environ["KEYWORD"].lower()
DEST_TITLE = os.environ.get("DEST_CHANNEL", "🔔 Alerts")
STATE_FILE = "state.json"

async def find_dest(client):
    """Resolve destination: try numeric ID first, else search dialog titles."""
    dest_env = os.environ.get("DEST_ID", "").strip()
    if dest_env:
        try:
            return await client.get_entity(int(dest_env))
        except Exception:
            pass
    async for d in client.iter_dialogs():
        if d.is_channel and d.name.strip() == DEST_TITLE:
            return d.entity
    raise RuntimeError(f"Channel '{DEST_TITLE}' not found in your dialogs. Did you join it with this account?")

async def main():
    client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)
    await client.start()

    entity = await client.get_entity(SOURCE)
    dest = await find_dest(client)

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
            await client.send_message(dest, f"🔔 {KEYWORD}\n\n{text}")
            sent += 1

    json.dump({"last_id": new_last}, open(STATE_FILE, "w"))
    print(f"Checked chat of {SOURCE}: {len(msgs)} new msgs, forwarded {sent} matching '{KEYWORD}' to '{DEST_TITLE}'.")
    await client.disconnect()

asyncio.run(main())
