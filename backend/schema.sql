CREATE TABLE IF NOT EXISTS ad_films(
    code text PRIMARY KEY, title text NOT NULL, week date NOT NULL,
    CHECK (extract(isodow from week)=1), cut_length int NOT NULL CHECK(cut_length>0)
);
CREATE TABLE IF NOT EXISTS ad_cues(
    code text PRIMARY KEY, film text NOT NULL REFERENCES ad_films(code),
    in_sec int NOT NULL CHECK(in_sec>=0), out_sec int NOT NULL CHECK(out_sec>in_sec),
    cue_text text NOT NULL, weight int NOT NULL CHECK(weight BETWEEN 1 AND 5),
    stage text NOT NULL DEFAULT 'draft' CHECK(stage IN ('draft','recorded','checked')),
    UNIQUE(film,in_sec)
);
CREATE TABLE IF NOT EXISTS ad_reviews(
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY, cue text NOT NULL REFERENCES ad_cues(code),
    result text NOT NULL CHECK(result IN ('approve','redo')), note text NOT NULL,
    reviewer text NOT NULL REFERENCES app_users(email), created timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS ad_channels(
    code text PRIMARY KEY, name text NOT NULL, active boolean NOT NULL DEFAULT true
);
CREATE TABLE IF NOT EXISTS ad_dispatches(
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY, week date NOT NULL,
    channel text NOT NULL REFERENCES ad_channels(code), receipt jsonb NOT NULL,
    release_at timestamptz NOT NULL, status text NOT NULL DEFAULT 'queued'
      CHECK(status IN ('queued','paused','delivered','cancelled')),
    job_id bigint NOT NULL REFERENCES app_jobs(id), delivered_at timestamptz,
    paused_at timestamptz, paused_cue text REFERENCES ad_cues(code),
    cue_stages jsonb NOT NULL DEFAULT '{}'::jsonb,
    UNIQUE(week,channel), CHECK ((status='delivered')=(delivered_at IS NOT NULL))
);

-- 旧库升级：新增「因返录暂停」状态与排期快照的口述点状态。
ALTER TABLE ad_dispatches DROP CONSTRAINT IF EXISTS ad_dispatches_status_check;
ALTER TABLE ad_dispatches ADD CONSTRAINT ad_dispatches_status_check
    CHECK(status IN ('queued','paused','delivered','cancelled'));
ALTER TABLE ad_dispatches ADD COLUMN IF NOT EXISTS paused_at timestamptz;
ALTER TABLE ad_dispatches ADD COLUMN IF NOT EXISTS paused_cue text REFERENCES ad_cues(code);
ALTER TABLE ad_dispatches ADD COLUMN IF NOT EXISTS cue_stages jsonb NOT NULL DEFAULT '{}'::jsonb;
ALTER TABLE ad_dispatches DROP CONSTRAINT IF EXISTS ad_dispatches_paused_check;
ALTER TABLE ad_dispatches ADD CONSTRAINT ad_dispatches_paused_check
    CHECK ((status='paused')=(paused_at IS NOT NULL));
