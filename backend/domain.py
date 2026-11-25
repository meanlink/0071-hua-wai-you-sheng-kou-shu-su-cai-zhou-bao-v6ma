from fastapi import APIRouter
from description import cuts,voice_routes,dispatch_routes
from description.demo import seed
from description.dispatch_service import deliver

router=APIRouter()
for segment in (cuts,voice_routes,dispatch_routes):
    router.include_router(segment.router)

def run_job(cx,kind,payload,job_id=None):
    if kind=="description-weekly":
        return deliver(cx,payload,job_id)
    raise ValueError(f"Unknown audio description task {kind}")
