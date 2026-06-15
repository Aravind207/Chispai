# Chispai — AI Wellness Gamification Engine

> Your AI-powered wellness companion that gamifies daily habits and grows your Zen Garden — built for the Microsoft Agents League Hackathon.

---

## Screenshots

### Starting State
![Chispai UI](screenshots/screenshot1.png)

### In Action — Natural Language + Azure Response
![Chispai in action](screenshots/screenshot2.png)

---

## What It Does

Chispai's gamification layer turns daily habits into a living, evolving Zen Garden. Users type naturally ("I did 30 mins of gymming and read books") and the AI extracts habits, calls an Azure Function for points calculation, and responds with a warm zen message.

---

## Architecture

```
User types in UI
      ↓
Habit extraction (NLP in browser)
      ↓
Azure Function /api/log
      ↓
Gamification engine (points, streaks, combos)
      ↓
Zen Garden updates + response
```

---

## Project Structure

```
chispai/
├── gamification_engine/
│   ├── function_app.py  ← Azure Function HTTP triggers
│   ├── engine.py        ← Core gamification logic
│   ├── host.json        ← Azure Function config
│   └── requirements.txt
├── ui/
│   └── chispai_final.html  ← Demo UI (chat + Azure calls)
├── screenshots/
│   ├── screenshot1.png
│   └── screenshot2.png
└── README.md
```

---

## Gamification Rules

| Habit    | Points |
|----------|--------|
| Water    | 20     |
| Vitamins | 15     |
| Gym      | 50     |
| Protein  | 20     |
| Reading  | 30     |

- **Streak multiplier**: ×1.1 per day, capped at ×2.0
- **Combo bonus**: +25 pts when 3+ habits completed in one day
- **Wabi-Sabi grace**: 1 miss = streak preserved. 2 consecutive misses = streak reset.
- **Zen Garden unlocks**: 100 / 250 / 500 / 1000 pts

---

## Live Endpoints

```
POST https://chispai-gamification.azurewebsites.net/api/log
POST https://chispai-gamification.azurewebsites.net/api/summary
```

### POST /api/log — Example

**Request:**
```json
{
  "state": null,
  "completed_habits": ["water", "gym", "reading"],
  "today": "2026-06-14"
}
```

**Response:**
```json
{
  "result": {
    "date": "2026-06-14",
    "habits_completed": ["water", "gym", "reading"],
    "base_points": 100,
    "combo_bonus": 25,
    "multiplier": 1.1,
    "total_earned": 137.5,
    "streak_days": 1,
    "new_unlocks": ["Bonsai sprout appears"],
    "wabi_sabi_grace": false,
    "streak_reset": false
  },
  "state": {
    "total_points": 137.5,
    "streak_days": 1,
    "current_multiplier": 1.1,
    "garden_stage": "Bonsai sprout appears",
    "unlocked_rewards": ["Bonsai sprout appears"]
  }
}
```

---

## Deploy to Azure

```bash
az login
az group create --name chispai-rg --location eastus
az storage account create --name chispaistorage --location eastus --resource-group chispai-rg --sku Standard_LRS
az functionapp create --resource-group chispai-rg --consumption-plan-location eastus --runtime python --runtime-version 3.11 --functions-version 4 --name chispai-gamification --storage-account chispaistorage --os-type linux
cd gamification_engine
func azure functionapp publish chispai-gamification --python
```

---

## Azure AI Foundry Agent

The gamification engine is also connected to an Azure AI Foundry agent. The agent understands natural language habit logging and automatically calls the Azure Function as a tool, returning warm zen responses.

Built with: Azure Functions · Azure AI Foundry · Python 3.11 · Microsoft Agents League Hackathon 2026


