import json
import os

SCORES_FILE = "scores.json"
MAX_SCORES = 10


def load_scores():
    if not os.path.exists(SCORES_FILE):
        return []
    try:
        with open(SCORES_FILE, "r") as f:
            scores = json.load(f)
        return sorted(scores, key=lambda x: x["score"], reverse=True)[:MAX_SCORES]
    except (json.JSONDecodeError, KeyError):
        return []


def save_score(name, score):
    scores = load_all_scores()
    scores.append({"name": name.upper(), "score": score})
    scores = sorted(scores, key=lambda x: x["score"], reverse=True)
    with open(SCORES_FILE, "w") as f:
        json.dump(scores, f, indent=2)


def load_all_scores():
    if not os.path.exists(SCORES_FILE):
        return []
    try:
        with open(SCORES_FILE, "r") as f:
            scores = json.load(f)
        return sorted(scores, key=lambda x: x["score"], reverse=True)
    except (json.JSONDecodeError, KeyError):
        return []


def get_top_scores():
    return load_scores()


def get_total_scores():
    if not os.path.exists(SCORES_FILE):
        return 0
    try:
        with open(SCORES_FILE, "r") as f:
            scores = json.load(f)
        return len(scores)
    except (json.JSONDecodeError, KeyError):
        return 0
