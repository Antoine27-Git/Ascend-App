import json
def state(manques=None, extra_sessions=None, theme='light', daily=None):
    profile = {
        "name": "Antoine", "weight": 91, "goalName": "Objectif Perso 80kms", "goalDate": "2027-09-25",
        "goalDist": 80, "goalDplus": 4500, "planStart": "2026-09-21", "introSeen": True, "onboarded": True,
        "stMode": "libre", "theme": theme,
        "modules": {"nutrition": True, "strength": True, "injury": False},
        "days": {"run": [3, 0], "long": 0, "cf": [2, 5], "time": {}},
        "orgs": [{"from": "F3", "enchaine": True, "days": {"run": [3, 6, 0], "long": 0, "cf": [2]}}],
        "terrain": {"climb": None, "mountain": None, "dplusMax": 900},
        "start": {"lastLong": {"date": "2026-09-06", "dur": 107, "dist": 12, "dplus": 500}, "pastRaces": [],
                  "freq4w": 1, "dur4w": 45, "pauseSince": None, "beforeFreq": None, "beforeDur": None,
                  "lastGoal": {"date": "2025-09-20", "dur": 390, "dist": 42, "dplus": 1300}},
        "races": [{"name": "Trail des coursières 2027", "date": "2027-05-08", "dist": 50, "dplus": 2000, "prio": "B"}],
        "shoes": [], "carbStart": 15, "fluidTarget": 800, "nutriTier": "none", "fluidTier": "high",
        "manques": manques if manques is not None else {"2026-10-07": "autre", "2026-10-11": "autre"},
    }
    sessions = [
        {"id": "s1", "date": "2026-09-27", "type": "long", "dur": 30, "rpe": 2, "dist": 4, "dplus": 60},
        {"id": "s2", "date": "2026-09-29", "type": "cf", "dur": 30, "rpe": 5, "cfJ": "peu"},
        {"id": "s3", "date": "2026-10-02", "type": "cf", "dur": 30, "rpe": 6, "cfJ": "peu"},
        {"id": "s4", "date": "2026-10-07", "type": "cf", "dur": 30, "rpe": 5, "cfJ": "peu"},
        {"id": "s5", "date": "2026-10-09", "type": "cf", "dur": 30, "rpe": 8, "cfJ": "fort"},
    ] + (extra_sessions or [])
    return {"v": 2, "profile": profile, "daily": daily or {}, "sessions": sessions, "plan": []}
AUTH = {"access_token": "x", "refresh_token": "y", "user": {"id": "u1", "email": "a@b.c"}, "expires_at": 9999999999999, "email": "a@b.c", "user_id": "u1"}
