from psycopg.types.json import Jsonb

def live_channels(cx):
    return cx.execute("SELECT * FROM ad_channels WHERE active ORDER BY code").fetchall()

def dispatch_list(cx):
    return cx.execute("""
      SELECT d.*,c.name FROM ad_dispatches d JOIN ad_channels c ON c.code=d.channel ORDER BY d.id DESC
    """).fetchall()

def set_schedule(cx,week,body,brief,job):
    return cx.execute("""
      INSERT INTO ad_dispatches(week,channel,receipt,release_at,job_id) VALUES (%s,%s,%s,%s,%s)
      ON CONFLICT (week,channel) DO UPDATE SET
        receipt=EXCLUDED.receipt,release_at=EXCLUDED.release_at,job_id=EXCLUDED.job_id,
        status='queued',delivered_at=NULL WHERE ad_dispatches.status='cancelled'
      RETURNING *
    """,(week,body.channel,Jsonb(brief),body.release_at,job)).fetchone()

def cancel(cx, id):
    return cx.execute("""
      UPDATE ad_dispatches SET status='cancelled' WHERE id=%s AND status='queued' RETURNING *
    """,(id,)).fetchone()

def complete(cx, job):
    return cx.execute("""
      UPDATE ad_dispatches SET status='delivered',delivered_at=now()
      WHERE job_id=%s AND status='queued' RETURNING *
    """,(job,)).fetchone()
