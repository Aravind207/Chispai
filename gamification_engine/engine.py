"""
Chispai Gamification Engine
Core logic: points, streaks, combos, Wabi-Sabi grace, Zen Garden unlocks.
"""

from dataclasses import dataclass, field
from datetime import date
from typing import Optional

HABIT_POINTS: dict[str, int] = {
    "water":    20,
    "vitamins": 15,
    "gym":      50,
    "protein":  20,
    "reading":  30,
}

STREAK_MULTIPLIER_PER_DAY = 1.1
MAX_MULTIPLIER = 2.0
COMBO_THRESHOLD = 3
COMBO_BONUS = 25

ZEN_UNLOCKS: list[tuple[int, str]] = [
    (100,  "Bonsai sprout appears"),
    (250,  "Water ripples bloom"),
    (500,  "Cherry blossoms open"),
    (1000, "Zen Temple fully awakened"),
]


@dataclass
class UserState:
    total_points: float = 0.0
    streak_days: int = 0
    consecutive_misses: int = 0
    last_active_date: Optional[date] = None
    unlocked_rewards: list = field(default_factory=list)


def calculate_multiplier(streak_days: int) -> float:
    """1.1x per streak day, capped at 2x."""
    raw = 1.0 + (streak_days * (STREAK_MULTIPLIER_PER_DAY - 1.0))
    return round(min(raw, MAX_MULTIPLIER), 2)


def log_day(state: UserState, completed_habits: list[str], today: date) -> dict:
    """
    Process one day of habit logging.

    Args:
        state:             UserState object — mutated in place.
        completed_habits:  List of habit keys completed today.
        today:             Date being logged.

    Returns:
        Dict with full breakdown: base pts, combo, multiplier, streak info,
        Wabi-Sabi status, and any new Zen Garden unlocks.
    """
    result = {
        "date": str(today),
        "habits_completed": completed_habits,
        "base_points": 0,
        "combo_bonus": 0,
        "multiplier": 1.0,
        "total_earned": 0.0,
        "streak_days": state.streak_days,
        "consecutive_misses": state.consecutive_misses,
        "new_unlocks": [],
        "wabi_sabi_grace": False,
        "streak_reset": False,
    }

    if completed_habits:
        state.consecutive_misses = 0
        state.streak_days += 1
        state.last_active_date = today

        base = sum(HABIT_POINTS.get(h, 0) for h in completed_habits)
        combo = COMBO_BONUS if len(completed_habits) >= COMBO_THRESHOLD else 0
        multiplier = calculate_multiplier(state.streak_days)
        total = round((base + combo) * multiplier, 1)

        state.total_points += total

        result.update({
            "base_points": base,
            "combo_bonus": combo,
            "multiplier": multiplier,
            "total_earned": total,
            "streak_days": state.streak_days,
            "consecutive_misses": 0,
        })

    else:
        state.consecutive_misses += 1
        if state.consecutive_misses == 1:
            result["wabi_sabi_grace"] = True
        else:
            state.streak_days = 0
            result["streak_reset"] = True

        result["streak_days"] = state.streak_days
        result["consecutive_misses"] = state.consecutive_misses

    previously_unlocked = set(state.unlocked_rewards)
    for threshold, reward in ZEN_UNLOCKS:
        if state.total_points >= threshold and reward not in previously_unlocked:
            state.unlocked_rewards.append(reward)
            result["new_unlocks"].append(reward)

    return result


def get_garden_stage(total_points: float) -> str:
    stage = "Empty garden — begin your journey"
    for threshold, reward in ZEN_UNLOCKS:
        if total_points >= threshold:
            stage = reward
    return stage


def summary(state: UserState) -> dict:
    return {
        "total_points": round(state.total_points, 1),
        "streak_days": state.streak_days,
        "consecutive_misses": state.consecutive_misses,
        "current_multiplier": calculate_multiplier(state.streak_days),
        "garden_stage": get_garden_stage(state.total_points),
        "unlocked_rewards": state.unlocked_rewards,
    }
