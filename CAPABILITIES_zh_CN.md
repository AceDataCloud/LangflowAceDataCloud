# 已实现的 API 范围

下表只说明本扩展实现的**首跑动作**，不代表 Ace Data Cloud API 的全部能力。公开接口和参数参考 Ace API 指南及 [Ace Data Cloud 已投稿的 Dify 插件](https://github.com/orgs/AceDataCloud/repositories?q=Dify)，并于 2026 年 10 月 9 日复核。每个组件固定公开接口路径；`extra_parameters` 仅接受 [`specs.py`](src/lfx_acedatacloud/specs.py) 中列出的字段。

| 服务 | 首跑操作 | 提交接口 | 任务接口 | Langflow 验证 |
| --- | --- | --- | --- | --- |
| GPT Image | `gpt-image-2` 低画质、1 张 1024×1024 图片 | `/openai/images/generations` | `/openai/tasks` | 新提交、完成、媒体、账单 |
| Suno | `chirp-v6` 短纯音乐 | `/suno/audios` | `/suno/tasks` | 已有任务查询和媒体 |
| Seedance | 文本转 `doubao-seedance-2-0-mini-260615` 480p 无声视频 | `/seedance/videos` | `/seedance/tasks` | 已有任务查询和媒体 |
| Fish Audio | `s2-pro` MP3 语音；模型放在请求头 | `/fish/tts` | 异步时 `/fish/tasks` | 已有任务查询和媒体 |
| Seedream | `doubao-seedream-5-0-lite-260128`、2K 图片 | `/seedream/images` | `/seedream/tasks` | 已有任务查询和媒体 |
| Happy Horse | `happyhorse-1.1-t2v` 3 秒视频 | `/happyhorse/videos` | `/happyhorse/tasks` | 已有任务查询和媒体 |
| Qwen Image | `qwen-image-3.0` 图片 | `/qwen-image/images` | `/qwen-image/tasks` | 已有任务查询和媒体 |
| Veo | `veo31-fast` 文生视频 | `/veo/videos` | `/veo/tasks` | 已有任务查询和媒体 |
| Google Search | 返回 3 条网页结果 | `/serp/google` | 同步 | 新调用和账单 |
| Grok Video | `grok-imagine-video-1.5-fast:reverse`、480p 视频 | `/grok/videos` | `/grok/tasks` | 已有任务查询和媒体 |
| Face Transform | 人脸关键点分析；动作选择器另映射 6 个公开人脸接口 | 首跑 `/face/analyze` | 同步 | 新关键点调用和账单 |
| Midjourney | 8.2 版 fast 模式图片 | `/midjourney/imagine` | `/midjourney/tasks` | 已有任务查询和媒体 |
| Flux | `flux-dev`、1024×1024 图片 | `/flux/images` | `/flux/tasks` | 已有任务查询和媒体 |
| MiniMax H3 | `MiniMax-H3` 视频；文本转换为 content 数组 | `/minimax/videos` | `/minimax/tasks` | 已有任务查询和媒体 |
| Wan | `wan3.0-video`、720P、关闭音频的文生视频 | `/wan/videos` | `/wan/tasks` | 已有任务查询和媒体 |
| Kling | `kling-v3-turbo` 标准模式文生视频 | `/kling/videos` | `/kling/tasks` | 已有任务查询和媒体 |
| Nano Banana | `nano-banana-2-lite`、1K 图片 | `/nano-banana/images` | `/nano-banana/tasks` | 已有任务查询和媒体 |

模型 Provider 固定使用 Ace Data Cloud 的 OpenAI 兼容 `/v1` 接口，注册 `ChatAceDataCloud`，内置 5 条已知模型目录回退项，并在用户连接 Key 后读取需要鉴权的 `/v1/models`。实际调用模型必须提供 Key。只展示 2026 年 10 月 9 日已和线上模型列表交叉核对的 84 个公开对话模型 ID；图像与 embedding 模型不会误入对话列表。`gpt-4.1-mini` 已完成真实 Langflow 流程，返回 16 tokens，并匹配到 Credits 用量记录。

15 类异步服务分别有 Generate 和 Retrieve Task 组件。Generate 只发一次 HTTP 请求，不自动重试；Retrieve Task 仅访问对应 `/tasks`，可接收生成结果或已有任务 ID，且会核对已连接任务的服务身份。状态明确为 `pending`、`succeeded` 或 `failed`，只有 `succeeded` 才显示媒体链接。15 个 `retrieve_only` 示例均不含生成节点。

编辑、续写、批量查询、声音管理、视频口型同步等高级动作，以及关键点之外的人脸动作，**尚未全部配有独立首跑流程和真实测试**，不能宣称已在 Langflow 全面支持。Hailuo、Luma、Producer 不属于这次 Dify 正式投稿对标清单，因此未纳入本包。

验证记录：`lfx extension validate --execute-imports` 通过；0.1.0 wheel 在新的 Langflow 1.12.5 环境中加载了 32 个命名服务组件与模型 Provider；18 个首跑 JSON 和 15 个独立查询 JSON 均可导入。[脱敏读回](tests/evidence/)区分新付费调用与已有完成任务的只读查询。
