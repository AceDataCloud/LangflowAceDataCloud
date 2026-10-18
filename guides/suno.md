# Suno by Ace Data Cloud for Langflow


**Suno by Ace Data Cloud** lets you generate instrumental music in Langflow. This is an Ace Data Cloud integration, not a claim of endorsement by the Suno service owner. Search **suno** or **suno** in the component palette; choose **Suno Generate by Ace Data Cloud** and **Suno Retrieve Task by Ace Data Cloud**.

## 1. Install and find the nodes

In Langflow's Python environment, install `lfx-acedatacloud-suno==0.1.4`, then restart the server:

```bash
python -m pip install "https://github.com/AceDataCloud/LangflowAceDataCloud/releases/download/v0.1.4/lfx_acedatacloud_suno-0.1.4-py3-none-any.whl"
```

The [v0.1.4 GitHub release](https://github.com/AceDataCloud/LangflowAceDataCloud/releases/tag/v0.1.4) also provides a wheel for this service. Open **Components → Suno by Ace Data Cloud** or search the service name. This package registers only its two nodes and no chat provider. Its Python package `examples/` directory contains matching no-key Generate and Retrieve-only flows. See the [package README](../packages/suno/README.md).

The [aggregate installation](../README.md#1-install-the-extension) provides all services and a native chat provider. Root [generation](../examples/suno.json) and [retrieve-only](../examples/retrieve_only/suno.json) examples use aggregate IDs. Service-only examples use a separate bundle ID; both categories can coexist without replacing saved nodes. Official default inclusion is still [under review](https://github.com/langflow-ai/langflow/pull/15659); the proposed official documentation URL may remain unavailable until accepted.

## 2. Get an application API Token

Register or sign in at [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=langflow_suno_guide_api_key). If there is no **General application**, choose **Initialize General Application**. Copy its existing API Key or choose **Manage Keys → Create** for a dedicated Langflow token. Check Suno access, expiry, usage limit, [current price](https://platform.acedata.cloud/models?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=langflow_suno_guide_pricing) and balance. If **Allowed APIs** is restricted, allow both `/suno/audios` and `/suno/tasks`.

Copy only the raw token, without `Bearer ` or quotes. Do not use an account-management token. The Console images below are real existing screenshots from the Ace guide (2026-10-12 source revision); displayed keys are redacted.

![Copy or manage an Ace application key](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/get-api-key-en.png)

![Create a dedicated application key](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/create-api-key-en.png)

## 3. Save the token in Langflow

Open **Settings → Global Variables → Add New**. Choose **Credential**, name it `ACEDATACLOUD_API_KEY`, paste the raw token into **Value**, and save. On both Suno nodes, use the globe icon in **Ace Data Cloud API key** to select that credential. Never put a literal token in prompts or exported flow JSON.

![Real Langflow Create Credential dialog, before a key is entered](https://raw.githubusercontent.com/AceDataCloud/LangflowAceDataCloud/59beda518889ff106f64da9caaad56e59690a6e4/_assets/tutorial/17-create-credential.png)

This is a historical Langflow 1.12.5 screenshot from 2026-10-09. Its placement may differ in later versions; it is not a new Suno generation result.

## 4. Configure one submission and the same-task reader

Connect **Suno Generate by Ace Data Cloud → Suno Retrieve Task by Ace Data Cloud → Chat Output**. The reader's **Submitted task** input receives Generate's result. Bind the Credential on both nodes, then use these existing first-run values:

| Field | First-run value |
| --- | --- |
| Prompt (`prompt`) | `A short gentle instrumental piano melody for a sunrise, no vocals.` |
| Model (`model`) | `chirp-v6` |
| Instrumental (`instrumental`) | `True` |
| Target duration (seconds) (`duration`) | `10` |
| Additional route parameters | `{"async": true}` |
| Retrieve Task → Wait up to seconds | `240` |

The [flow file](https://github.com/AceDataCloud/LangflowAceDataCloud/blob/main/examples/suno.json) contains the exact prompt and route-specific values. Model availability and price can change. Review them before clicking Run; do not replace a model silently.

![Historical real Langflow wiring: Generate, Retrieve Task, Chat Output](https://raw.githubusercontent.com/AceDataCloud/LangflowAceDataCloud/59beda518889ff106f64da9caaad56e59690a6e4/_assets/tutorial/13-imported-gpt-image-flow.png)

This real screenshot is the GPT Image example on Langflow 1.12.5 (2026-10-09), illustrating the shared wiring only. It is not a screenshot of a new Suno run or evidence of official default inclusion.

## 5. Read the result without paying for a second submission

Click the Chat Output run control **once**. Generate makes one paid submission. The connected reader queries the same task; a green Langflow node or preview does not prove media completion. The terminal success output has `status=succeeded`, `success=true`, and `media_urls` with result links.

If the wait ends with `pending`, use the separate [retrieve-only Suno flow](https://github.com/AceDataCloud/LangflowAceDataCloud/blob/main/examples/retrieve_only/suno.json), paste the original task ID, and bind the same Credential. Do not rerun Generate just to check status. If a submission was accepted but its response timed out, recover the original ID from request history before considering another submission.

Check [Usage History](https://platform.acedata.cloud/console/usages?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=langflow_suno_guide_usage) against that original task or trace. Charges are Credits, not a fixed USD amount. Historical component tests are documented in the [capability matrix](https://github.com/AceDataCloud/LangflowAceDataCloud/blob/main/CAPABILITIES.md); a component test is not proof that every UI path or advanced API action has been exercised.

## Troubleshooting

- **No search result:** confirm the bundle is installed in the server's Python environment, restart it, then search the service name. Use version 0.1.3 or later for the service-first labels.
- **401/403:** check the raw application token, service access and allowed submit/query routes.
- **400:** check model and route-specific fields against the current guide.
- **429:** wait and reduce concurrency; keep automatic paid retries off.
- **Pending/timeout:** query the original task; do not submit another generation to poll.

The extension is free; Ace API use follows current prices and your balance. See [Ace Data Cloud bundle scope and privacy](https://docs.langflow.org/bundles-acedatacloud).
