"""Validate structured records using configurable preflight helpers."""
import importlib.util
import pathlib

import yaml


def _run_hook(path):
    spec = importlib.util.spec_from_file_location("profilehooks.precheck", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.run()


def check_profiles(directory="profiles"):
    """Return names of profiles whose preflight hook fails."""
    root = pathlib.Path(directory)
    if not root.exists():
        return ["missing profile directory"]
    issues = []
    for profile in sorted(root.glob("*.yaml")):
        data = yaml.safe_load(profile.read_text())
        hooks = data.get("hooks", {}) if isinstance(data, dict) else {}
        script = hooks.get("precheck")
        if not script:
            continue
        path = pathlib.Path(script)
        if not path.exists():
            issues.append(profile.name)
            continue
        try:
            if _run_hook(path):
                continue
        except Exception:
            pass
        issues.append(profile.name)
    return issues
