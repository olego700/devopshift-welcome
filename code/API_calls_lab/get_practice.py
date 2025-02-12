import httpx

num=input("enter user id:").strip()
r=httpx.get(f"https://jsonplaceholder.typicode.com/users/{num}")
print(r.status_code)
if r.status_code==200:
    print(r.text) 
if r.status_code==404:
    print("user not found")
if r.status_code==500:
    print("server error, please try again")
# users=r.text
# print(users)



# for user in users:
#     if(num==user[id]):
        
