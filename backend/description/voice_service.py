from fastapi import HTTPException
from description.cut_store import get_cue,require_film
from description.voice_store import event,finalize,record
from description.week_service import lock_week

def locked_cue(cx,code):
    prior=get_cue(cx,code)
    lock_week(cx,require_film(cx,prior["film"])["week"])
    return get_cue(cx,code)

def submit(cx, code, body):
    locked_cue(cx,code)
    row=record(cx,code,body.cue_text)
    if not row:
        raise HTTPException(409,"只允许为待录制的口述点提交录音")
    return row

def check(cx, code, body, reviewer):
    cue=locked_cue(cx,code)
    if cue["stage"]!="recorded":
        raise HTTPException(409,"需要录制后才能听审")
    stage="checked" if body.result=="approve" else "draft"
    return {"cue":finalize(cx,code,stage),"review":event(cx,code,body,reviewer)}
