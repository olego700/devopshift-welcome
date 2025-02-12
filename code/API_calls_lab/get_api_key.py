import httpx
from time import sleep

header={"Authorization": "Bearer YOUR_API_KEY"}
metrics="cpu,memory"


for i in range(3):
    try:
        r=httpx.get(f"https://api.example.com/system/metrics?{metrics}",headers=header)
        r.raise_for_status
        print(r.json)
        print(f"attempt number {i+1}")
        if(r.status_code==200):
            print("ye boi")
        elif (r.status_code==401):
            print("invalid api key")  
        elif(r.status_code==500):
            print("server is curretly down")
            pass
    except:
        print(f"attempt number {i+1}")
        print("retrying in 2 seconds...")
        sleep(2)
        if(i==2):
            print("all attempts failed")
            break