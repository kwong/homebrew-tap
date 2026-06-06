#!/usr/bin/env python3

import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile
import urllib.request


ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / ".github" / "managed-casks.json"


def run(cmd):
    return subprocess.run(cmd, check=True, text=True, capture_output=True)


def gh_api(path):
    result = run(["gh", "api", path])
    if not result.stdout.strip():
        raise RuntimeError(f"GitHub API returned no data for {path}")
    clean_stdout = re.sub(r"\x1b\[[0-9;]*m", "", result.stdout)
    return json.loads(clean_stdout)


def normalize_version(tag_name):
    return tag_name[1:] if tag_name.startswith("v") else tag_name


def compute_sha256(url):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_path = pathlib.Path(tmp.name)
    try:
        with urllib.request.urlopen(url) as response, tmp_path.open("wb") as fh:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                fh.write(chunk)
        digest = hashlib.sha256()
        with tmp_path.open("rb") as fh:
            while True:
                chunk = fh.read(1024 * 1024)
                if not chunk:
                    break
                digest.update(chunk)
        return digest.hexdigest()
    finally:
        tmp_path.unlink(missing_ok=True)


def latest_release(repo):
    return gh_api(f"repos/{repo}/releases/latest")


def choose_asset(release, pattern):
    version = normalize_version(release["tag_name"])
    expected_name = pattern.format(version=version)
    for asset in release.get("assets", []):
        if asset["name"] == expected_name:
            return asset
    raise RuntimeError(f"Could not find asset '{expected_name}' in release {release['tag_name']}")


def asset_sha256(asset):
    digest = asset.get("digest", "")
    if digest.startswith("sha256:"):
        return digest.split(":", 1)[1]
    return compute_sha256(asset["browser_download_url"])


def replace_once(content, pattern, replacement, path):
    updated, count = re.subn(pattern, replacement, content, count=1, flags=re.MULTILINE)
    if count != 1:
        raise RuntimeError(f"Expected one match for pattern '{pattern}' in {path}")
    return updated


def update_cask(cask_config):
    release = latest_release(cask_config["repo"])
    if release.get("draft") or release.get("prerelease"):
        raise RuntimeError(f"Latest release for {cask_config['repo']} is not publishable")

    version = normalize_version(release["tag_name"])
    asset = choose_asset(release, cask_config["asset_pattern"])
    sha256 = asset_sha256(asset)
    url = cask_config["url_template"]
    asset_url = asset["browser_download_url"]

    cask_path = ROOT / cask_config["cask_path"]
    original = cask_path.read_text()
    updated = original
    current_version = re.search(r'^\s*version\s+"(.*)"$', original, flags=re.MULTILINE).group(1)
    current_sha256 = re.search(r'^\s*sha256\s+"(.*)"$', original, flags=re.MULTILINE).group(1)
    current_url = re.search(r'^\s*url\s+"(.*)"$', original, flags=re.MULTILINE).group(1)

    if current_version != version:
        updated = replace_once(updated, r'^\s*version\s+".*"$', f'  version "{version}"', cask_path)
    if current_sha256 != sha256:
        updated = replace_once(updated, r'^\s*sha256\s+".*"$', f'  sha256 "{sha256}"', cask_path)
    if current_url != url:
        updated = replace_once(updated, r'^\s*url\s+".*"$', f'  url "{url}"', cask_path)

    if updated != original:
        cask_path.write_text(updated)
        return {
            "token": cask_config["token"],
            "repo": cask_config["repo"],
            "old_version": current_version,
            "new_version": version,
            "url": asset_url,
            "sha256": sha256,
            "path": str(cask_path.relative_to(ROOT)),
        }
    return None


def main():
    manifest = json.loads(MANIFEST_PATH.read_text())
    updates = []
    for cask in manifest["casks"]:
        result = update_cask(cask)
        if result:
            updates.append(result)

    if updates:
        print(json.dumps({"updated": updates}, indent=2))
    else:
        print(json.dumps({"updated": []}, indent=2))

    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as fh:
            if updates:
                fh.write("## Updated casks\n\n")
                for update in updates:
                    fh.write(
                        f"- `{update['token']}`: `{update['old_version']}` -> `{update['new_version']}`\n"
                    )
            else:
                fh.write("## Updated casks\n\n- No updates found.\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
