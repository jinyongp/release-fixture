#!/usr/bin/env python3
import gzip
import io
import os
from pathlib import Path
import tarfile
import sys

PLATFORMS = (
    "macos-arm64",
    "macos-x86_64",
    "linux-arm64",
    "linux-x86_64",
)


def archive_bytes(version: str, platform: str) -> bytes:
    executable = (
        "#!/usr/bin/env sh\n"
        "set -eu\n"
        'if [ "${1:-}" = "--version" ]; then\n'
        f'  echo "release-fixture {version} {platform}"\n'
        "  exit 0\n"
        "fi\n"
        f'echo "release-fixture {platform}"\n'
    ).encode()

    compressed = io.BytesIO()
    with gzip.GzipFile(fileobj=compressed, mode="wb", filename="", mtime=0) as gz:
        with tarfile.open(fileobj=gz, mode="w", format=tarfile.USTAR_FORMAT) as tar:
            info = tarfile.TarInfo("release-fixture")
            info.size = len(executable)
            info.mode = 0o755
            info.mtime = 0
            info.uid = 0
            info.gid = 0
            info.uname = ""
            info.gname = ""
            tar.addfile(info, io.BytesIO(executable))
    return compressed.getvalue()


def main() -> None:
    if len(sys.argv) > 2:
        raise SystemExit("usage: build-fixtures.py [VERSION]")
    version = sys.argv[1] if len(sys.argv) == 2 else os.environ.get("VERSION", "")
    if not version:
        raise SystemExit("VERSION is required")

    output = Path("dist")
    output.mkdir(exist_ok=True)
    for old in output.glob("release-fixture_*.tar.gz"):
        old.unlink()

    for platform in PLATFORMS:
        name = platform.replace("-", "_")
        (output / f"release-fixture_{name}.tar.gz").write_bytes(
            archive_bytes(version, platform)
        )


if __name__ == "__main__":
    main()
