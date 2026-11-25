from psycopg.types.json import Jsonb

def live_channels(cx):
    return cx.execute("SELECT * FROM ad_channels WHERE active ORDER BY code").fetchall()

def dispatch_list(cx):
    return cx.execute("""
      SELECT d.*,c.name FROM ad_dispatches d JOIN ad_channels c ON c.code=d.channel ORDER BY d.id DESC
    """).fetchall()

def active_dispatch(cx,week,channel):
    return cx.execute("""
      SELECT * FROM ad_dispatches
      WHERE week=%s AND channel=%s AND status IN ('queued','paused')
    """,(week,channel)).fetchone()

def delivered_dispatch(cx,week,channel):
    return cx.execute("""
      SELECT * FROM ad_dispatches WHERE week=%s AND channel=%s AND status='delivered'
    """,(week,channel)).fetchone()

def set_schedule(cx,week,body,brief,stages,job):
    return cx.execute("""
      INSERT INTO ad_dispatches(week,channel,receipt,cue_stages,release_at,job_id)
      VALUES (%s,%s,%s,%s,%s,%s)
      ON CONFLICT (week,channel) DO UPDATE SET
        receipt=EXCLUDED.receipt,cue_stages=EXCLUDED.cue_stages,
        release_at=EXCLUDED.release_at,job_id=EXCLUDED.job_id,
        status='queued',delivered_at=NULL,paused_at=NULL,paused_cue=NULL
      WHERE ad_dispatches.status='cancelled'
      RETURNING *
    """,(week,body.channel,Jsonb(brief),Jsonb(stages),body.release_at,job)).fetchone()

def rearm(cx,dispatch_id,body,brief,stages,job):
    """Replace a paused snapshot once hearing review has re-run the schedule."""
    return cx.execute("""
      UPDATE ad_dispatches SET receipt=%s,cue_stages=%s,release_at=%s,job_id=%s,
        status='queued',paused_at=NULL,paused_cue=NULL
      WHERE id=%s AND status='paused' RETURNING *
    """,(Jsonb(brief),Jsonb(stages),body.release_at,job,dispatch_id)).fetchone()

def cancel(cx, id):
    return cx.execute("""
      UPDATE ad_dispatches SET status='cancelled',paused_at=NULL,paused_cue=NULL
      WHERE id=%s AND status IN ('queued','paused') RETURNING *
    """,(id,)).fetchone()

def pause_week(cx, week, cue):
    """A redo pauses only pending snapshots that counted this approval.

    Other schedules for the week keep their frozen input and deliver normally.
    Rows scheduled before snapshots were recorded have no per-cue stage, so
    they are paused too rather than risking a stale report.
    """
    return cx.execute("""
      UPDATE ad_dispatches SET status='paused',paused_at=now(),paused_cue=%s
      WHERE week=%s AND status='queued'
        AND (cue_stages->>%s='checked' OR NOT (cue_stages ? %s)) RETURNING *
    """,(cue,week,cue,cue)).fetchall()

def complete(cx, job):
    return cx.execute("""
      UPDATE ad_dispatches SET status='delivered',delivered_at=now()
      WHERE job_id=%s AND status='queued' RETURNING *
    """,(job,)).fetchone()
