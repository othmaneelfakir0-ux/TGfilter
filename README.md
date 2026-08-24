# Telegram keyword filter (userbot + GitHub Actions)

Forwards messages from a bot's private chat to your Saved Messages when they contain a keyword.

## One-time setup

1. Get API credentials at https://my.telegram.org → "API development tools" → note `api_id` and `api_hash`.
2. Generate your session string locally:
   ```
   .venv/Scripts/python gen_session.py
   ```
   (asks for api_id, api_hash, phone, login code)
3. Create a **private** GitHub repo and copy these files into it.
4. In repo → Settings → Secrets and variables → Actions, add:
   - `API_ID`, `API_HASH`, `TELETHON_SESSION` (from step 2)
   - `SOURCE_BOT` — username of the bot to watch (e.g. `some_bot`)
   - `KEYWORD` — the word to filter on
5. Actions tab → enable workflows. It runs every 5 min; you can also trigger manually with "Run workflow".

## Notes
- GitHub cron can be a few minutes late; that's normal on free tier.
- The session string = full access to your Telegram account. Keep the repo private.
- Change KEYWORD secret anytime — no code edit needed.
- To watch multiple keywords: change matching in bot.py (`any(k in text.lower() for k in [...])`).
