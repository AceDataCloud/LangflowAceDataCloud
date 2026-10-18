# GPT Image by Ace Data Cloud for Langflow

Install just the GPT Image Generate and Retrieve Task nodes. This candidate package
does not install the full Ace bundle or register a chat model provider.
It uses the same reviewed client, request rules, and task implementation as the
aggregate package. Ace Data Cloud supplies this integration; service-owner
endorsement is not implied.

Version 0.1.3 is a source candidate, not a published PyPI or GitHub release.
From a complete checkout at the desired commit, in Langflow's Python environment:

```bash
python -m pip install ./packages/gpt-image
lfx extension list
langflow run
```

Restart an existing server. Open **Components → GPT Image by Ace Data Cloud** or search **GPT Image**.
Bind an Ace application API key stored as a Langflow Credential to both nodes.
Generate submits once; Retrieve Task only queries the original task. API usage
is paid according to current service prices; installing this extension is free.
See the [English guide](https://github.com/AceDataCloud/LangflowAceDataCloud/blob/main/guides/gpt-image.md)
and [Chinese guide](https://github.com/AceDataCloud/LangflowAceDataCloud/blob/main/guides/gpt-image_zh_CN.md).
These guides are part of the same candidate until merged.

The wheel includes no-key generation and retrieve-only flow JSON under
`lfx_acedatacloud_gpt_image/examples/`; use these with this service package. Aggregate examples
retain `ext:ace_data_cloud:*` IDs and require the aggregate installation.
This package uses `ext:ace_gpt_image:<Class>@official` IDs. All five service packages
can coexist. With the aggregate installed, its legacy category remains alongside
the service category; neither replaces the other's saved nodes. Uninstalling
one package does not remove another package's files.

Build a wheel and a self-contained sdist with `python -m build packages/gpt-image`.
The shared hook stages runtime source under the unique `lfx_acedatacloud_gpt_image` namespace;
only these two component files are discoverable. No runtime code is maintained
in this packaging directory. Maintainers regenerate metadata and hook copies
with `python scripts/service_packages.py`, then use `--check` to detect drift.
