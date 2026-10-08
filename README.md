# Ace Data Cloud for Langflow

Use Ace Data Cloud chat models and service components in Langflow 1.12.5 or later. One Extension Bundle supplies a named **Ace Data Cloud** model provider and separate components for 17 image, video, audio, search, and face service families. The examples contain no credentials.

[简体中文教程](README_zh_CN.md) · [Current models and prices](https://platform.acedata.cloud/models) · [Source](https://github.com/AceDataCloud/LangflowAceDataCloud)

> **Availability:** The [0.1.0 GitHub Release](https://github.com/AceDataCloud/LangflowAceDataCloud/releases/tag/v0.1.0) is pip-installable. It is not yet published on PyPI or included in Langflow's default curated installation. The [official Langflow submission](https://github.com/langflow-ai/langflow/pull/15659) is under review.

## 1. Install the extension

Ask your Langflow administrator to install it in the **same Python environment** as Langflow. For a fresh local environment:

```bash
uv venv --python 3.12
source .venv/bin/activate
uv pip install "langflow==1.12.5"
uv pip install "https://github.com/AceDataCloud/LangflowAceDataCloud/releases/download/v0.1.0/lfx_acedatacloud-0.1.0-py3-none-any.whl"
lfx extension list
langflow run
```

You can also clone this repository and run `uv pip install .` to install from source. The GitHub wheel is a public package artifact, not a PyPI listing.

Restart an existing Langflow server after installing. Open the local URL shown by `langflow run` (normally `http://localhost:7860`). In a flow, open **Components → Ace Data Cloud**. The package exposes 17 service actions and 15 separate task readers. An installed Python package appearing in this palette is proof of this server's installation only.

![Ace Data Cloud component group in Langflow 1.12.5](_assets/tutorial/04-service-components.png)

## 2. Create an API key with the right access

1. Sign in to [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications).
2. Open **General application** if you want one key for both chat models and several services. A service-specific application key can only use that service. Copy an existing key or create a dedicated key in **Manage Keys → Create**.
3. Check service access, current price, and balance before any paid run. If you restrict **Allowed APIs**, include the exact submit and task-query routes used by your flow. For GPT Image, allow `/openai/images/generations` and `/openai/tasks`. For chat models, allow `/v1/models` and `/v1/chat/completions`.
4. Copy the token string only. Do not prepend `Bearer ` or use a platform management token. Keep the key out of prompts, flow JSON, screenshots, and support tickets.

## 3. Store the key in Langflow

Choose your profile icon → **Settings → Global Variables → Add New**. Set **Type** to **Credential**, **Name** to `ACEDATACLOUD_API_KEY`, paste the token into **Value**, then choose **Save Variable**. The saved value is masked.

![Langflow's Create Variable dialog before a key is entered](_assets/tutorial/17-create-credential.png)

![Credential global variable saved with its value masked](_assets/tutorial/18-saved-credential.png)

The same variable connects the named model provider. Open **Settings → Model Providers → Ace Data Cloud** and check the API Key shows as connected. The test installation showed 84 public chat models on 9 October 2026; model access and the live catalog can change. Enable the specific model you want to use.

![Named Ace Data Cloud provider in Langflow settings](_assets/tutorial/26-model-provider-settings.png)

![Connected provider credential and model list, with the key masked](_assets/tutorial/27-model-provider-detail.png)

On each service node, click the globe icon in **Ace Data Cloud API key** and select `ACEDATACLOUD_API_KEY`. The first GPT Image flow has **two** key fields: one on Generate and one on Retrieve Task. Bind both. A global variable reference saves the variable name in the flow; the token stays in Langflow's credential store. Before sharing an exported flow, inspect it for literal secrets. In our Langflow 1.12.5 test, enabling `LANGFLOW_REMOVE_API_KEYS=true` also removed this field's global-variable reference on reload; use the default setting for persistent binding and confirm the reference survives a reload.

## 4. Try the chat model provider

On the Projects page, click **Upload a flow** and select [`examples/chat_model.json`](examples/chat_model.json). It has a Language Model node set to **Ace Data Cloud → `gpt-4.1-mini`**, connected to Chat Output. Its fixed input says `Reply with exactly OK.`. The API Key override is empty so Langflow uses the provider credential configured above. Click the **Run component** triangle on Chat Output once, then inspect the output or **Traces**.

![Ready-to-import chat model flow](_assets/tutorial/31-chat-model-flow.png)

The recorded test returned `OK` using 11 input and 5 output tokens. The model and reply were verified in the flow trace and one matching Credits usage record. Your response and charge depend on the current model and account.

![Actual Ace Data Cloud model response in Langflow Traces](_assets/tutorial/33-chat-model-trace.png)

## 5. Generate one GPT Image and query the same task

Upload [`examples/gpt_image.json`](examples/gpt_image.json). Langflow 1.12.5 accepted the no-key JSON and displayed this path:

![The no-key flow uploaded successfully in Projects](_assets/tutorial/12-import-result.png)

**GPT Image Generate → GPT Image Retrieve Task → Chat Output**

![Actual imported GPT Image flow with two connections](_assets/tutorial/13-imported-gpt-image-flow.png)

Bind `ACEDATACLOUD_API_KEY` to both Ace nodes. The example already sets these first-run values; leave other parameters empty:

| Field | Value |
| --- | --- |
| Prompt | `A single blue paper sphere on a plain cream background, clean studio photograph, no text.` |
| Model | `gpt-image-2` |
| Size | `1024x1024` |
| Quality | `low` |
| Image count | `1` |
| Additional route parameters | `{"async": true}` |
| Retrieve Task → Wait up to seconds | `240` |

In the editor, select Generate → **Parameters → Add** on **Additional route parameters** to inspect the prefilled `async=true` pair. It requests a task ID without waiting for the full media generation in the submit call.

![The real 0.1.1 Langflow form with async true visible](_assets/tutorial/41-async-first-run.png)

Click **Run component** on **Chat Output once**. Generate makes one paid submission and requests an immediate task ID. Its returned `task_id` is connected to Retrieve Task's **Submitted task** input. Retrieve Task uses only `/openai/tasks` and waits up to 240 seconds for that same ID. A green flow before the service task is terminal is not proof that the media is ready.

![One completed Langflow run with both API components and a masked credential reference](_assets/tutorial/21-gpt-image-run.png)

![One successful run in Flow Activity](_assets/tutorial/22-run-traces.png)

The real test returned `status=succeeded`, `success=true`, task ID `ac4ffabb-ada6-4689-b275-7e9f9928493a`, and one PNG URL. The returned media was opened over HTTPS and its response was `200 image/png`.

![Actual task output in Langflow Traces](_assets/tutorial/25-task-output.png)

![Image produced by that run](_assets/tutorial/38-generated-image.png)

If the result is still `pending`, **do not rerun the generation flow**. That would submit another paid task. Import [`examples/retrieve_only/gpt_image.json`](examples/retrieve_only/gpt_image.json), bind the same Credential variable, paste the original task ID into **Task ID**, and run Chat Output. This flow contains no generation node. Repeat this read-only flow until the task is terminal.

If a submission times out after the service accepted it, check Usage History before another submission. GPT Image, Midjourney, and Veo task readers also accept a **Trace ID** from request history when the task ID was not returned. For other services, recover the task ID from the original usage record or ask support with its trace ID. Query the recovered task; never regenerate only to learn its status.

![An actual Midjourney result recovered in a query-only Langflow flow using its trace ID](_assets/tutorial/39-trace-recovery.png)

![Separate task lookup with the original task ID](_assets/tutorial/34-retrieve-only.png)

![The retrieve-only flow completed without a generation node](_assets/tutorial/35-retrieve-only-run.png)

## 6. Check the charge

In [Ace Data Cloud → Usage History](https://platform.acedata.cloud/console/usages), filter to the relevant API, key, and time, then compare the task or trace ID. The completed GPT Image test had trace ID `813ac552-4724-4d05-8b17-3c93534fbed6`; the platform returned **one** HTTP 200 usage record for that trace and deducted **0.099 Credits**. Langflow's task output also reported `cost.amount=0.099` in `credit` currency. This is evidence for that single test, not a fixed future price. Read your account's current package rate if you need a USD conversion.

The chat model example had one matching usage record for `gpt-4.1-mini`, 16 tokens, and `0.0000234636021` Credits. [Sanitized run evidence](tests/evidence/) keeps task, media, import, and billing readbacks separate.

## Other service examples

Each file below is a no-key first-run flow. For asynchronous services, the matching `retrieve_only` file queries an existing task ID without another submission. Each named component exposes the listed first-run action and an allowlisted **Additional route parameters** field. These are focused entry points; they do not claim every advanced action supported by the underlying API.

The 15 asynchronous first-run flows and newly added media components prefill `{"async": true}` so the task reader can query promptly. Fish Audio can also finish synchronously when used without that option; a connected completed result passes through its reader without another API call.

The exact public routes, default values, and proof level for each action are in [Capabilities](CAPABILITIES.md).

| Service | First-run action | Import flow | Task lookup |
| --- | --- | --- | --- |
| GPT Image | Generate one image | [Flow](examples/gpt_image.json) | [Lookup](examples/retrieve_only/gpt_image.json) |
| Suno | Generate instrumental audio | [Flow](examples/suno.json) | [Lookup](examples/retrieve_only/suno.json) |
| Seedance | Generate text-to-video | [Flow](examples/seedance.json) | [Lookup](examples/retrieve_only/seedance.json) |
| Fish Audio | Text-to-speech | [Flow](examples/fish_audio.json) | [Lookup](examples/retrieve_only/fish_audio.json) |
| Seedream | Generate one image | [Flow](examples/seedream.json) | [Lookup](examples/retrieve_only/seedream.json) |
| Happy Horse | Generate text-to-video | [Flow](examples/happy_horse.json) | [Lookup](examples/retrieve_only/happy_horse.json) |
| Qwen Image | Generate one image | [Flow](examples/qwen_image.json) | [Lookup](examples/retrieve_only/qwen_image.json) |
| Veo | Generate text-to-video | [Flow](examples/veo.json) | [Lookup](examples/retrieve_only/veo.json) |
| Google Search | Web search, synchronous | [Flow](examples/google_search.json) | No task ID |
| Grok Video | Generate text-to-video | [Flow](examples/grok.json) | [Lookup](examples/retrieve_only/grok.json) |
| Face Transform | Analyze face keypoints, synchronous | [Flow](examples/face_transform.json) | No task ID |
| Midjourney | Imagine one image | [Flow](examples/midjourney.json) | [Lookup](examples/retrieve_only/midjourney.json) |
| Flux | Generate one image | [Flow](examples/flux.json) | [Lookup](examples/retrieve_only/flux.json) |
| MiniMax H3 | Generate text-to-video | [Flow](examples/minimax_h3.json) | [Lookup](examples/retrieve_only/minimax_h3.json) |
| Wan | Generate text-to-video | [Flow](examples/wan.json) | [Lookup](examples/retrieve_only/wan.json) |
| Kling | Generate text-to-video | [Flow](examples/kling.json) | [Lookup](examples/retrieve_only/kling.json) |
| Nano Banana | Generate one image | [Flow](examples/nano_banana.json) | [Lookup](examples/retrieve_only/nano_banana.json) |

All 18 first-run JSON flows (one model plus 17 services) and all 15 retrieve-only flows were imported into Langflow 1.12.5. The 15 readers first retrieved existing completed tasks without submitting generation. We then made exactly one new paid submission through each of the other 14 media Component classes: all 14 tasks completed, their first media URLs returned HTTP 200, and each matched one Credits usage record. Those 14 calls deducted 19.302232 Credits in total; see [sanitized per-service evidence](tests/evidence/media-generation-live.json). Midjourney and Grok's original synchronous submit calls timed out after the service accepted them; both tasks were recovered from usage records and completed without a paid retry. The imported UI flow itself was run end to end for GPT Image and the chat model; the other service flows were imported and their component methods were called, but their full UI graph execution has not been claimed.

## Troubleshooting

| What you see | What to do |
| --- | --- |
| Bundle missing | Install in Langflow's Python environment, run `lfx extension list`, then restart the server. |
| Provider missing or zero models | Check **Settings → Model Providers**, the Credential global variable, `/v1/models` access, and the desired model toggle. |
| 401 or 403 | Check the full application API key, allowed API routes, service entitlement, expiry, and balance. Do not paste `Bearer ` into the key field. |
| 400 | Check the exact model, action, duration, size, and any additional parameters. This bundle fixes the public route for each first-run action. |
| `pending` or no media | Query the same task ID with the retrieve-only flow. Do not click Generate again to poll. |
| 429 | Wait and reduce concurrency. Do not enable automatic paid retries. |
| Timeout or 5xx | Check request history and task status before deciding whether a new submission is needed. Use the task reader's Trace ID field where available. Give support the task or trace ID, never the key. |

## Privacy, scope, and development

The extension sends the selected inputs and Bearer token to `https://api.acedata.cloud`. Secrets belong in Langflow Credential global variables. Generated media links can be shared by anyone who has the URL; handle exported flows and outputs accordingly. The extension itself is free; Ace Data Cloud API usage follows the current service price and your account balance. See [Privacy](PRIVACY.md), [Issues](https://github.com/AceDataCloud/LangflowAceDataCloud/issues), or dev@acedata.cloud.

To develop or review the package:

```bash
uv pip install -e .
lfx extension validate src/lfx_acedatacloud --execute-imports
pytest -q tests
python -m build
```

The public `BUNDLE_API_VERSION=1` manifest and separate provider/component IDs are checked against Langflow 1.12.5. Package installation, official Langflow source acceptance, default inclusion, and live service completion are tracked as distinct outcomes.
