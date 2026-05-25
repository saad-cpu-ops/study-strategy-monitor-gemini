import os
import json
import asyncio
import datetime
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DB_ID = os.getenv("NOTION_DB_ID")
GEMINI_KEY = os.getenv("GEMINI_KEY")

NOTION_HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

DIMENSIONS = {
    "deep_processing": {
        "name": "Deep Processing",
        "emoji": "🧠",
        "questions": "After studying today, can you explain what you learned in your own words without looking at notes?",
        "tips": {
            "low": "Close your notes and write a summary from memory. Then check what you missed.",
            "medium": "After each concept, ask: where would I use this in real life?",
            "high": "Try teaching the concept out loud as if explaining to a friend."
        }
    },
    "self_regulation": {
        "name": "Self-Regulation",
        "emoji": "⚙️",
        "questions": "Did you notice your method wasn't working at any point and change it?",
        "tips": {
            "low": "Before every session write: what do I want to be able to DO after this? Check it at the end.",
            "medium": "Set a 20-minute timer. When it rings, ask: am I going deep or just reading?",
            "high": "Experiment with one new technique this week and compare results."
        }
    },
    "mindset": {
        "name": "Mindset",
        "emoji": "💭",
        "questions": "Did you face something difficult today? Did you push through or avoid it?",
        "tips": {
            "low": "Write down one mistake you made today and what it taught you. Mistakes are data.",
            "medium": "When something feels hard, say: this difficulty means I am growing.",
            "high": "Start deliberately choosing the hardest exercises first."
        }
    },
    "retrieval": {
        "name": "Retrieval",
        "emoji": "🔁",
        "questions": "Did you test yourself from memory today without looking at notes or answers?",
        "tips": {
            "low": "After every session, close everything and write 5 things you remember. Brain dump.",
            "medium": "Review yesterday's material for 10 min before starting new content.",
            "high": "Practice under exam conditions — timed, no notes, real problems."
        }
    },
    "self_management": {
        "name": "Self-Management",
        "emoji": "🎯",
        "questions": "Where was your phone during the session? How many times did you get distracted?",
        "tips": {
            "low": "Nuclear option: phone in another room, one tab open, timer running. No exceptions.",
            "medium": "Create a 2-minute start ritual: phone away, water ready, goal written, timer set.",
            "high": "Identify your single biggest distraction and eliminate it permanently."
        }
    }
}

user_sessions = {}

def ask_gemini(system_prompt, user_message, history=None):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    
    contents = []
    if history:
        for msg in history:
            role = "user" if msg["role"] == "user" else "model"
            contents.append({"role": role, "parts": [{"text": msg["content"]}]})
    contents.append({"role": "user", "parts": [{"text": user_message}]})
    
    payload = {
        "system_instruction": {"parts": [{"text": system_prompt}]},
        "contents": contents,
        "generationConfig": {"maxOutputTokens": 1000, "temperature": 0.7}
    }
    
    response = requests.post(url, json=payload)
    result = response.json()
    return result["candidates"][0]["content"]["parts"][0]["text"]

def log_to_notion(data):
    url = "https://api.notion.com/v1/pages"
    today = datetime.date.today().isoformat()
    
    properties = {
        "Date": {"date": {"start": today}},
        "Subject": {"select": {"name": data.get("subject", "General")}},
        "Deep Processing": {"number": data.get("deep_processing", 0)},
        "Self-Regulation": {"number": data.get("self_regulation", 0)},
        "Mindset": {"number": data.get("mindset", 0)},
        "Retrieval": {"number": data.get("retrieval", 0)},
        "Self-Management": {"number": data.get("self_management", 0)},
        "Overall Score": {"number": data.get("overall", 0)},
        "AI Feedback": {"rich_text": [{"text": {"content": data.get("feedback", "")[:2000]}}]},
        "Improvement Focus": {"rich_text": [{"text": {"content": data.get("focus", "")[:2000]}}]}
    }
    
    payload = {"parent": {"database_id": NOTION_DB_ID}, "properties": properties}
    r = requests.post(url, headers=NOTION_HEADERS, json=payload)
    return r.status_code

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    keyboard = [
        [InlineKeyboardButton("📚 Daily check-in", callback_data="checkin")],
        [InlineKeyboardButton("❓ Ask a study question", callback_data="ask")],
        [InlineKeyboardButton("💡 Quick tips", callback_data="tips")]
    ]
    await update.message.reply_text(
        f"Hey {user}! 👋 I'm your Study Coach.\n\n"
        f"I track your progress across 5 dimensions:\n"
        f"🧠 Deep Processing — are you thinking or just reading?\n"
        f"⚙️ Self-Regulation — are you adjusting your method?\n"
        f"💭 Mindset — how you handle difficulty\n"
        f"🔁 Retrieval — are you testing your memory?\n"
        f"🎯 Self-Management — focus and environment\n\n"
        f"What do you want to do?",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data

    if data == "checkin":
        keyboard = [
            [InlineKeyboardButton("🇩🇪 German", callback_data="subject_German")],
            [InlineKeyboardButton("💻 IT Certification", callback_data="subject_IT Cert")],
            [InlineKeyboardButton("🐛 Bug Bounty", callback_data="subject_Bug Bounty")]
        ]
        await query.message.reply_text(
            "What did you study today?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == "ask":
        user_sessions[user_id] = {"mode": "ask", "history": []}
        await query.message.reply_text(
            "Go ahead — ask me anything about your studies, a concept you're stuck on, or how to improve. 🎯"
        )

    elif data == "tips":
        await query.message.reply_text(
            "💡 *Quick tips for your 3 goals:*\n\n"
            "🇩🇪 *German B1→B2:* Speak out loud every day even alone. Make mistakes on purpose.\n\n"
            "💻 *IT Certs:* Do practice exams from day 1, not just at the end. Failing early = learning faster.\n\n"
            "🐛 *Bug Bounty:* Pick ONE platform (HackerOne or Bugcrowd), ONE target. Go deep not wide.\n\n"
            "⚙️ *Self-regulation:* Every 20 min ask: can I explain this without notes?",
            parse_mode="Markdown"
        )

    elif data.startswith("subject_"):
        subject = data.replace("subject_", "")
        user_sessions[user_id] = {
            "mode": "checkin",
            "subject": subject,
            "dimension_index": 0,
            "scores": {}
        }
        await ask_next_dimension(query.message, user_id)

    elif data.startswith("score_"):
        parts = data.split("_")
        dim = parts[1]
        score = int(parts[2])
        if user_id in user_sessions:
            user_sessions[user_id]["scores"][dim] = score
            user_sessions[user_id]["dimension_index"] += 1
            await ask_next_dimension(query.message, user_id)

async def ask_next_dimension(message, user_id):
    session = user_sessions.get(user_id)
    if not session:
        return

    dim_keys = list(DIMENSIONS.keys())
    idx = session["dimension_index"]

    if idx >= len(dim_keys):
        await finish_checkin(message, user_id)
        return

    dim_key = dim_keys[idx]
    dim = DIMENSIONS[dim_key]

    keyboard = [
        [
            InlineKeyboardButton("1 — Not at all", callback_data=f"score_{dim_key}_1"),
            InlineKeyboardButton("2 — A little", callback_data=f"score_{dim_key}_2")
        ],
        [
            InlineKeyboardButton("3 — Somewhat", callback_data=f"score_{dim_key}_3"),
            InlineKeyboardButton("4 — Mostly yes", callback_data=f"score_{dim_key}_4")
        ],
        [InlineKeyboardButton("5 — Absolutely yes", callback_data=f"score_{dim_key}_5")]
    ]

    await message.reply_text(
        f"{dim['emoji']} *{dim['name']}* [{idx+1}/5]\n\n{dim['questions']}",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def finish_checkin(message, user_id):
    session = user_sessions.get(user_id)
    scores = session["scores"]
    subject = session["subject"]

    overall = round(sum(scores.values()) / len(scores), 1)
    weakest_key = min(scores, key=scores.get)
    weakest = DIMENSIONS[weakest_key]
    weakest_score = scores[weakest_key]
    level = "low" if weakest_score <= 2 else "medium" if weakest_score <= 3 else "high"
    tip = weakest["tips"][level]

    score_summary = "\n".join([
        f"{DIMENSIONS[k]['emoji']} {DIMENSIONS[k]['name']}: {'⭐' * v} ({v}/5)"
        for k, v in scores.items()
    ])

    system_prompt = """You are a study coach AI. The student is Saad.
His learning profile: Sprout learner (53% overall), Self-regulation 27% (biggest weakness), Deep processing 67%, Mindset 60% (his strength — believes he can be the best), Retrieval and Self-management also need work.
He is learning: German (B1 target B2/C1), IT Certifications (CompTIA/Microsoft), Bug Bounty hacking.
His main bad habit: switching between too many resources instead of going deep on one.
Based on today's check-in scores, give a sharp 3-sentence analysis. Be honest, direct, like a mentor. Identify the weakest dimension and give ONE specific action to improve it in the next session. No fluff."""

    scores_text = "\n".join([f"{DIMENSIONS[k]['name']}: {v}/5" for k, v in scores.items()])
    
    try:
        feedback = ask_gemini(system_prompt, f"Subject: {subject}\nScores:\n{scores_text}\nOverall: {overall}/5")
    except Exception as e:
        feedback = f"Could not generate AI feedback: {str(e)}"

    log_to_notion({
        "subject": subject,
        "deep_processing": scores.get("deep_processing", 0),
        "self_regulation": scores.get("self_regulation", 0),
        "mindset": scores.get("mindset", 0),
        "retrieval": scores.get("retrieval", 0),
        "self_management": scores.get("self_management", 0),
        "overall": overall,
        "feedback": feedback,
        "focus": tip
    })

    await message.reply_text(
        f"✅ *Check-in complete — {subject}*\n\n"
        f"{score_summary}\n\n"
        f"📊 Overall: *{overall}/5*\n\n"
        f"🔍 *Analysis:*\n{feedback}\n\n"
        f"🎯 *Focus for next session:*\n_{tip}_\n\n"
        f"📓 Logged to Notion!",
        parse_mode="Markdown"
    )

    if user_id in user_sessions:
        del user_sessions[user_id]

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    session = user_sessions.get(user_id, {})

    if session.get("mode") == "ask":
        history = session.get("history", [])

        system_prompt = """You are a strategic study coach. The student is Saad.
Profile: Sprout learner, Self-regulation 27% (main weakness), Deep processing 67%, Mindset 60% (strong — believes he can be the best).
Goals: German B1→B2, IT Certifications (CompTIA/Microsoft), Bug Bounty hacking.
Bad habit: switches between too many resources, seeks instant reward over deep effort.
Answer his question directly and practically. Reference his specific goals when relevant. Be like a sharp mentor — honest, no fluff. Max 120 words."""

        try:
            response = ask_gemini(system_prompt, text, history)
        except Exception as e:
            response = f"Sorry, could not get a response right now: {str(e)}"

        history.append({"role": "user", "content": text})
        history.append({"role": "assistant", "content": response})
        user_sessions[user_id]["history"] = history[-10:]

        await update.message.reply_text(response)
    else:
        keyboard = [
            [InlineKeyboardButton("📚 Daily check-in", callback_data="checkin")],
            [InlineKeyboardButton("❓ Ask a question", callback_data="ask")]
        ]
        await update.message.reply_text(
            "Use the buttons to get started 👇",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Study Coach Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
