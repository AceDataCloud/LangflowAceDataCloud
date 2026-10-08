# Implemented API surface

This table describes the **first-run actions implemented by this extension**, not every action in the Ace Data Cloud APIs. The route and parameter contracts were checked against the public Ace API guides and the corresponding [Ace Data Cloud Dify submissions](https://github.com/orgs/AceDataCloud/repositories?q=Dify) on 9 October 2026. Each component fixes its public route; `extra_parameters` accepts only the allowlisted fields in [`specs.py`](src/lfx_acedatacloud/specs.py).

| Service | First-run operation | Submit route | Task route | Tested in Langflow |
| --- | --- | --- | --- | --- |
| GPT Image | `gpt-image-2`, low quality, one 1024×1024 image | `/openai/images/generations` | `/openai/tasks` | New submit, completion, media, billing |
| Suno | `chirp-v6` short instrumental | `/suno/audios` | `/suno/tasks` | Existing task lookup and media |
| Seedance | Text content to `doubao-seedance-2-0-mini-260615` video, 480p, no audio | `/seedance/videos` | `/seedance/tasks` | Existing task lookup and media |
| Fish Audio | `s2-pro` MP3 speech; model is a request header | `/fish/tts` | `/fish/tasks` when async | Existing task lookup and media |
| Seedream | `doubao-seedream-5-0-lite-260128` image, 2K | `/seedream/images` | `/seedream/tasks` | Existing task lookup and media |
| Happy Horse | `happyhorse-1.1-t2v` video, 3 seconds | `/happyhorse/videos` | `/happyhorse/tasks` | Existing task lookup and media |
| Qwen Image | `qwen-image-3.0` image | `/qwen-image/images` | `/qwen-image/tasks` | Existing task lookup and media |
| Veo | `veo31-fast` text-to-video | `/veo/videos` | `/veo/tasks` | Existing task lookup and media |
| Google Search | Three web search results | `/serp/google` | Synchronous | New call and billing |
| Grok Video | `grok-imagine-video-1.5-fast:reverse` video, 480p | `/grok/videos` | `/grok/tasks` | Existing task lookup and media |
| Face Transform | Analyze image keypoints; action selector also maps six other published face routes | `/face/analyze` for first run | Synchronous | New keypoints call and billing |
| Midjourney | Version 8.2 image, fast mode | `/midjourney/imagine` | `/midjourney/tasks` | Existing task lookup and media |
| Flux | `flux-dev` image, 1024×1024 | `/flux/images` | `/flux/tasks` | Existing task lookup and media |
| MiniMax H3 | `MiniMax-H3` video; text is a content array | `/minimax/videos` | `/minimax/tasks` | Existing task lookup and media |
| Wan | `wan3.0-video` text-to-video, 720P, audio off | `/wan/videos` | `/wan/tasks` | Existing task lookup and media |
| Kling | `kling-v3-turbo` text-to-video, standard mode | `/kling/videos` | `/kling/tasks` | Existing task lookup and media |
| Nano Banana | `nano-banana-2-lite` image, 1K | `/nano-banana/images` | `/nano-banana/tasks` | Existing task lookup and media |

The model Provider uses the fixed Ace Data Cloud OpenAI-compatible `/v1` endpoint. It registers `ChatAceDataCloud`, includes five known fallback catalog rows, and reads an authenticated `/v1/models` list when a key is connected. A key is required to invoke models. Only model IDs in the 84-entry public chat catalog verified against the live list on 9 October 2026 are offered; image and embedding IDs are excluded. The `gpt-4.1-mini` model completed a real Langflow flow with 16 tokens and a matching Credits usage record.

For the 15 asynchronous families, the Generate and Retrieve Task classes are separate. Generate sends one HTTP request and never retries automatically. Retrieve Task uses only the relevant `/tasks` route, accepts a connected result or an existing literal task ID, checks the service identity on connected results, and reports `pending`, `succeeded`, or `failed`. Media URLs are shown only when status is `succeeded`. A pending result is never treated as completion. The 15 retrieve-only examples have no generation node.

Advanced actions such as edit, extend, batch retrieval, voice management, video lip sync, or face transformations beyond keypoints are **not all represented by first-run flows**. They require their own UI fields and tests before being claimed as Langflow-supported. Hailuo, Luma, and Producer are excluded because they were not in the official-submitted Dify comparison set.

Validation evidence: `lfx extension validate --execute-imports` passed, the 0.1.0 wheel loaded 32 named service components and the model Provider in a fresh Langflow 1.12.5 environment, and the 18 first-run plus 15 retrieve-only JSON files were imported. [Sanitized live readbacks](tests/evidence/) distinguish new paid calls from read-only reuse of existing completed tasks.
