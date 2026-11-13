#!/usr/bin/env python3
"""Download the pinned mdBook tools into .tools/bin (ignored by git).

    python scripts/install_tools.py

The versions and checksums below are the only place the book's toolchain is pinned; `make install`
and CI both run this script. An archive whose SHA-256 does not match is rejected. The script needs
only Python 3 and works on Linux, macOS and Windows. To upgrade, change a version, download the new
archives from the release page, and replace the checksums (`shasum -a 256 <file>`).
"""

from __future__ import annotations

import hashlib
import io
import platform
import shutil
import stat
import subprocess
import sys
import tarfile
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
BIN = REPO / ".tools" / "bin"

TOOLS = {
    "mdbook": {
        "version": "0.5.4",
        "url": "https://github.com/rust-lang/mdBook/releases/download/v{version}/mdbook-v{version}-{target}.{ext}",
        "sha256": {
            "x86_64-unknown-linux-gnu": "3f28de05dafca9d0f2eab99c662116b0e37b89b1d96a08f8f430b9eeae958cd7",
            "aarch64-unknown-linux-musl": "753e5c5c363ee8a56972344dcf91466f005a51db84a7aeffe427ae3ef83d6d44",
            "x86_64-apple-darwin": "a47d7bf0d5d670cff9ee6cce95537cbeb62dc10704d9e7131ffbd13e2b59a5de",
            "aarch64-apple-darwin": "03e8a6d8b13a2971e0b3280affd03b388373c1485e26f73407c3a76b0b1838df",
            "x86_64-pc-windows-msvc": "8a6b2421aa522de06d746871d2b8fff9c8d71773467e310a4516d2566e7f2de4",
        },
    },
    "mdbook-mermaid": {
        "version": "0.17.1",
        "url": "https://github.com/badboy/mdbook-mermaid/releases/download/v{version}/mdbook-mermaid-v{version}-{target}.{ext}",
        "sha256": {
            "x86_64-unknown-linux-gnu": "9afcfa5b8463afe606d48595a7ae338564302903e626ea5b6edb8007d29393a5",
            "aarch64-unknown-linux-musl": "b1782ecaf775bfbe069dead6cdd8ac7cc739d5e62d138bd0e800efec6467cf3a",
            "x86_64-apple-darwin": "9b752cc4f26251eaa5d85564345a6f7c8447a922ba6acbfa6ee4f2a17a68ef7e",
            "aarch64-apple-darwin": "5be76bfffefd36efe5abf876c52530ba03c16df5f44c94164cc9ca88d16df1e1",
            "x86_64-pc-windows-msvc": "bb1e3d99d06e799d4a95a7e6beb6e8e041ba2c3b1528185e873f3f751e52feb5",
        },
    },
}

TARGETS = {
    ("Linux", "x86_64"): "x86_64-unknown-linux-gnu",
    ("Linux", "aarch64"): "aarch64-unknown-linux-musl",
    ("Darwin", "x86_64"): "x86_64-apple-darwin",
    ("Darwin", "arm64"): "aarch64-apple-darwin",
    ("Windows", "AMD64"): "x86_64-pc-windows-msvc",
}


def installed_version(binary: Path) -> str | None:
    marker = binary.with_name(binary.name + ".version")
    return marker.read_text().strip() if binary.exists() and marker.exists() else None


def download(url: str) -> bytes:
    """Fetch a URL with Python, or with curl when Python has no usable certificate store.

    (The python.org installer for macOS ships without root certificates until the user runs its
    "Install Certificates" command.) The caller checks the SHA-256 either way.
    """
    try:
        with urllib.request.urlopen(url, timeout=120) as response:
            return response.read()
    except urllib.error.URLError as error:
        curl = shutil.which("curl")
        if curl is None:
            sys.exit(f"Cannot download {url}: {error.reason}")
        print(f"  Python could not download it ({error.reason}); trying curl.")
        result = subprocess.run([curl, "-fsSL", "--max-time", "300", url], capture_output=True)
        if result.returncode != 0:
            sys.exit(f"Cannot download {url}: {result.stderr.decode(errors='replace').strip()}")
        return result.stdout


def install(name: str, tool: dict, target: str) -> None:
    windows = target.endswith("windows-msvc")
    member = name + (".exe" if windows else "")
    binary = BIN / member
    if installed_version(binary) == tool["version"]:
        print(f"{name} {tool['version']} is already installed.")
        return

    url = tool["url"].format(version=tool["version"], target=target, ext="zip" if windows else "tar.gz")
    print(f"Downloading {url}")
    archive = download(url)
    digest = hashlib.sha256(archive).hexdigest()
    if digest != tool["sha256"][target]:
        sys.exit(f"{name}: checksum mismatch for {url}\n  expected {tool['sha256'][target]}\n  got      {digest}")

    if windows:
        with zipfile.ZipFile(io.BytesIO(archive)) as bundle:
            data = bundle.read(member)
    else:
        with tarfile.open(fileobj=io.BytesIO(archive), mode="r:gz") as bundle:
            data = bundle.extractfile(member).read()
    BIN.mkdir(parents=True, exist_ok=True)
    binary.write_bytes(data)
    binary.chmod(binary.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    binary.with_name(binary.name + ".version").write_text(tool["version"] + "\n")
    print(f"Installed {name} {tool['version']} to {binary.relative_to(REPO)}")


def main() -> int:
    key = (platform.system(), platform.machine())
    target = TARGETS.get(key)
    if target is None:
        versions = ", ".join(f"{name} {tool['version']}" for name, tool in TOOLS.items())
        sys.exit(f"No prebuilt tools for {key[0]} {key[1]}. Install these versions yourself and put them in .tools/bin: {versions}.")
    for name, tool in TOOLS.items():
        install(name, tool, target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
