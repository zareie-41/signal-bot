import logging
import os

def setup_logger():
    logger = logging.getLogger('SignalBot')
    logger.setLevel(logging.INFO)
    
    # Clear any existing handlers
    logger.handlers = []
    
    # Prevent propagation to avoid duplicate logs
    logger.propagate = False
    
    # Create logs directory if it doesn't exist
    os.makedirs('data/logs', exist_ok=True)
    
    # File handler
    file_handler = logging.FileHandler('data/logs/bot.log')
    file_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    # Console handler for debugging
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    return logger
