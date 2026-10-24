"""Verify the two static deliveries using only Python's standard library."""

import base64
import hashlib
import json
import re
import struct
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
THEMES = ("pumpkin-hollow", "blueberry-cove")
RESPONSIVE_PHOTOS = {
    "pumpkin-hollow": ("spice-latte-small.png", "apple-cider-small.png"),
    "blueberry-cove": (
        "blueberry-latte-small.png", "blueberry-pie-small.png",
        "blueberry-jar-small.png", "lemonade-small.png",
    ),
}


class LocalReferences(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paths = []

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name in ("src", "href") and value:
                target = urlsplit(value)
                if not target.scheme and not target.netloc and target.path:
                    self.paths.append(unquote(target.path))


def verify():
    for theme in THEMES:
        folder = ROOT / theme
        manifest = json.loads((folder / "package-manifest.json").read_text())
        listed = set()
        for entry in manifest["files"]:
            relative = Path(entry["file"])
            if relative.is_absolute() or ".." in relative.parts:
                raise ValueError(f"Unsafe manifest path: {relative}")
            if entry["file"] in listed:
                raise ValueError(f"Duplicate manifest path: {relative}")
            listed.add(entry["file"])
            data = (folder / relative).read_bytes()
            if len(data) != entry["bytes"] or hashlib.sha256(data).hexdigest() != entry["sha256"]:
                raise ValueError(f"Manifest mismatch: {theme}/{relative}")
        actual = {
            str(p.relative_to(folder)) for p in folder.rglob("*")
            if p.is_file() and p.name != "package-manifest.json"
        }
        if actual != listed:
            raise ValueError(f"Unlisted or missing files: {theme}: {actual ^ listed}")
        for name in ("index.html", "app.js", "style.css", "shop-config.js",
                     "assets/model-data.js", "README.html", "PROVENANCE.html"):
            if name not in listed:
                raise ValueError(f"Missing required file: {theme}/{name}")
        payload = (folder / "assets/model-data.js").read_text().split(
            "window.LITTLE_STOREFRONTS_MODELS = ", 1
        )[1].strip().removesuffix(";")
        models = json.loads(payload)
        if len(models) != 7:
            raise ValueError(f"Expected seven embedded models in {theme}")
        for name, value in models.items():
            if not re.fullmatch(r"\./assets/models/[a-z0-9-]+\.glb", name):
                raise ValueError(f"Unexpected embedded model path: {name}")
            if not value.startswith("data:") or ";base64," not in value:
                raise ValueError(f"Model must be embedded: {name}")
            data = base64.b64decode(value.split(",", 1)[1], validate=True)
            if len(data) < 20:
                raise ValueError(f"Truncated GLB: {name}")
            magic, version, size, json_size, json_type = struct.unpack("<5I", data[:20])
            if (magic, version, size, json_type) != (0x46546C67, 2, len(data), 0x4E4F534A):
                raise ValueError(f"Invalid GLB: {name}")
            gltf = json.loads(data[20:20 + json_size])
            for resource in gltf.get("images", []) + gltf.get("buffers", []):
                if resource.get("uri") and not resource["uri"].startswith("data:"):
                    raise ValueError(f"External model resource: {name}")
        for html in folder.glob("*.html"):
            references = LocalReferences()
            references.feed(html.read_text())
            for path in references.paths:
                resolved = (html.parent / path).resolve()
                if not resolved.is_relative_to(folder.resolve()) or not resolved.is_file():
                    raise ValueError(f"Missing or unsafe HTML reference: {theme}/{path}")
        config = json.loads((folder / "shop-config.js").read_text().split(
            "window.SHOP_CONFIG = ", 1
        )[1].strip().removesuffix(";"))
        for item in config["menu"]:
            image = folder / item["image"]
            if not image.resolve().is_relative_to(folder.resolve()) or not image.is_file():
                raise ValueError(f"Missing menu photo: {theme}/{item['image']}")
        # The existing bundle selects these dynamically through image srcset.
        for name in RESPONSIVE_PHOTOS[theme]:
            if f"assets/photos/{name}" not in listed:
                raise ValueError(f"Missing responsive photo: {theme}/{name}")
        for p in folder.rglob("*"):
            if p.is_file() and (p.suffix in (".tsx", ".ts", ".blend", ".map") or p.name.startswith(".env")):
                raise ValueError(f"Unexpected development file: {p}")
        print(f"{theme}: {len(listed)} delivered files verified")
    for name in ("README.md", "README.zh-CN.md", "CREDITS.md", "ASSET_LICENSE.md"):
        for link in re.findall(r"\]\(([^)]+)\)", (ROOT / name).read_text()):
            target = urlsplit(link)
            if not target.scheme and not target.netloc and target.path:
                if not (ROOT / unquote(target.path)).exists():
                    raise ValueError(f"Broken documentation link: {name}: {link}")


if __name__ == "__main__":
    verify()
