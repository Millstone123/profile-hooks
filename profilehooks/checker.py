"""Validate structured records using configured profile hooks."""
import pathlib
import subprocess

import yaml


def _command(entry):
    command = entry.get("precheck")
    if not command:
        return True
    result = subprocess.run(
        command,
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


def check_profiles(directory="profiles"):
    """Return names of profiles whose preflight hooks fail."""
    root = pathlib.Path(directory)
    if not root.exists():
        return ["missing profile directory"]
    issues = []
    for profile in sorted(root.glob("*.yaml")):
        data = yaml.safe_load(profile.read_text())
        hooks = data.get("hooks", {}) if isinstance(data, dict) else {}
        if _command(hooks):
            continue
        issues.append(profile.name)
    return issues
