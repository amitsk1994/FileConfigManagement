import difflib
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from netmiko import ConnectHandler

ip='10.10.10.2'
device_type='arista_eos'
username='admin'
password='python'
command='show running'


session=ConnectHandler(device_type=device_type,ip=ip,username=username,password=password,global_delay_factor=3)
enable=session.enable()
output=session.send_command(command)

#yesterday file for comparison
device_cfg_old='cfgfiles/'+ip+'_'+(datetime.date.today()-datetime.timedelta(days=1)).isoformat()

#cmd output for a file for today
with open('cfgfiles/'+ip+'_'+datetime.date.today().isoformat(),'w') as device_cfg_new:
    device_cfg_new.write(output+'\n')

with open(device_cfg_old, 'r') as old_file, open('cfgfiles/' + ip + '_' + datetime.date.today().isoformat(), 'r') as new_file:
    difference = difflib.HtmlDiff().make_file(fromlines = old_file.readlines(), tolines = new_file.readlines(),
     fromdesc = 'Yesterday', todesc = 'Today')


# to send email

fromaddr='yourmail@gmail.com'
toaddr='destmail@gmail.com'

msg=MIMEMultipart()
msg['From']=fromaddr
msg['To']=toaddr
msg['Subject']="Daily Configuration Management Report"
msg.attach(MIMEText(difference,'html'))

server=smtplib.SMTP('smtp.gmail.com',587)

server.starttls()
server.login('mailid','your password')
erver.sendmail(fromaddr,toaddr,msg.as_string())
server.quit()

#sudo crontab -e    -cmd to setup scheduled email
#0 5 * * * cd/home/configMgmt && sudo python3 config.property
#above command on crontab
#sudo chmod 755 cd/home/configMgmt/config.py
