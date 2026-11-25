from datetime import date
from fastapi import APIRouter,Depends,HTTPException
from core import db,require
from description.dispatch_form import Dispatch
from description.channel_store import cancel,dispatch_list,live_channels
from description.dispatch_service import schedule
from description.week_service import calculate

router=APIRouter(prefix="/api/description")

@router.get("/weeks/{week}")
def week_view(week:date,_=Depends(require())):
    with db() as cx: return calculate(cx,week)

@router.get("/channels")
def channels(_=Depends(require())):
    with db() as cx: return live_channels(cx)

@router.get("/dispatches")
def releases(_=Depends(require())):
    with db() as cx: return dispatch_list(cx)

@router.post("/weeks/{week}/dispatch",status_code=201)
def prepare(week:date,body:Dispatch,_=Depends(require("reviewer"))):
    with db() as cx: return schedule(cx,week,body)

@router.post("/dispatches/{dispatch_id}/cancel")
def recall(dispatch_id:int,_=Depends(require("reviewer"))):
    with db() as cx:
        row=cancel(cx,dispatch_id)
        if not row:
            raise HTTPException(409,"只能取消还在待分发状态的周报")
        return row
