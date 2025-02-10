
serv={"server1":True,"server2":False}
y=True
while y:
    x=input("give me server name: ")
    try:
        n=serv[x]
        if n:s
            print("server running:",n)
            y=False
    except:
        print("not a valid server name")

    # try:
    #     if (x in serv.keys()):
    #         print("server status:", serv[x])
    #         y=False
    # except Exception as err:
    #         print(err)