import paramiko

def read_router_list(file_name):
    with open(file_name, 'r') as file:
        return [line.strip() for line in file if line.strip()]


def read_login(file_name):
    with open(file_name, 'r') as file:
        login_data = file.readlines()
        username = login_data[0].strip()
        password = login_data[1].strip()
        port = int(login_data[2].strip())
        return username, password, port


def read_config(file_name):
    with open(file_name, 'r') as file:
        return [line.strip() for line in file if line.strip()]    


def log_result(router_ip, commands, output, error):
    with open('result.txt', 'a') as file:
        file.write(f"Router IP: {router_ip}\n")
        file.write("Commands:\n")
        for command in commands:
            file.write(f"{command}\n")
        file.write("Output:\n")
        file.write(output + '\n')
        file.write("Error:\n")
        file.write(error + '\n')
        file.write("-" * 50 + '\n')  

def on_router(router_ip, username, password, port, commands):
    try:
        
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(router_ip, username=username, password=password, port=port, timeout=3)
        
        
        for command in commands:
            stdin, stdout, stderr = ssh.exec_command(command)
            output = stdout.read().decode()
            error = stderr.read().decode()
            
            
            log_result(router_ip, commands, output, error)
            
            if output:
                print(f"Output from {router_ip}: {output}")
            if error:
                print(f"Error from {router_ip}: {error}")
        
        ssh.close()
        
    except Exception as e:
        print(f"Error connecting to {router_ip}: {e}")
        log_result(router_ip, [], '', f"Error connecting: {e}")


routers = read_router_list('router.txt')
username, password, port = read_login('login.txt')  
commands = read_config('config.txt')


for router_ip in routers:
    print(f"Connecting to {router_ip}...")
    on_router(router_ip, username, password, port, commands)

print("Operation completed. Check result.txt for details.")
