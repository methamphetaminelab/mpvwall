import sys
import logging

from mpvwall.log import setup_logging
from mpvwall.autostart import restore
from mpvwall.tui import run

def main():
    DEBUG = "--debug" in sys.argv

    setup_logging(debug=DEBUG)
    log = logging.getLogger("mpvwall")

    log.info("mpvwall started")

    if "--restore" in sys.argv:
        restore()
    else:
        run()

    log.info("mpvwall exited")


if __name__ == "__main__":
    main()
