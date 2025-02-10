import os
import sys
import logging
import json

log_level=os.environ.get("LOG_LEVEL","DEBUG")
log_format=os.environ.get("LOG_FORMAT","text")

class JSONFormatter(logging.Formatter):
    def format(self,record):
        log={"level":record.levelname,"time:":self.formatTime(record,self.datefmt),"message:":record.getMessage()}
        return json.dumps(log)

logger=logging.getLogger(__name__)
logger.setLevel(log_level)
stdout_handler=logging.StreamHandler(sys.stdout)

if (log_format=="json"):
    stdout_handler.setFormatter(JSONFormatter())
else:
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    stdout_handler.setFormatter(formatter)
logger.addHandler(stdout_handler)

logger.info("info")
logger.error("ok")