def seed(cx):
    cx.execute("""
      INSERT INTO ad_films VALUES ('CUT-401','候鸟过桥','2026-11-23',780),
       ('CUT-402','纸船送信','2026-11-23',610) ON CONFLICT DO NOTHING;
      INSERT INTO ad_channels VALUES ('MIX','混录交付组',true),('ACCESS','放映无障碍联络组',true),
       ('OLD','停用审片组',false) ON CONFLICT DO NOTHING;
      INSERT INTO ad_cues VALUES
       ('CUE-11','CUT-401',31,39,'车窗映出一座空桥',4,'checked'),
       ('CUE-12','CUT-401',128,140,'芦苇划过船舷',3,'recorded'),
       ('CUE-13','CUT-401',390,408,'白鸟落到警示牌上',2,'draft'),
       ('CUE-14','CUT-402',42,58,'小孩把作业纸折成纸船',5,'recorded'),
       ('CUE-15','CUT-402',602,609,'河岸上出现一排灯',1,'checked') ON CONFLICT DO NOTHING;
    """)
