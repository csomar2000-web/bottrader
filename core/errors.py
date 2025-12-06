import sys
import traceback
from core.log import get_logger

log = get_logger("global")

def handle_uncaught(exc_type, exc, tb):
    log.error(
        "Unhandled exception",
        context={
            "type": exc_type.__name__,
            "error": str(exc),
            "trace": "".join(traceback.format_tb(tb)),
        },
    )

sys.excepthook = handle_uncaught
