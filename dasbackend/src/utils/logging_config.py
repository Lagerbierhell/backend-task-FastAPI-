import json
import logging.config
import os

def setup_logging():
    env = os.getenv('ENVIRONMENT', 'dev')
    config_path = f'config/logging_{env}.json'
    
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
        os.makedirs('logs', exist_ok=True)
        logging.config.dictConfig(config)
    else:
        # Basic fallback configuration
        logging.basicConfig(level=logging.INFO)
        logging.warning(f"Logging config file not found: {config_path}. Using basic config.")

# Call this early in your application startup
setup_logging()