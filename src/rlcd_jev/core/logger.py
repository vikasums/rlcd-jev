"""
Structured logging module for Enterprise Compliance Firewall.
"""

import logging
import sys
import os

def setup_logger(name: str = "rlcd_jev", level: str = "INFO") -> logging.Logger:
    log_level = getattr(logging, os.getenv("LOG_LEVEL", level).upper(), logging.INFO)
    
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
    return logger

logger = setup_logger()
