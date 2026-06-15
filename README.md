# Chispai — Gamification Engine

Habit tracking, streaks, combos, Wabi-Sabi grace, and Zen Garden unlocks.
Built as an Azure Function for the Microsoft Agents League Hackathon.

---

## Project Structure

```
chispai/
├── gamification_engine/
│   ├── __init__.py      ← Azure Function app (HTTP triggers)
│   ├── engine.py        ← Core gamification logic
│   ├── host.json        ← Azure Function config
│   ├── requirements.txt
│   └── test_local.py    ← Local test script
└── ui/
    └── index.html       ← Standalone demo UI
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

- **Streak multiplier**: ×1.1 per day, capped at ×2.0 — applied to total daily score
- **Combo bonus**: +25 pts when 3+ habits completed in one day
- **Wabi-Sabi grace**: 1 miss = streak preserved. 2 consecutive misses = streak reset.
- **Zen Garden unlocks**: 100 / 250 / 500 / 1000 pts

---

## Running Locally

```bash
cd gamification_engine
pip install -r requirements.txt
python test_local.py
```

---

## Deploy to Azure

### Prerequisites
- Azure CLI installed
- Azure Functions Core Tools installed

### Steps

```bash
# 1. Login
az login

# 2. Create a resource group
az group create --name chispai-rg --location eastus

# 3. Create a storage account (required by Azure Functions)
az storage account create \
  --name chispaistorage \
  --location eastus \
  --resource-group chispai-rg \
  --sku Standard_LRS

# 4. Create the Function App
az functionapp create \
  --resource-group chispai-rg \
  --consumption-plan-location eastus \
  --runtime python \
  --runtime-version 3.11 \
  --functions-version 4 \
  --name chispai-gamification \
  --storage-account chispaistorage \
  --os-type linux

# 5. Deploy
cd gamification_engine
func azure functionapp publish chispai-gamification
```

---

## API Endpoints

### POST /api/log
Log a day's habits and get points + streak update.

**Request:**
```json
{
  "state": {
    "total_points": 145.2,
    "streak_days": 3,
    "consecutive_misses": 0,
    "unlocked_rewards": ["Bonsai sprout appears"]
  },
  "completed_habits": ["water", "gym", "reading"],
  "today": "2025-06-14"
}
```

**Response:**
```json
{
  "result": {
    "date": "2025-06-14",
    "habits_completed": ["water", "gym", "reading"],
    "base_points": 100,
    "combo_bonus": 25,
    "multiplier": 1.4,
    "total_earned": 175.0,
    "streak_days": 4,
    "new_unlocks": ["Water ripples bloom"],
    "wabi_sabi_grace": false,
    "streak_reset": false
  },
  "state": {
    "total_points": 320.2,
    "streak_days": 4,
    "current_multiplier": 1.4,
    "garden_stage": "Water ripples bloom",
    "unlocked_rewards": ["Bonsai sprout appears", "Water ripples bloom"]
  }
}
```

### POST /api/summary
Get current garden state without logging a day.

**Request:**
```json
{ "state": { "total_points": 320.2, "streak_days": 4, ... } }
```

---

## Connecting to Copilot Studio

In Copilot Studio, add an HTTP action node pointing to:
```
https://chispai-gamification.azurewebsites.net/api/log
```
Pass the user's state from conversation variables and update it with the response.
For persistence, store state in Azure Cosmos DB keyed by user ID.
