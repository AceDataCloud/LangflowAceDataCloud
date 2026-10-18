"""Check real installed service wheels, forms, IDs and credential-free graphs.

Run after pip installation, outside src/; never submits or queries an API.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from importlib.metadata import distribution, distributions, version
from pathlib import Path

from lfx.custom.utils import create_component_template
from lfx.extension.discovery import discover_installed_extensions
from lfx.extension.loader import load_installed_extensions
from lfx.graph import Graph

from service_packages import SERVICES


def main() -> None:
    """Fail on extra service registration, namespace collision or stale examples."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--services", nargs="*", choices=SERVICES, default=[])
    parser.add_argument("--aggregate", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    expected = {f"lfx-acedatacloud-{slug}" for slug in args.services}
    if args.aggregate:
        expected.add("lfx-acedatacloud")
    installed = [
        dist
        for dist in distributions()
        if dist.metadata["Name"].startswith("lfx-acedatacloud")
    ]
    assert {dist.metadata["Name"] for dist in installed} == expected
    records, errors = discover_installed_extensions(installed)
    assert not errors, errors
    assert {record.extension_id for record in records} == expected
    results = load_installed_extensions(installed)
    assert len(results) == len(expected)
    assert all(result.ok for result in results), results
    components = [component for result in results for component in result.components]
    ids = [component.namespaced_id for component in components]
    assert len(ids) == len(set(ids)), ids
    bundles = [result.bundle for result in results]
    assert len(bundles) == len(set(bundles)), bundles
    provider_ids = [
        provider.provider_id
        for record in records
        for provider in record.manifest.manifest.providers
    ]
    assert provider_ids == (["acedatacloud"] if args.aggregate else [])
    forms = []
    for component in components:
        template, _ = create_component_template(component_extractor=component.klass())
        assert template.get("outputs")
        forms.append({"id": component.namespaced_id, "label": template["display_name"]})
    assert len(forms) == len(args.services) * 2 + (32 if args.aggregate else 0)
    flows = []
    sources = {}
    for slug in args.services:
        key, _, _ = SERVICES[slug]
        module = f"lfx_acedatacloud_{key}"
        dist = distribution(f"lfx-acedatacloud-{slug}")
        root = Path(dist.locate_file(module)).resolve()
        assert "site-packages" in root.parts, root
        source = json.loads(dist.read_text("direct_url.json") or "{}")
        assert not source.get("dir_info", {}).get("editable")
        sources[dist.metadata["Name"]] = source
        manifest = json.loads((root / "extension.json").read_text())
        assert "providers" not in manifest
        component_files = list((root / "components/acedatacloud").glob("*.py"))
        assert {path.stem for path in component_files} == {
            "__init__",
            key,
            f"{key}_task",
        }
        assert not (root / "provider.py").exists()
        for path in sorted((root / "examples").rglob("*.json")):
            payload = json.loads(path.read_text())
            assert "ext:ace_data_cloud:" not in path.read_text()
            for node in payload["data"]["nodes"]:
                key_field = node["data"]["node"]["template"].get("api_key")
                assert not key_field or not key_field.get("value")
            graph = Graph.from_payload(payload, emit_extension_events=False)
            assert len(graph.vertices) == len(payload["data"]["nodes"])
            flows.append({"package": dist.metadata["Name"], "file": path.name})
    assert len(flows) == len(args.services) * 2
    evidence = {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "lfx_version": version("lfx"),
        "packages": {name: version(name) for name in sorted(expected)},
        "sources": sources,
        "forms": forms,
        "flows": flows,
        "provider_ids": provider_ids,
        "paid_calls": 0,
        "boundary": "Real pip installation and LFX startup discovery, forms and graph parsing; no browser, API or billing.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(evidence, indent=2) + "\n")
    print(f"{len(expected)} packages: {len(forms)} forms, {len(flows)} no-key graphs")


if __name__ == "__main__":
    main()
