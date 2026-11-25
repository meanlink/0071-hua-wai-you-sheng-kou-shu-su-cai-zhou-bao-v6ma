from fastapi import HTTPException

def require_film(cx, code):
    row=cx.execute("SELECT * FROM ad_films WHERE code=%s",(code,)).fetchone()
    if not row:
        raise HTTPException(404,"没有该片档")
    return row

def list_cues(cx):
    return cx.execute("SELECT * FROM ad_cues ORDER BY film,in_sec").fetchall()

def get_cue(cx, code):
    row=cx.execute("SELECT * FROM ad_cues WHERE code=%s",(code,)).fetchone()
    if not row:
        raise HTTPException(404,"没有此口述点")
    return row

def insert(cx, body):
    return cx.execute("""
      INSERT INTO ad_cues(code,film,in_sec,out_sec,cue_text,weight)
      VALUES (%(code)s,%(film)s,%(in_sec)s,%(out_sec)s,%(cue_text)s,%(weight)s) RETURNING *
    """,body.model_dump()).fetchone()

def has_overlap(cx, body):
    return cx.execute("""
      SELECT 1 FROM ad_cues WHERE film=%s AND in_sec < %s AND out_sec > %s
    """,(body.film,body.out_sec,body.in_sec)).fetchone() is not None
