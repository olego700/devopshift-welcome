import logging
import json
import os
import sys

# Set log format dynamically
LOG_LEVEL=os.environ.get("LOGLEVEL","DEBUG")
LOG_FORMAT = os.environ.get("LOG_FORMAT", "json")  # 'json' or 'text'

# Create a JSON formatter class
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "level": record.levelname,
            "timestamp": self.formatTime(record, self.datefmt),
            "message": record.getMessage(),
        }
        return json.dumps(log_record)

logger=logging.getLogger("serverapp")

# Configure logging
# logging.basicConfig(
#     level=logging.INFO,
#     # handlers=[logging.StreamHandler(sys.stdout)]
# )
logger.setLevel(LOG_LEVEL)
handler=logging.StreamHandler(sys.stdout)
# Apply the appropriate formatter
if LOG_FORMAT == "json":
    formatter = JSONFormatter()
else:
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

for handler in logging.getLogger().handlers:
    handler.setFormatter(formatter)

logger.addHandler(handler)
# Test logs
logger.info("Dynamic logging format enabled")

serv={"server1":True,"server2":False}
y=True
while y:
    x=input("give me server name: ").strip()
    logging.info(x)
    try:
        n=serv[x]
        if n:
            logger.info("server running")
            
            # y=False
    except:
        logger.error("not a valid server name")
