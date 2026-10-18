# GPT Image by Ace Data Cloud for Langflow

Install just the GPT Image Generate and Retrieve Task nodes. This service package
does not install the full Ace bundle or register a chat model provider.
It uses the same reviewed client, request rules, and task implementation as the
aggregate package. Ace Data Cloud supplies this integration; service-owner
endorsement is not implied.

## 1. Install the nodes

Version 0.1.4. Install the public GitHub wheel in the same Python environment
as Langflow (1.12.5 or later):

```bash
python -m pip install "https://github.com/AceDataCloud/LangflowAceDataCloud/releases/download/v0.1.4/lfx_acedatacloud_gpt_image-0.1.4-py3-none-any.whl"
lfx extension list
langflow run
```

The [versioned GitHub release](https://github.com/AceDataCloud/LangflowAceDataCloud/releases/tag/v0.1.4) provides the wheel
and a self-contained source archive. No GitHub account is needed to install it.
If version 0.1.4 is listed on [PyPI](https://pypi.org/project/lfx-acedatacloud-gpt-image/),
you can also run `python -m pip install "lfx-acedatacloud-gpt-image==0.1.4"`.
Suno and Seedance project creation was temporarily rate-limited by PyPI at the
0.1.3 release; the direct wheel command above works independently of PyPI listing
availability. [Official Langflow default inclusion](https://github.com/langflow-ai/langflow/pull/15659)
remains under review.

Restart an existing server. Open **Components → GPT Image by Ace Data Cloud** or search **GPT Image**.

## 2. Create and copy your application API key

1. Register or sign in at [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=langflow_gpt_image_package_api_key).
   If there is no **General application**, choose **Initialize General Application**
   first, then open it. A general-application key uses your account's enabled
   services; a service-specific application key is limited to that service.
2. Copy the existing API Key with the copy icon, or choose **Manage Keys → Create**
   to make a dedicated key, for example `Langflow GPT Image`.
3. Set the key's expiration, usage limit and **Allowed APIs** as needed. If you
   restrict Allowed APIs, include both `/openai/images/generations` and `/openai/tasks`
   so Generate and Retrieve Task can both work. Click **Create**, return to the
   key list or application card, and copy the token.
4. Confirm GPT Image service access, [current price and balance](https://platform.acedata.cloud/models?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=langflow_gpt_image_package_pricing)
   before a paid run. Copy only the raw token, without `Bearer ` or quotes.
   Use an application API key, not an account-management token.

![Copy the API key or open Manage Keys](https://raw.githubusercontent.com/AceDataCloud/LangflowAceDataCloud/v0.1.4/_assets/tutorial/get-api-key-en.png)

![Create a dedicated application API key](https://raw.githubusercontent.com/AceDataCloud/LangflowAceDataCloud/v0.1.4/_assets/tutorial/create-api-key-en.png)

## 3. Save a private Credential in Langflow

Open **Settings → Global Variables → Add New**. Set **Type** to **Credential**,
**Name** to `ACEDATACLOUD_API_KEY`, paste the token into **Value**, and choose
**Save Variable**. On **both Generate and Retrieve Task**, click the globe icon
next to **Ace Data Cloud API key** and select `ACEDATACLOUD_API_KEY`.
Confirm the binding survives a reload. Keep the token out of prompts, screenshots
and exported flow JSON; inspect exports for literal secrets before sharing.
Revoke a temporary or exposed key under **Manage Keys**, then update the saved
Credential if you replace it.

![Create a Credential before entering a key](https://raw.githubusercontent.com/AceDataCloud/LangflowAceDataCloud/v0.1.4/_assets/tutorial/17-create-credential.png)

## 4. Run and check the result

Generate submits once; Retrieve Task only queries the original task. API usage
is paid according to current service prices; installing this extension is free.
Use the retrieve-only flow with the original task ID while a task is pending;
do not rerun Generate just to check progress. Compare the task or trace with
[Usage History](https://platform.acedata.cloud/console/usages?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=langflow_gpt_image_package_usage). Charges are in Credits.
See the [English guide](https://github.com/AceDataCloud/LangflowAceDataCloud/blob/v0.1.4/guides/gpt-image.md)
and [Chinese guide](https://github.com/AceDataCloud/LangflowAceDataCloud/blob/v0.1.4/guides/gpt-image_zh_CN.md)
for first-run inputs and troubleshooting. For 401/403, check the copied key,
expiry, limits, both allowed routes, service access and balance.

## Packaging and saved flows

The wheel includes no-key generation and retrieve-only flow JSON under
`lfx_acedatacloud_gpt_image/examples/`; use these with this service package. Aggregate examples
retain `ext:ace_data_cloud:*` IDs and require the aggregate installation.
This package uses `ext:ace_gpt_image:<Class>@official` IDs. All five service packages
can coexist. With the aggregate installed, its legacy category remains alongside
the service category; neither replaces the other's saved nodes. Uninstalling
one package does not remove another package's files.

From the complete `v0.1.4` source checkout, build a wheel and a self-contained sdist with `python -m build packages/gpt-image`. A local source install is `python -m pip install ./packages/gpt-image`.
The shared hook stages runtime source under the unique `lfx_acedatacloud_gpt_image` namespace;
only these two component files are discoverable. No runtime code is maintained
in this packaging directory. Maintainers regenerate metadata and hook copies
with `python scripts/service_packages.py`, then use `--check` to detect drift.
