from fastapi import FastAPI
from models import ServerStatusResponse, Server
from models import read_server_list,add_new_server
app = FastAPI()

servers=read_server_list("servers_file.txt")
# for i in range(len(servers)):
    


@app.get("/server")
def get_server(server_name: str) -> ServerStatusResponse:
    servers=read_server_list("servers_file.txt")
    for server in servers:
        if server_name == server.name:
            return ServerStatusResponse(server_name=server.name, server_status=server.online)
            
    return ServerStatusResponse(server_name=server_name, server_status="server not found")


@app.post("/server")
def create_server(server_name: str,staus:bool,cpus:int ,ram:int) -> ServerStatusResponse:
    servers=read_server_list("servers_file.txt")
    for server in servers:
        if server_name==server.name:
            return ServerStatusResponse(server_name=server.name, server_status="Name already exists")
            
    new_server=Server(name=server_name,online=staus,cpus=cpus,ram=ram)
    add_new_server(new_server)
    return ServerStatusResponse(server_name=new_server.name, server_status="Created")