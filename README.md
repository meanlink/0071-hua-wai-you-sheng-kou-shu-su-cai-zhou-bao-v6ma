# 画外有声 · 口述素材周报

灯箱无障碍制片组共有 6 名编导和口述录制、听审人员，为社区短片放映补齐口述轨。剪辑带时间码提供版次，编导在表格中记口述难度，听审组在邮件里退回录音。过去同一空隙被两个脚本占用，返录段被继续计入已录，计划时与实际收到的报告分数不一致。工作台把剪辑带、听审事件和定时收件连接起来，把周报交给后期混录与放映联络组。

| 角色 | 工作任务 |
|---|---|
| operator | 定口述点和权重、提交录音稿 |
| reviewer | 听审后通过或返录；排期和撤回 |
| viewer | 查阅当前进度、分发冻结件和回执 |

1. 周一 09:00 在剪辑带选 CUT-401《候鸟过桥》780 秒切片。
2. 09:20 核对 CUE-12（128—140 秒），同窗禁止加入第二条口述。
3. 10:45 听审 CUE-12 的权重 3 条目，返录并保存批注。
4. 11:10 更新口述稿并提交录制，随后听审通过。
5. 11:30 查看周报两部短片总权重 15，已得 10.5。
6. 13:30 设置 ACCESS 收件组的投递计划。停用的 OLD 组无法设置。
7. 14:00 worker 将冻结周报写入站内收件箱，归档实际投递时间。

正式权重为口述难度 1 到 5。待录制系数 0，录制待审系数 0.5，听审通过系数 1。以已得权重除以总权重，空分母保持为空。周一为周起点。定时分发保留排期时的输入快照，同一周同一组已投递后无法重排；待投递可以撤回重排。此原型使用录音稿登记及站内收件箱。

```sh
cp -n .env.example .env
docker compose up -d --build --wait
docker compose exec backend python -m scripts.seed_demo
docker compose down -v --remove-orphans
```

FRONTEND_PORT 为前端、BACKEND_PORT 为 API、DB_PORT 为 PostgreSQL。三个演示账号 operator@demo.local、reviewer@demo.local、viewer@demo.local 使用默认密码 Demo2026!。SEED_DEMO 控制自动填充，JWT_SECRET、POSTGRES_PASSWORD、DEMO_PASSWORD 控制本机身份与数据库。五服务使用 Nginx/原生 ES modules、Python/FastAPI、PostgreSQL、Redis 和 worker。后端本地开发安装 backend/requirements.txt，配置 DATABASE_URL、REDIS_URL、JWT_SECRET，启动 `uvicorn app:app --reload` 与 `python worker.py`。backend/description 存放版次、听审、排期逻辑，frontend/studio 是工作台。角色/任务枚举在 backend/core.py 与 frontend/base.js；口述和投递枚举在 backend/schema.sql、backend/description/cue_forms.py、frontend/studio/timing.js。MIT 许可证。

前端地址为 http://127.0.0.1:18465，API 为 http://127.0.0.1:19465，数据库本机映射端口为 17965。
