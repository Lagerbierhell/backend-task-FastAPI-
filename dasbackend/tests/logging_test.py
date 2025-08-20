import os
import logging
from src.utils.logging_config import setup_logging


# Setup logging
setup_logging()

# Set environment
os.environ['ENVIRONMENT'] = 'development'  # or 'production', depending on your needs



# Test different log levels
logger = logging.getLogger(__name__)

logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")

# Test with context
logger.info("User action", extra={
    "user_id": 123,
    "action": "login",
    "ip": "192.168.1.1"
})