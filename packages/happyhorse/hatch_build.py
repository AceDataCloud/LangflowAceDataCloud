# Generated from scripts/service_build_hook.py; do not edit.
"""Canonical build hook; generate package-local copies with service_packages.py.

Service wheels contain a namespaced subset of the existing implementation.
There is no aggregate extension dependency, provider registration, or shared
installed file. A service sdist contains the same subset and rebuilds offline.
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class ServiceBuildHook(BuildHookInterface):
    """Stage one service from canonical source, or use its self-contained sdist."""

    def initialize(self, version: str, build_data: dict) -> None:
        """Include only runtime helpers and this service's two component files."""
        config = self.metadata.hatch.config["service"]
        module = config["module"]
        service = config["key"]
        root = Path(self.root)
        canonical = root.parent.parent / "src" / "lfx_acedatacloud"
        if canonical.is_dir():
            self._stage = tempfile.TemporaryDirectory(prefix=f"{module}-")
            source = Path(self._stage.name) / module
            files = [
                "__init__.py",
                "client.py",
                "specs.py",
                "components/__init__.py",
                "components/base.py",
                "components/acedatacloud/__init__.py",
                f"components/acedatacloud/{service}.py",
                f"components/acedatacloud/{service}_task.py",
            ]
            for relative in files:
                target = source / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                original = canonical / relative
                if not original.is_file() and original.name != "__init__.py":
                    raise FileNotFoundError(original)
                text = (
                    original.read_text(encoding="utf-8") if original.is_file() else ""
                )
                target.write_text(
                    text.replace("lfx_acedatacloud", module), encoding="utf-8"
                )
            manifest = {
                "$schema": "https://schemas.langflow.org/extension/v1.json",
                "id": self.metadata.core.name,
                "version": self.metadata.version,
                "name": config["display"],
                "description": self.metadata.core.description,
                "lfx": {"compat": ["1"]},
                "bundles": [
                    {
                        "name": config["bundle"],
                        "path": "components/acedatacloud",
                        "display_name": config["display"],
                        "icon": config["icon"],
                    }
                ],
                "capabilities": {"requiresCredentials": True},
            }
            (source / "extension.json").write_text(
                json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
            )
            # Preserve component IDs in legacy examples; service-specific imports
            # get new bundle coordinates and embedded imports at build time.
            for relative in (f"{service}.json", f"retrieve_only/{service}.json"):
                example = root.parent.parent / "examples" / relative
                target = source / "examples" / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(
                    example.read_text(encoding="utf-8")
                    .replace("ext:ace_data_cloud:", f"ext:{config['bundle']}:")
                    .replace("lfx_acedatacloud", module),
                    encoding="utf-8",
                )
        else:
            source = root / "src" / module
            if not (source / "extension.json").is_file():
                raise RuntimeError("Build from a complete repository or service sdist")
        destination = f"src/{module}" if self.target_name == "sdist" else module
        build_data["force_include"][str(source)] = destination

    def finalize(self, version: str, build_data: dict, artifact_path: str) -> None:
        """Release temporary staging after Hatch has written the artifact."""
        if hasattr(self, "_stage"):
            self._stage.cleanup()
