"""Check the public wheel in an isolated stable Langflow installation.

This checks component forms and the real graph parser, without running a model
or service. It deliberately imports the installed wheel rather than src/.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from importlib.metadata import distribution, version
from pathlib import Path

import lfx_acedatacloud
from lfx.custom.utils import create_component_template
from lfx.extension.loader import load_extension
from lfx.graph import Graph


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--release", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    package_root = Path(lfx_acedatacloud.__file__).resolve().parent
    if package_root.is_relative_to(repo_root / "src"):
        raise RuntimeError("The release check must import the installed wheel")
    release = json.loads(args.release.read_text())
    installed_version = version("lfx-acedatacloud")
    if release["tag_name"] != f"v{installed_version}":
        raise RuntimeError("The installed version does not match the public tag")
    if version("langflow") != "1.12.5":
        raise RuntimeError("This check requires stable Langflow 1.12.5")
    direct_url = json.loads(
        distribution("lfx-acedatacloud").read_text("direct_url.json") or "{}"
    )
    if direct_url.get("dir_info", {}).get("editable"):
        raise RuntimeError("An editable source install is not a public wheel")

    loaded = load_extension(package_root)
    if loaded.errors:
        raise RuntimeError(str(loaded.errors))
    components = []
    for component in loaded.components:
        template, _ = create_component_template(component_extractor=component.klass())
        if not template.get("outputs"):
            raise RuntimeError(f"No output form for {component.class_name}")
        components.append(
            {
                "class": component.class_name,
                "display_name": template["display_name"],
                "form": "accepted",
            }
        )
    if len(components) != 32:
        raise RuntimeError(f"Expected 32 service components, got {len(components)}")

    flows = []
    for path in sorted((repo_root / "examples").rglob("*.json")):
        payload = json.loads(path.read_text())
        for node in payload["data"]["nodes"]:
            key_field = node["data"]["node"]["template"].get("api_key")
            if key_field and key_field.get("value"):
                raise RuntimeError(f"A flow contains a nonempty API key: {path.name}")
        graph = Graph.from_payload(payload, emit_extension_events=False)
        if len(graph.vertices) != len(payload["data"]["nodes"]):
            raise RuntimeError(f"Graph parser lost nodes: {path.name}")
        flows.append(
            {
                "path": str(path.relative_to(repo_root)),
                "nodes": len(graph.vertices),
                "parse": "accepted",
            }
        )
    if len(flows) != 33:
        raise RuntimeError(f"Expected 33 no-key flows, got {len(flows)}")

    evidence = {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "release": release["html_url"],
        "extension_version": installed_version,
        "langflow_version": version("langflow"),
        "lfx_version": version("lfx"),
        "installed_from": direct_url,
        "component_count": len(components),
        "no_key_flow_count": len(flows),
        "paid_calls": 0,
        "boundary": "Installed wheel, component forms and Graph.from_payload; no UI graph execution, generation, task retrieval or new billing.",
        "components": components,
        "flows": flows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n")
    print(
        f"Public {installed_version}: {len(components)} component forms and {len(flows)} no-key flows accepted"
    )


if __name__ == "__main__":
    main()
