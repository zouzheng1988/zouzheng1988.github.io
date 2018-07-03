import time,datetime,sys

from SSH import Ssh
from Sftp import Sftp
from getDate import getDate

#ip = "10.16.1.1"
ip = "10.16.1.1"
user = "root"
passwd = "password"


sftp = Sftp(ip, username=user, password=passwd)

ssh = Ssh(ip,username=user,password=passwd)

#ssh.Exec_noreturn("./serial2tcp --config config.json")

'''
back sorce file
'''
source_path_nginx = "/etc/nginx/sites-available/demo.nginx.conf"

localname = "/home/royzou/backup/nginx/backup/" + getDate.getdatetoday()

sftp.GetFile(source_path_nginx, localname)


'''
update config file
'''
update_config_path = "/home/royzou/backup/nginx/update/update.nginx.conf"

sftp.PutFile(update_config_path, source_path_nginx)

'''
test nginx config -t
'''

# cmd = "nginx -t > /result_nginx_test"
# test_result = ssh.Exec(cmd)
# result_file_path = "/result_nginx_test"
# sftp.GetFile(result_file_path, "./result_nginx_test")
# f = open("./result_nginx_test")
# test_result = f.readlines()
# f.close()
# print(test_result)
# if "successful" in test_result:
#     print("nginx test ok")
# else:
#     print("nginx test failed ,please check config file")
#     sys.exit(1)

'''
restart nginx server
'''

cmd = "/etc/init.d/nginx restart"
test_result_service_restart = ssh.Exec(cmd)
if "failed" not in test_result_service_restart:
    print("nginx restart ok")
    print("$$$$" + str(ip) + " is ok ")
else:
    print("nginx restart failed")
    print("$$$$" + str(ip) + " is failed ")





sftp.Close()
