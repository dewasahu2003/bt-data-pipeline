import logging
import colorlog

# Define a custom log format with colors
log_colors = {
    "DEBUG": "cyan",
    "INFO": "green",
    "WARNING": "yellow",
    "ERROR": "red",
    "CRITICAL": "bold_red",
}
formatter = colorlog.ColoredFormatter(
    "%(asctime)s [%(log_color)s%(levelname)s%(reset)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    log_colors=log_colors,
)

# Configure the root logger to use colorized output
logging.basicConfig(
    level=logging.INFO, format="%(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
root_logger = logging.getLogger()
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
root_logger.addHandler(stream_handler)

# Create a logger
logger = logging.getLogger(__name__)
