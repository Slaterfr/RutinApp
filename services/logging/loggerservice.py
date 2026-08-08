import logging

logging.basicConfig(
    level=logging.INFO,
    format="""

%(asctime)s
%(levelname)s
%(message)s
""",
    force=True
)

logger = logging.getLogger("gym-api")