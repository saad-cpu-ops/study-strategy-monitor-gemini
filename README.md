# 🧠 Study Coach Bot

A Telegram bot that tracks your learning progress across 5 evidence-based dimensions, gives you AI-powered feedback after every session, and automatically logs everything to Notion.

Built on the **Meta-Learning Mastery Framework** — the same framework used by high-performance learners to identify and fix the real bottlenecks in their study habits.

---

## 📸 How it looks

**Daily check-in flow:**
```
Bot: 🧠 Deep Processing [1/5]
     After studying today, can you explain what you 
     learned in your own words without looking at notes?

     [ 1 — Not at all ]  [ 2 — A little ]
     [ 3 — Somewhat   ]  [ 4 — Mostly yes ]
          [ 5 — Absolutely yes ]
```

**After check-in — AI feedback:**
```
✅ Check-in complete — 🇩🇪 German

🧠 Deep Processing:     ⭐⭐⭐⭐ (4/5)
⚙️ Self-Regulation:     ⭐⭐ (2/5)
💭 Mindset:             ⭐⭐⭐⭐ (4/5)
🔁 Retrieval:           ⭐⭐⭐ (3/5)
🎯 Self-Management:     ⭐⭐⭐⭐ (4/5)

📊 Overall: 3.4/5

🔍 Analysis:
Good mindset and deep processing today. Self-regulation 
is still your main blocker — you didn't adjust your method 
when stuck. Next session: set a clear goal before starting 
and check it at the end.

🎯 Focus for next session:
Set a 20-min timer. When it rings ask: am I going deep 
or just reading?

📓 Logged to Notion!
```

---

## 🎯 The 5 Dimensions

| Dimension | What it measures |
|---|---|
| 🧠 Deep Processing | Are you thinking critically or just reading? |
| ⚙️ Self-Regulation | Are you monitoring and adjusting your method? |
| 💭 Mindset | How do you handle difficulty and mistakes? |
| 🔁 Retrieval | Are you testing your memory actively? |
| 🎯 Self-Management | Are you managing your focus and environment? |

---

## ⚙️ Features

- ✅ Daily check-in across all 5 learning dimensions
- ✅ AI-powered personalized feedback after every session
- ✅ Auto-detects your weakest dimension
- ✅ Gives you ONE specific action to improve next session
- ✅ Logs everything automatically to Notion
- ✅ Ask study questions anytime — bot knows your profile
- ✅ Tracks session quality (Excellent / Good / Average / Poor)
- ✅ Weekly progress tracking in Notion
- ✅ Completely free to run (Gemini API + Railway free tier)

---

## 🛠️ Tech Stack

- **Python** — bot logic
- **python-telegram-bot** — Telegram integration
- **Google Gemini API** — AI feedback (free tier)
- **Notion API** — progress tracking database
- **Railway** — free hosting

---

## 🚀 Setup Guide

### Step 1 — Create your Telegram bot
1. Open Telegram and search for `@BotFather`
2. Send `/newbot`
3. Follow the steps and copy your **bot token**

### Step 2 — Get your free Gemini API key
1. Go to [aistudio.google.com](https://aistudio.google.com)
2. Sign in with Google
3. Click **"Get API key"** — completely free, no credit card

### Step 3 — Set up Notion
1. Go to [notion.so](https://notion.so) and create an account
2. Create a new page with a **Table database** — name it `Study Monitoring System`
3. Go to [notion.so/profile/integrations](https://notion.so/profile/integrations)
4. Click **"New integration"** → name it `study-coach` → save
5. Copy the `secret_...` token
6. Open your database → click `...` → **Connections** → connect `study-coach`
7. Copy your **database ID** from the URL (the part between `/` and `?v=`)

### Step 4 — Set up the Notion database columns
Run the setup script once:
```bash
pip install requests
python setup_notion.py
```
It will automatically create all columns and add a sample entry.

### Step 5 — Deploy on Railway (free)
1. Fork this repo to your GitHub
2. Go to [railway.app](https://railway.app) and sign up with GitHub
3. Click **New Project** → **Deploy from GitHub repo** → select this repo
4. Go to the **Variables** tab and add:

| Variable | Value |
|---|---|
| `TELEGRAM_TOKEN` | your Telegram bot token |
| `NOTION_TOKEN` | your Notion `secret_...` token |
| `NOTION_DB_ID` | your Notion database ID |
| `GEMINI_KEY` | your Gemini API key |

5. Click **Deploy** — your bot is live! 🎉

---

## 💬 How to use

1. Open Telegram and find your bot
2. Send `/start`
3. After every study session → tap **"Daily check-in"**
4. Answer 5 quick questions (takes 2 minutes)
5. Get AI feedback + improvement tip
6. Everything logs to Notion automatically
7. When stuck on something → tap **"Ask a study question"**

---

## 📊 Notion Dashboard

Every session is logged with:
- Date and subject studied
- Score for each of the 5 dimensions
- Overall session quality rating
- AI-generated feedback
- Specific improvement focus for next session
- Week number for progress tracking

---

## 🔧 Customization

All customization is in `bot.py`:

| What to change | Where |
|---|---|
| Check-in questions | `DIMENSIONS` dictionary |
| Improvement tips | `"tips"` inside each dimension |
| AI personality | `system_prompt` in `finish_checkin` |
| Add new subjects | `subject_` buttons in `button_handler` |
| Welcome message | `start` function |

---

## 📄 License

MIT License — free to use, modify, and share.

---

## 🙏 Credits

Built on the **Meta-Learning Mastery Framework** and inspired by research on self-regulated learning, neuroplasticity, and cognitive performance.

> "High-level expertise is driven by invisible habits of thought, not by the external act of logging hours."

---

⭐ If this helped you, give it a star on GitHub!
