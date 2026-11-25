from datetime import date
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from core import enqueue
from description.channel_store import active_dispatch,complete,delivered_dispatch,live_channels,rearm,set_schedule
from description.week_service import calculate,lock_week,stage_snapshot

def schedule(cx, week, body):
    report=calculate(cx,week)
    if not report["summary"]["total"]:
        raise HTTPException(409,"此周尚无可分发的口述素材")
    if not any(row["code"]==body.channel for row in live_channels(cx)):
        raise HTTPException(409,"该交接组未启用")
    existing=active_dispatch(cx,week,body.channel)
    if existing and existing["status"]=="queued":
        raise HTTPException(409,"此周已安排该接收组，可先撤回排期后重排")
    if not existing and delivered_dispatch(cx,week,body.channel):
        raise HTTPException(409,"此周周报已送达，请保留原件与回执，无法重排")
    stages=stage_snapshot(cx,week)
    job=enqueue(cx,"description-weekly",{"channel":body.channel,"week":str(week)},available_at=body.release_at)
    if existing:
        # A snapshot paused by a redo may only go out again after hearing
        # review re-runs this schedule, which rebuilds the frozen report.
        return rearm(cx,existing["id"],body,jsonable_encoder(report),stages,job)
    item=set_schedule(cx,week,body,jsonable_encoder(report),stages,job)
    if not item:
        raise HTTPException(409,"此周已安排该接收组，可先撤回排期后重排")
    return item

def deliver(cx,payload,job_id=None):
    if job_id is None:
        raise ValueError("投递任务缺少作业编号")
    week=date.fromisoformat(payload["week"])
    # Serialize with re-recording so a redo that lands first pauses this
    # report instead of letting the stale snapshot reach the inbox.
    lock_week(cx,week)
    # Identity comes from the job itself, never from a channel/week lookup:
    # a stale retry must not consume a later schedule for the same slot.
    release=complete(cx,job_id)
    if release is None:
        return {"cancelled":True}
    return {"internal_inbox":release["channel"],"snapshot":release["receipt"]["summary"],"dispatch_id":release["id"]}
