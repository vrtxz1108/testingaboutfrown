# 🎯 OxBoys Telegram Bot

A Telegram bot with 18 category lookup lists + personal vault system.

---

## 📋 Features
- 18 categories: DX, VALET, CS SUITE, NVBV NAV, NAV, SELF REV, CHECKER, INFO, MBIN, 1602, MCI/MA, BHG, MCR, BRELLA, MCP, DCS, NVBV DX
- Admin can upload/clear master lists per category
- Users send random 6-digit codes → bot shows which match
- 🔐 Personal Vault: each user stores their own private list and checks against it
- `/stats` command for admins

---

## 🚀 Setup (Step by Step)

### Step 1 — Get your Bot Token
1. Open Telegram → search **@BotFather**
2. Send `/newbot`
3. Follow prompts, copy the token it gives you

### Step 2 — Get your Telegram User ID
1. Open Telegram → search **@userinfobot**
2. Send `/start` — it'll show your ID number

### Step 3 — Deploy to Railway (FREE, 24/7)
1. Go to **https://railway.app** → sign up free
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Upload this folder to a GitHub repo first (or use Railway's file upload)
4. In Railway dashboard → **Variables** tab, add:
   - `BOT_TOKEN` = your token from BotFather
   - `ADMIN_IDS` = your Telegram user ID (e.g. `123456789`)
   - If multiple admins: `123456789,987654321`
5. Deploy! Railway will keep it running 24/7.

### Alternative: Run locally (for testing)
```bash
pip install -r requirements.txt
BOT_TOKEN="your_token" ADMIN_IDS="your_id" python bot.py
```

---

## 👑 Admin Commands

| Action | How |
|--------|-----|
| Upload master list for a category | Click the category → "⬆️ Upload Master List" → send codes |
| Clear a category list | Click category → "🗑️ Clear Master List" |
| View stats | Send `/stats` |

---

## 👤 User Flow

1. `/start` → see the menu
2. Click any category (e.g. **DX**)
3. Click **"📋 Send List to Check"**
4. Send your 6-digit codes (any format — one per line, spaces, etc.)
5. Bot instantly shows ✅ matches and ❌ non-matches

### Vault
1. Click **🔐 VAULT**
2. **"➕ Add to My Vault"** → send your personal master codes
3. **"📋 Check Against My Vault"** → send random codes to check
4. Only YOU can see your vault — completely private

---

## 📁 File Structure
```
oxboys_bot/
├── bot.py              # Main bot code
├── requirements.txt    # Dependencies
├── railway.toml        # Railway deployment config
├── Procfile            # For Heroku/Render
├── .env.example        # Environment variables template
└── data/               # Auto-created, stores all lists
    ├── master_lists.json
    └── vault_lists.json
```

---

## ⚠️ Notes
- The `data/` folder is created automatically
- All lists are saved to JSON files — they persist across restarts
- On Railway, use a **Volume** (free) to make data truly persistent
