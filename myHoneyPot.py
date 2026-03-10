#imports
import logging
from logging.handlers import RotatingFileHandler

#constants
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
max_log_size = 1024 * 1024 # 1 MB
backup_count = 5

# Initialize loggers
# 1. AUTHENTICATION INTELLIGENCE LOGGER
auth_intel = logging.getLogger("auth_intel")
auth_intel.setLevel(logging.INFO)
auth_handler = RotatingFileHandler('auth_auditor.log', maxBytes=max_log_size, backupCount=backup_count)
auth_handler.setFormatter(logging.Formatter(log_format))
auth_intel.addHandler(auth_handler)

# 2. COMMAND INTELLIGENCE LOGGER
cmd_intel = logging.getLogger("cmd_intel")
cmd_intel.setLevel(logging.INFO)
cmd_handler = RotatingFileHandler('cmd_auditor.log', maxBytes=max_log_size, backupCount=backup_count)
cmd_handler.setFormatter(logging.Formatter(log_format))
cmd_intel.addHandler(cmd_handler)

