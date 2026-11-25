from fastapi import HTTPException
from description.cut_store import insert,has_overlap,require_film
from description.week_service import lock_week

def register(cx, body):
    film=require_film(cx,body.film)
    lock_week(cx,film["week"])
    if body.out_sec > film["cut_length"]:
        raise HTTPException(409,"出点超过当前剪辑版长度")
    if has_overlap(cx,body):
        raise HTTPException(409,"口述点与现有口述时窗重叠")
    return insert(cx,body)
