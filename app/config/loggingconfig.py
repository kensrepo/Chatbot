import logging
import logging.config
from logging.handlers import TimedRotatingFileHandler
import os
from config.chatbotconfig import buildChatBotConfig

req_config_variables = buildChatBotConfig()

log_dir = req_config_variables.get('LOG_DIR')
os.makedirs(log_dir, exist_ok=True)
log_file_path = os.path.join(log_dir, "app.log")
logging_setup = {
    "version": 1,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] [%(levelname)s] [%(name)s:%(lineno)d] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },
    "handlers": {
        "file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": log_file_path,
            "when": "D",
            "interval": 3,
            "backupCount": 7,
            "encoding": "utf-8",
            "formatter": "default"
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default"
        }
    },
    "root": {
        "level": req_config_variables.get('LOG_LEVEL').upper(),
        "handlers": ["file","console"]
    }
}
    