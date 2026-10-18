"""Packaging contracts for reproducible service-only distributions."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def test_service_packaging_metadata_and_hooks_are_current() -> None:
    """Reject hook, license and metadata drift from the single source generator."""
    root = Path(__file__).resolve().parents[1]
    spec = importlib.util.spec_from_file_location(
        "service_packages", root / "scripts/service_packages.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for path, expected in module.generated_files().items():
        assert path.read_text() == expected, f"Regenerate {path.relative_to(root)}"
