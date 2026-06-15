import azure.functions as func
import json
from engine import log_day, summary, UserState
from datetime import date

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.route(route="log", methods=["POST"])
def log_habits(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON", status_code=400)

    raw = body.get("state") or {}
    state = UserState(
        total_points=raw.get("total_points", 0.0),
        streak_days=raw.get("streak_days", 0),
        consecutive_misses=raw.get("consecutive_misses", 0),
        unlocked_rewards=raw.get("unlocked_rewards", []),
    )

    completed_habits = body.get("completed_habits", [])
    today_str = body.get("today")
    today = date.fromisoformat(today_str) if today_str else date.today()

    result = log_day(state, completed_habits, today)
    state_out = summary(state)

    return func.HttpResponse(
        json.dumps({"result": result, "state": state_out}),
        mimetype="application/json",
        status_code=200,
    )


@app.route(route="summary", methods=["POST"])
def get_summary(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON", status_code=400)

    raw = body.get("state") or {}
    state = UserState(
        total_points=raw.get("total_points", 0.0),
        streak_days=raw.get("streak_days", 0),
        consecutive_misses=raw.get("consecutive_misses", 0),
        unlocked_rewards=raw.get("unlocked_rewards", []),
    )

    return func.HttpResponse(
        json.dumps(summary(state)),
        mimetype="application/json",
        status_code=200,
    )
