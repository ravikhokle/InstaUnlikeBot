# Insta Unlike Bot 🔧

**Automatically unlike Instagram posts/reels you've previously liked.**

---

## ✅ Quick Start

1. **Install Python 3** (recommended 3.8+).
2. Open a terminal in this project folder and run:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a file named `.env` in the same folder as `bot.py` and add your credentials:

   ```env
   IG_USERNAME=your_instagram_username
   IG_PASSWORD=your_instagram_password
   ```

4. Run the bot:

   ```bash
   python bot.py
   ```

---

## 🔍 What the Bot Does

- Opens Google Chrome automatically
- Logs into your Instagram account
- Navigates to **Your Activity → Likes**
- Selects liked posts and unlikes them in batches

---

## ⚙️ Requirements & Notes

- **Google Chrome** must be installed. If the script requires a ChromeDriver, ensure it matches your Chrome version or use a webdriver manager (see `requirements.txt`).
- Keep the `.env` file private — **do not commit** it to source control.
- Use a secondary or disposable account for automation to reduce risk.

> ⚠️ Automation may violate Instagram's terms of service and can result in account action. Use at your own risk.

---

## ⚡ Speed Control (How to tune)

You can control how aggressively the bot operates by editing the `SPEED_PROFILE` variable in `bot.py`. Available options: **`slow`**, **`safe`**, **`fast`**, **`aggressive`**.

**How the profile affects behavior:**
- `click` — per-click delay (seconds).
- `burst` — short pause inserted every few actions.
- `batch_pause` — pause after finishing a batch of unlikes.
- `scroll` — delay after each scroll step.

**Recommended usage:**
- **safe** — Recommended for most users (balanced speed and reduced detection risk). ✅
- **slow** — Use if you have 2FA, frequent login checks, or want lowest risk. ⚠️
- **fast** — Faster, but increases chance of being flagged. Use with caution. ⚠️
- **aggressive** — Very fast and high-risk. Only use on a disposable/secondary account. ❗

**Other settings to consider:**
- `BATCH_SIZE` — number of posts to select per batch. Try **20–50** for safer runs.
- `MAX_BATCHES` — number of batches per run.
- `DAILY_MAX_UNLIKES` — hard stop to prevent excessive activity.

To change how the bot behaves, open `bot.py`, update `SPEED_PROFILE` (and optionally `BATCH_SIZE` / `DAILY_MAX_UNLIKES`), save the file, and run `python bot.py`.

---

## 🛑 Stopping the Bot

- Press **CTRL + C** in the terminal to stop immediately.
- Or allow it to finish and press **ENTER** when prompted.

---

## 🐞 Troubleshooting

- Login fails: double-check your username/password in `.env`. If Instagram prompts for verification or 2FA, the bot may not be able to complete login.
- Chrome doesn't open or WebDriver errors: make sure Chrome is installed and the ChromeDriver (if needed) is compatible with your Chrome version.
- Bot doesn't find or unlike posts anymore: Instagram's UI can change. The selectors may need updating.

---

## ✍️ Contributing & Issues

- Found a bug or want a feature? Open an issue or submit a PR.

---

## 📜 Disclaimer

This project is provided "as-is." The author is not responsible for any account actions resulting from use of this tool.

---

Happy unliking! ✅
