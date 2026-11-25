def weekly_films(cx,week):
    return cx.execute("SELECT * FROM ad_films WHERE week=%s ORDER BY code",(week,)).fetchall()

def weekly_cues(cx,week):
    return cx.execute("""
      SELECT c.* FROM ad_cues c JOIN ad_films f ON f.code=c.film
      WHERE f.week=%s ORDER BY c.film,c.in_sec
    """,(week,)).fetchall()

def films(cx):
    return cx.execute("""
      SELECT f.*,count(c.code) AS cues FROM ad_films f LEFT JOIN ad_cues c ON c.film=f.code
      GROUP BY f.code ORDER BY f.week DESC,f.code
    """).fetchall()
