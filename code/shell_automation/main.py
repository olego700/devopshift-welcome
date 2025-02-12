import subprocess

def get_folder_contant():
    try:
        p=subprocess.run(["wsl","ls","-l","/var/log"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        output_bytes=p.stdout
        output_str= output_bytes.decode()
        print(output_str)
        output_err=p.stderr
        err_output= output_err.decode()
        print(err_output)
    except PermissionError:
        print("no premissions")
        
    except FileNotFoundError:
        
        print("no such file")

p=subprocess.run(["wsl","systemctl","status","nginx"])
