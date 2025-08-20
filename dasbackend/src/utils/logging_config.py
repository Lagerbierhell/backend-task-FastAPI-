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
        logging.basicConfig(level=logging.INFO)
        logging.warning(f"Login Konfiguration nicht gefunden: {config_path}. Nutze die basics.")

#immer aufrufen bevor fastapi läuft im main.py ! 
setup_logging()