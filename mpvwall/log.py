import logging
from pathlib import Path

LOG_DIR = Path.home() / ".local/state/mpvwall"
LOG_FILE = LOG_DIR / "mpvwall.log"

def setup_logging(debug: bool = False):
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8")
        ]
    )
