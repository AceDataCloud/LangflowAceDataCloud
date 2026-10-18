# Suno by Ace Data Cloud for Langflow

Install just the Suno Generate and Retrieve Task nodes. This service package
does not install the full Ace bundle or register a chat model provider.
It uses the same reviewed client, request rules, and task implementation as the
aggregate package. Ace Data Cloud supplies this integration; service-owner
endorsement is not implied.

Version 0.1.3. Install in the same Python environment as Langflow:

```bash
python -m pip install "lfx-acedatacloud-suno==0.1.3"
lfx extension list
langflow run
```

The [versioned GitHub release](https://github.com/AceDataCloud/LangflowAceDataCloud/releases/tag/v0.1.3) also provides a wheel and self-contained source archive for this service.

Restart an existing server. Open **Components → Suno by Ace Data Cloud** or search **Suno**.
Bind an Ace application API key stored as a Langflow Credential to both nodes.
Generate submits once; Retrieve Task only queries the original task. API usage
is paid according to current service prices; installing this extension is free.
See the [English guide](https://github.com/AceDataCloud/LangflowAceDataCloud/blob/main/guides/suno.md)
and [Chinese guide](https://github.com/AceDataCloud/LangflowAceDataCloud/blob/main/guides/suno_zh_CN.md).


The wheel includes no-key generation and retrieve-only flow JSON under
`lfx_acedatacloud_suno/examples/`; use these with this service package. Aggregate examples
retain `ext:ace_data_cloud:*` IDs and require the aggregate installation.
This package uses `ext:ace_suno:<Class>@official` IDs. All five service packages
can coexist. With the aggregate installed, its legacy category remains alongside
the service category; neither replaces the other's saved nodes. Uninstalling
one package does not remove another package's files.

From the complete `v0.1.3` source checkout, build a wheel and a self-contained sdist with `python -m build packages/suno`. A local source install is `python -m pip install ./packages/suno`.
The shared hook stages runtime source under the unique `lfx_acedatacloud_suno` namespace;
only these two component files are discoverable. No runtime code is maintained
in this packaging directory. Maintainers regenerate metadata and hook copies
with `python scripts/service_packages.py`, then use `--check` to detect drift.
