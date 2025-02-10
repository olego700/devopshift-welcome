from log import setup_logging


logger=setup_logging()


serv={"server1":True,"server2":False}

def get_server_status(server_name:str)-> bool:
    # if (server_name=="exit"):
    #     y=False
    #     return
    try:
        status=serv[server_name]
    except KeyError:
        logger.error("server does not exist")
    else:
        logger.info("server status is:"+ str(status))


y=True
while y:
    server_name=input("give me server name: ").strip()
    status=get_server_status(server_name)
    