from collections import defaultdict
from fastapi import HTTPException
from description.projection import lower_case_rate
from description.weekly_store import weekly_films,weekly_cues

def lock_week(cx, week):
    if week.weekday()!=0:
        raise HTTPException(422,"请选择周一作为报告周起点")
    cx.execute("SELECT pg_advisory_xact_lock(1941,%s)",(week.toordinal(),))

def calculate(cx,week):
    lock_week(cx,week)
    films=weekly_films(cx,week)
    cues=weekly_cues(cx,week)
    grouped=defaultdict(list)
    for row in cues:
        grouped[row["film"]].append(row)
    return {"films":[film | lower_case_rate(grouped[film["code"]]) for film in films],
            "summary":lower_case_rate(cues)}

def stage_snapshot(cx,week):
    """Frozen per-cue stages recorded alongside a scheduled report."""
    return {row["code"]:row["stage"] for row in weekly_cues(cx,week)}
