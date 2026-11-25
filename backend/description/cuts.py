from fastapi import APIRouter,Depends
from core import db,require
from description.cut_store import list_cues
from description.cut_service import register
from description.cue_forms import Cue
from description.weekly_store import films

router=APIRouter(prefix="/api/description")

@router.get("/films")
def list_films(_=Depends(require())):
    with db() as cx: return films(cx)

@router.get("/cues")
def cues(_=Depends(require())):
    with db() as cx: return list_cues(cx)

@router.post("/cues",status_code=201)
def add(body:Cue,_=Depends(require("operator"))):
    with db() as cx: return register(cx,body)
