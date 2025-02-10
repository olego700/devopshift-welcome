import os
import sys
import logging
import json



class JSONFormatter(logging.Formatter):
    def format(self,record):
        log={
        "level":record.levelname,
        "time:":self.formatTime(record,self.datefmt),
        "message:":record.getMessage()
        }
        return json.dumps(log)
def setup_logging():
    log_level=os.environ.get("LOG_LEVEL","DEBUG")
    log_format=os.environ.get("LOG_FORMAT","text")

    logger=logging.getLogger(__name__)
    logger.setLevel(log_level)
    stdout_handler=logging.StreamHandler(sys.stdout)
    file_handler=logging.FileHandler("log.txt")

    if (log_format=="json"):
        formatter=JSONFormatter()
    else:
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        
    stdout_handler.setFormatter(formatter)    
    logger.addHandler(stdout_handler)
    # file_handler.setFormatter(formatter)    
    # logger.addHandler(file_handler)
    return logger
