def record(cx,code,text):
    return cx.execute("""
      UPDATE ad_cues SET cue_text=%s,stage='recorded' WHERE code=%s AND stage='draft' RETURNING *
    """,(text,code)).fetchone()

def finalize(cx,code,stage):
    return cx.execute("UPDATE ad_cues SET stage=%s WHERE code=%s RETURNING *",(stage,code)).fetchone()

def event(cx, code, body, reviewer):
    return cx.execute("""
      INSERT INTO ad_reviews(cue,result,note,reviewer) VALUES (%s,%s,%s,%s) RETURNING *
    """,(code,body.result,body.note,reviewer)).fetchone()

def events(cx):
    return cx.execute("SELECT * FROM ad_reviews ORDER BY id DESC").fetchall()
