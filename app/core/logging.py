import logging
from datetime import datetime
from pathlib import Path

# Create logs directory if it doesn't exist
logs_dir = Path("/tmp/logs")
logs_dir.mkdir(parents=True, exist_ok=True)


# Configure logging
def setup_logging():
    log_file = logs_dir / f"transparency_{datetime.now().strftime('%Y-%m-%d')}.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(),
        ],
    )
    
    for logger_name in [
        "weasyprint",
        "fontTools",
        "fontTools.subset",
        "fontTools.subset.timer",
        "fontTools.ttLib.ttFont",
        "PIL",
        "cssselect",
        "cffi",
        "cairocffi"
    ]:
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.CRITICAL)  # 50
        logger.propagate = False  # Prevent propagation to parent loggers
        logger.addHandler(logging.NullHandler())

    # Create logger
    logger = logging.getLogger("transparency_kenya")
    return logger


logger = setup_logging()
