from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from core import enqueue
from description.channel_store import complete,live_channels,set_schedule
from description.week_service import calculate

def schedule(cx, week, body):
    report=calculate(cx,week)
    if not report["summary"]["total"]:
        raise HTTPException(409,"此周尚无可分发的口述素材")
    if not any(row["code"]==body.channel for row in live_channels(cx)):
        raise HTTPException(409,"该交接组未启用")
    job=enqueue(cx,"description-weekly",{"channel":body.channel,"week":str(week)},available_at=body.release_at)
    item=set_schedule(cx,week,body,jsonable_encoder(report),job)
    if not item:
        raise HTTPException(409,"此周已安排该接收组")
    return item

def deliver(cx,payload):
    # The worker locks its row before invoking the domain handler.
    job=cx.execute("""
      SELECT id FROM app_jobs WHERE kind='description-weekly' AND status='running'
      AND payload->>'channel'=%s AND payload->>'week'=%s ORDER BY id LIMIT 1
    """,(payload["channel"],payload["week"])).fetchone()
    release=complete(cx,job["id"])
    if release is None:
        return {"cancelled":True}
    return {"internal_inbox":release["channel"],"snapshot":release["receipt"]["summary"],"dispatch_id":release["id"]}
