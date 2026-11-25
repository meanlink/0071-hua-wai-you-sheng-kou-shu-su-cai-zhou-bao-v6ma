from fastapi import HTTPException
from description.channel_store import pause_week
from description.cut_store import get_cue,require_film
from description.voice_store import event,finalize,record
from description.week_service import lock_week

def locked_cue(cx,code):
    prior=get_cue(cx,code)
    week=require_film(cx,prior["film"])["week"]
    lock_week(cx,week)
    return get_cue(cx,code),week

def submit(cx, code, body):
    cue,_=locked_cue(cx,code)
    if cue["stage"]!="draft":
        raise HTTPException(409,"只允许为待录制的口述点提交录音")
    row=record(cx,code,body.cue_text)
    if not row:
        raise HTTPException(409,"只允许为待录制的口述点提交录音")
    return row

def check(cx, code, body, reviewer):
    cue,week=locked_cue(cx,code)
    if cue["stage"] not in ("recorded","checked"):
        raise HTTPException(409,"需要录制后才能听审")
    # Approved points may still be sent back for a new take.
    stage="checked" if body.result=="approve" else "draft"
    result={"cue":finalize(cx,code,stage),"review":event(cx,code,body,reviewer)}
    if body.result=="redo":
        # Pause only snapshots that counted this approval; other schedules keep
        # going out with their own frozen input.
        result["paused"]=pause_week(cx,week,code)
    return result
