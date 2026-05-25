import requests
import datetime

NOTION_TOKEN = input("Notion token (secret_...): ").strip()
NOTION_DB_ID = input("Database ID: ").strip()

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

print("\nChecking existing database...")

# First get existing properties
r = requests.get(f"https://api.notion.com/v1/databases/{NOTION_DB_ID}", headers=headers)
if r.status_code != 200:
    print(f"❌ Cannot access database: {r.text}")
    exit()

existing = list(r.json()["properties"].keys())
print(f"Existing columns: {existing}")

# Only add properties that don't exist yet
new_props = {}

if "Date" not in existing:
    new_props["Date"] = {"date": {}}
if "Subject" not in existing:
    new_props["Subject"] = {"select": {"options": [
        {"name": "🇩🇪 German", "color": "blue"},
        {"name": "💻 IT Cert", "color": "green"},
        {"name": "🐛 Bug Bounty", "color": "red"}
    ]}}
if "Overall Score" not in existing:
    new_props["Overall Score"] = {"number": {"format": "number"}}
if "Deep Processing" not in existing:
    new_props["Deep Processing"] = {"number": {"format": "number"}}
if "Self-Regulation" not in existing:
    new_props["Self-Regulation"] = {"number": {"format": "number"}}
if "Mindset" not in existing:
    new_props["Mindset"] = {"number": {"format": "number"}}
if "Retrieval" not in existing:
    new_props["Retrieval"] = {"number": {"format": "number"}}
if "Self-Management" not in existing:
    new_props["Self-Management"] = {"number": {"format": "number"}}
if "Session Quality" not in existing:
    new_props["Session Quality"] = {"select": {"options": [
        {"name": "🔥 Excellent", "color": "green"},
        {"name": "✅ Good", "color": "blue"},
        {"name": "⚠️ Average", "color": "yellow"},
        {"name": "❌ Poor", "color": "red"}
    ]}}
if "Weakest Dimension" not in existing:
    new_props["Weakest Dimension"] = {"select": {"options": [
        {"name": "🧠 Deep Processing", "color": "purple"},
        {"name": "⚙️ Self-Regulation", "color": "orange"},
        {"name": "💭 Mindset", "color": "pink"},
        {"name": "🔁 Retrieval", "color": "yellow"},
        {"name": "🎯 Self-Management", "color": "red"}
    ]}}
if "AI Feedback" not in existing:
    new_props["AI Feedback"] = {"rich_text": {}}
if "Improvement Focus" not in existing:
    new_props["Improvement Focus"] = {"rich_text": {}}
if "Week Number" not in existing:
    new_props["Week Number"] = {"number": {"format": "number"}}

if new_props:
    r2 = requests.patch(
        f"https://api.notion.com/v1/databases/{NOTION_DB_ID}",
        headers=headers,
        json={"properties": new_props}
    )
    if r2.status_code == 200:
        print(f"✅ Added {len(new_props)} new columns!")
    else:
        print(f"❌ Error: {r2.status_code} — {r2.text}")
        exit()
else:
    print("✅ All columns already exist!")

# Add sample entry
today = datetime.date.today()
sample = {
    "parent": {"database_id": NOTION_DB_ID},
    "properties": {
        "Name": {"title": [{"text": {"content": f"🇩🇪 German — {today.strftime('%d %b %Y')}"}}]},
        "Date": {"date": {"start": today.isoformat()}},
        "Subject": {"select": {"name": "🇩🇪 German"}},
        "Overall Score": {"number": 3.4},
        "Deep Processing": {"number": 4},
        "Self-Regulation": {"number": 2},
        "Mindset": {"number": 4},
        "Retrieval": {"number": 3},
        "Self-Management": {"number": 4},
        "Session Quality": {"select": {"name": "⚠️ Average"}},
        "Weakest Dimension": {"select": {"name": "⚙️ Self-Regulation"}},
        "AI Feedback": {"rich_text": [{"text": {"content": "Good mindset and deep processing today. Self-regulation is still your main blocker. Next session: set a clear goal before starting and check it at the end."}}]},
        "Improvement Focus": {"rich_text": [{"text": {"content": "Set a 20-min timer. When it rings ask: am I going deep or just reading? If shallow — close everything and write what you remember."}}]},
        "Week Number": {"number": today.isocalendar()[1]}
    }
}

r3 = requests.post("https://api.notion.com/v1/pages", headers=headers, json=sample)
if r3.status_code == 200:
    print("✅ Sample entry added!")
else:
    print(f"⚠️ Sample entry error: {r3.status_code} — {r3.text}")

print("\n🎉 Done! Open Notion and check your database.")
