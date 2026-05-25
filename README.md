# study-strategy-monitor
this is telegram bot to track and improve my study strategy and follow the five dimintions 
# Study Coach Bot — Setup Guide

## What this bot does
- Daily check-in across 5 learning dimensions
- AI-powered feedback after every session
- Auto-logs everything to Notion
- Ask study questions anytime — bot knows your profile

## Step 1 — Get your Anthropic API key
1. Go to console.anthropic.com
2. Create an account or log in
3. Go to "API Keys" → Create key
4. Copy it

## Step 2 — Set up Notion database
Follow the instructions in notion_setup.md exactly.

## Step 3 — Deploy on Railway (free)
1. Go to railway.app and sign up with GitHub
2. Click "New Project" → "Deploy from GitHub repo"
3. Upload this folder or connect your GitHub
4. Go to "Variables" and add these 4 environment variables:
   - TELEGRAM_TOKEN = (your telegram token)
   - NOTION_TOKEN = (your notion integration token)
   - NOTION_DB_ID = (your notion database id)
   - ANTHROPIC_KEY = (your anthropic api key)
5. Deploy — done!

## How to use
1. Open Telegram, find your bot
2. Send /start
3. Every day after studying → "Start daily check-in"
4. Answer 5 quick questions (takes 2 minutes)
5. Get AI feedback + tip logged to Notion automatically
6. When stuck on something → "Ask a study question"

## The 5 dimensions tracked
1. Deep Processing — are you thinking or just reading?
2. Self-Regulation — are you adjusting your method?
3. Mindset — how you handle difficulty and mistakes
4. Retrieval — are you testing your memory?
5. Self-Management — focus and environment control
