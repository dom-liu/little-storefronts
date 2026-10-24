"""Create two independent download ZIPs; never overwrite a previous delivery."""

import hashlib
import sys
from datetime import datetime, timezone
from zipfile import ZIP_DEFLATED, ZipFile

sys.dont_write_bytecode = True

from check import ROOT, THEMES, verify

verify()
stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
destination = ROOT / "out" / f"0.1.0-{stamp}"
destination.mkdir(parents=True)
checksums = []
for theme in THEMES:
    archive = destination / f"{theme}-v0.1.0.zip"
    with ZipFile(archive, "x", compression=ZIP_DEFLATED, compresslevel=9) as zipped:
        for file in sorted((ROOT / theme).rglob("*")):
            if file.is_file():
                zipped.write(file, file.relative_to(ROOT))
    with ZipFile(archive) as zipped:
        if zipped.testzip() is not None:
            raise ValueError(f"Archive verification failed: {archive.name}")
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    checksums.append(f"{digest}  {archive.name}")
(destination / "SHA256SUMS.txt").write_text("\n".join(checksums) + "\n")
print(f"Download packages: {destination}")
