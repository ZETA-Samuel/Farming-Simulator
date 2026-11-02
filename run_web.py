import re
import subprocess
import sys
from pathlib import Path
from urllib.request import urlopen

from pygbag.app import DEFAULT_CDN, VERSION


PROJECT_DIR = Path(__file__).resolve().parent
TEMPLATE_PATH = PROJECT_DIR / "build" / f"farming-simulator-{VERSION}.tmpl"


def strip_browserfs_script(template: str) -> str:
    """Remove outdated BrowserFS bootstrapping from pygbag's default template.

    In browser builds, this stale script can leave the page stuck on the
    "Loading, please wait ..." spinner even though the game itself is fine.
    """
    patterns = [
        r"(?is)<script\b[^>]*browserfs\.min\.js[^>]*>\s*</script>",
        r"(?is)<script\b[^>]*BrowserFS[^>]*>.*?</script>",
    ]
    cleaned = template
    for pattern in patterns:
        cleaned = re.sub(pattern, "", cleaned)
    return cleaned


def main():
    with urlopen(f"{DEFAULT_CDN}default.tmpl", timeout=30) as response:
        template = response.read().decode("utf-8")

    template = strip_browserfs_script(template)
    TEMPLATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    TEMPLATE_PATH.write_text(template, encoding="utf-8")

    subprocess.run(
        [
            sys.executable,
            "-m",
            "pygbag",
            "--template",
            str(TEMPLATE_PATH),
            str(PROJECT_DIR),
        ],
        cwd=PROJECT_DIR,
        check=True,
    )


if __name__ == "__main__":
    main()
