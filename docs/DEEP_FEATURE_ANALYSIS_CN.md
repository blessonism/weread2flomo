# WeRead2Flomo 功能深度分析与优化路线（产品经理视角）

本文件从“功能本质”与“系统化价值闭环”出发，提出 WeRead2Flomo 的优化方向与新功能建议，并给出可落地的工程方案。目标不是堆砌功能，而是把“零散划线”稳定地转化为“可复用的知识资产”，并形成长期复利的学习与输出闭环。

——

一、产品使命与北极星
- 使命：将阅读划线转化为可复用、可检索、可复盘的知识资产，且过程足够稳定、低摩擦、可解释。
- 北极星指标：高价值划线转化为有效笔记的占比（High-Value Highlights → Useful Notes Conversion Rate）。
- 价值闭环：采集 → 选择 → 加工 → 输出 → 复盘 → 迭代；每一环均要有反馈与学习。

二、用户与 JTBD
- 知识工作者：将书摘转为洞见与行动，关注质量、分类与可复用性。
- 信息收集者：快速处理大量片段，关注筛选效率与噪音控制。
- 学习者：组织知识点与复习卡片，关注结构化与复盘。
- JTBD 本质：在低负担下完成“组织、提炼、沉淀、复用”。

三、现状与根本痛点
- 现状：拉取 WeRead → 去重与筛选 → 模板渲染 → 发往 Flomo；支持可选 AI 标签与摘要；以 JSON 维护去重状态，可按时间与数量限制；支持 GitHub Actions 定时。
- 痛点：
  - 选择环节弱：按时间与数量，不足以凸显“重要性”，质量波动大。
  - 标签体系不稳：AI 标签漂移，与用户既有体系不一致，导致检索困难。
  - 去重脆弱：只基于 ID，文本微调或重复主题容易漏检。
  - 过程不可见：无“干跑预览”，用户缺乏信心与纠错路径。
  - 复盘缺失：缺乏长期质量反馈，不能主动学习和调参。
  - 单一通路：只支持 WeRead→Flomo，难以扩展到 Obsidian/Notion/Anki 等生态。

四、系统性优化方向（采集-选择-加工-输出-复盘）
1) 采集（Source）
- 多源标准化接口：定义 ContentSource 协议，WeRead 作为一个实现；统一数据模型（highlight_id、book_id、chapter、text、note、created_at、source、fingerprint）。
- 指纹与增量：基于归一化文本与元信息生成稳定指纹，结合 last_updated_at 增量拉取，降低重复与请求成本。

2) 选择（Selection）
- 重要性评分：文本长度与密度、是否有备注、书内位置、历史互动、时间衰减、书籍权重、重复主题惩罚；输出可解释的 Top-K。
- Backlog 智能补全：对历史积压按“评分+多样性”抽样补齐，限流节奏。

3) 加工（Processing）
- 模板条件化与宏：按分类/来源切换模板，支持条件、循环与宏片段，风格参数化（tone、length），模板 DSL 或 Jinja2 风格。
- 标签稳态化：词典与同义词归一、黑白名单、层级标签；AI 建议仅在低置信度时触发；回收用户修正形成规则库（主动学习）。
- 摘要层级化：微摘要/要点/深度摘要三档；成本治理（预算、缓存、降级链路）；多 Provider（OpenAI 兼容、本地模型）。
- 结构化输出：概念与关系抽取，生成“概念卡”与“复习卡”（问答/完形）。

4) 输出（Sink）
- 多目标：Flomo（默认）、Obsidian（MD/Dataview）、Notion（DB）、Anki（APKG/AnkiConnect）、Slack/Telegram（通知）。
- 幂等与可恢复：posting_key（fingerprint+sink+template_hash），记录 sink_item_id；失败重试、队列化、节流；干跑预览。

5) 复盘（Feedback）
- 指标与回收：编辑/收藏/删除等互动作为信号；每周报告：主题分布、模板质量、低效输出告警。
- 可解释性：给出“为何选择此条目”的评分贡献 Top-3。

五、工程落地与模块
- ContentSource/NoteSink 协议；Pipeline（Fetch→Dedup→Rank→Render→Post→Record）幂等化；本地 state：synced_state.json（posting_key、sink_item_id、fingerprint、score 等）。
- 去重：文本归一化 + 指纹（SimHash/MinHash 可演进），相似度阈值；当前可先实现 SHA1 指纹提升稳态。
- 选择：MMR 多样性；评分可解释。
- 标签：词典优先 + 统计 + AI 兜底；回收学习。
- 模板：条件化、宏、风格参数。
- 稳定性：速率限制、指数退避、Cookie 过期告警、降级缓存；日志与可观测性。

六、近期可交付（1-2 周）
- 指纹去重（已在本分支落地基础版）：归一化文本 + SHA1 指纹，记录于 synced_bookmarks.json 的 synced_fingerprints 字段，减少重复推送。
- 干跑预览：通过环境变量 DRY_RUN=true 进行无副作用演练（已支持 flomo 客户端层面的 Dry-Run）。
- 幂等与重试：保守重试策略（429/5xx），运行稳定性增强（已存在基础实现）。

七、中期能力（3-4 周）
- 重要性评分与主题多样性；标签规范化与用户回收学习；每周复盘报告与可解释性输出。

八、长期路线（5-8 周）
- 多 Sink 插件化（Obsidian/Notion/Anki）；概念/关系结构化输出、复习卡；多 Source 接入（Kindle/Pocket）。

九、成功指标与实验
- 产出质量：手动编辑率下降，后续互动率提升；
- 稳定性：重复推送率下降、最终成功率提升；
- 学习：标签一致性提升、长期复用率上升；
- 实验：时间筛 vs 评分、模板 A/B、摘要档位对互动的影响。

十、风险与对策
- WeRead 风控：节流与退避、Cookie 过期告警、降级缓存；
- AI 成本：缓存与预算、降级链路与本地兜底；
- 标签漂移：词典优先与回收学习；
- 多 Sink 幂等复杂度：统一 posting_key 与状态存储，严格 upsert 语义。

——

附：指纹与选择伪代码

normalize(s): join(re.findall("\\w+", s)).lower()
fingerprint(text): sha1(normalize(text))
score(h): w_len*f_len + w_note*has_note + w_pos*pos + w_hist*hist + w_time*decay - w_dup*dup
select: MMR(scores, topic_sim(simhash(h1), simhash(h2)))

本方案将 WeRead2Flomo 从“自动搬运”提升为“知识加工器”，优先在“重要性判别、去重稳态、模板条件化、幂等发布、预览+复盘”五处发力，先把质量与稳定性打牢，再扩展多源/多端与结构化能力，形成复利。
