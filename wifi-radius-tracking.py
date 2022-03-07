def wifi(device_ip):

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    bekci = "10.222.247.240" # buraya bağlanmak istediğiniz IP yi yazınız

    try:
        ssh.connect(device_ip, port="22", username=username, password= password, timeout=20)
        remote_connection = ssh.invoke_shell()
        print(colored("connected_ip_address_" + device_ip, "blue"))

        time.sleep(1)
        remote_connection.send( "e" + "\r")
        remote_connection.send("conf t" + "\r")
        remote_connection.send("radius-server tracking disable" + "\r")
        remote_connection.send("write memory" + "\r")
        remote_connection.send("exit" + "\r")

    except Exception as e:
        print("erisim yok_" + device_ip +"\n")
        time.sleep(2)
        with open("unreachables_CISCO.txt", "a") as f:
            f.write(device_ip + "\n")
        f.close()

global password
username = "admin"
password = "admin”

hosts = []
f1 = open('WIFI_ARUBA.txt', 'r')
devices = f1.readlines()
for i in devices:
    i = i.split()
    if len(i) != 0:
        # print(i)

        hosts.append(i[0])
#print (hosts)


q = Queue()
for host in hosts:
    q.put(host)
    break


def worker():

    while not q.empty():
        host = q.get()
        wifi(host)

        time.sleep(5)
        q.task_done()

for i in range(20):
    t = threading.Thread(target=worker)
    t.deamon = True
    t.start()

q.join()
