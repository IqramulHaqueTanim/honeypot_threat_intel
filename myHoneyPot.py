# Imports
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

# Emulate decoy shell for attackers to interact with
def decoy_shell(channel, client_ip):
    prompt = b"\n\radmin@bd-dhaka-srv-04:~$ "
    channel.send(prompt)
    command_buffer = b""
    while True:
        char = channel.recv(1)
        if not char:
            break
        channel.send(char)  
        command_buffer += char # Accumulate command input
        if char == b"\r":
            command = command_buffer.strip().decode('utf-8', errors='ignore')
            if command == 'exit':
                channel.send(b"\n\rGoodbye!\n\r")
                channel.close()
                break
            elif command == "ls":
                channel.send(b"conf  data  logs  scripts  webroot\r\n")
            
            elif command == "pwd":
                channel.send(b"/home/admin\r\n")
                
            elif command == "whoami":
                channel.send(b"admin\r\n")
                
            elif command == "uname -a":
                channel.send(b"Linux dhaka-srv-04 5.15.0-76-generic #83-Ubuntu SMP Thu Jun 15 19:16:32 UTC 2023 x86_64 x86_64 x86_64 GNU/Linux\r\n")
            
            elif command == "id":
                channel.send(b"uid=1000(admin) gid=1000(admin) groups=1000(admin),4(adm),24(cdrom),27(sudo)\r\n")

            elif command == "":
                pass
                
            else:
                # Standard bash error for unknown commands
                channel.send(f"-bash: {command}: command not found\r\n".encode())

            # Log the command to your creds_logger (using the logic from the tutorial)
            cmd_intel.info(f"IP: {client_ip} | Command: {command}")
            
            # Reset buffer and show prompt again
            command_buffer = ""
            channel.send(prompt)
            
        elif char == b"\x7f": # Handle Backspace
            if len(command_buffer) > 0:
                command_buffer = command_buffer[:-1]
                channel.send(b"\b \b") # Erase character from terminal
        else:
            # Add character to the buffer
            command_buffer += char.decode('utf-8', errors='ignore')