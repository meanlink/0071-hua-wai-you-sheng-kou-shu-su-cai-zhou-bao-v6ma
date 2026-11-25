from fastapi import APIRouter,Depends
from core import db,require
from description.cue_forms import Recording,Review
from description.voice_service import check,submit
from description.voice_store import events

router=APIRouter(prefix="/api/description")

@router.post("/cues/{code}/record")
def record(code:str, body:Recording,_=Depends(require("operator"))):
    with db() as cx: return submit(cx,code,body)

@router.post("/cues/{code}/hear")
def hear(code:str, body:Review,user=Depends(require("reviewer"))):
    with db() as cx: return check(cx,code,body,user["email"])

@router.get("/hearings")
def hearings(_=Depends(require())):
    with db() as cx: return events(cx)
