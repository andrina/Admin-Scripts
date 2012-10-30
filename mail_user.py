#!//usr/bin/python
# settings

SUBJECT = ' - Your Boot Drive Has Less Than 85% Free Space'
SMTP_SERVER = 'mail.yourserver.ca'
SMTP_PORT = 25
SMTP_FROM = 'mailaccount@yourserver.ca'

MESSAGE = """***This is an automatically generated message*** 
Your boot drive is running dangerously low on disk space.
Please take the time to clean up and remove any unnecessary files to free up space. 
You will continue to get this message once a day until your boot disk is less than 85% full.

Thanks,
Your ever dedicated and subservient IT department... No really, we mean it...
mailaccount@yourserver.ca
"""

# now construct the message
import smtplib, email
from email import encoders
import os
import subprocess

scutil = subprocess.Popen("scutil --get LocalHostName", shell=True, stdout=subprocess.PIPE)
hostname = scutil.communicate()[0]
host = hostname.rstrip()

p = subprocess.Popen("who | awk '/console/{print $1}'", shell=True, stdout=subprocess.PIPE)
whoami = p.communicate()[0]
username = whoami.rstrip()

if username == "":
	print('No user logged in')
	
else:	
	p = subprocess.Popen(["dscl /Active\ Directory/YOURDOMAIN/All\ Domains -read /Users/" + username, "EmailAddress"], shell=True, stdout=subprocess.PIPE)
	dscl_out = p.communicate()[0]
	list = dscl_out.split("\n")
 
	for pos,item in enumerate(list):
 		if "EMailAddress:" in item:
 			dump = list[pos].replace(" ", "")
 		
	userEmail = dump.replace('EMailAddress:','')

	msg = email.MIMEMultipart.MIMEMultipart()
	body = email.MIMEText.MIMEText(MESSAGE)
	msg.attach(body)
	msg.add_header('Subject', host + SUBJECT)
	msg.add_header('From', SMTP_FROM)
	msg.add_header('To', userEmail)
	
# now send the message
	mailer = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
	mailer.sendmail(SMTP_FROM, [userEmail], msg.as_string())
	mailer.close()