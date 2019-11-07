from urllib.request import urlopen
import re
import smtplib

# Setup our login credentials
from_address = 'etipiserver@gmail.com'
to_address = 'etiennebourke@gmail.com'
subject = 'etipi IP address'
username = 'etipiserver@gmail.com'
password = 'Clopiclopi1'

# Setup where we will get our IP address
url = 'http://checkip.dyndns.org'
print ("Our chosen IP address service is: ", url)

# Open up the url, then read the contents, and take away to IP address
request = urlopen(url).read().decode('utf-8')

# We extract the IP address only
ourIP = re.findall("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", request)
ourIP = str(ourIP)
print("Our IP address is ", ourIP)

def send_email(ourIP) :
        #Body of the mail
        body_text = ourIP + ' is our etipi IP address'
        msg = '\r\n'.join(['To: %s' % to_address,
                                'From: %s' % from_address,
                                'Subject: %s' % subject,
                                '', body_text])

        # Actually send the email
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls() # Our security for transmission of credentials
        server.login(username,password)
        server.sendmail(from_address, to_address, msg)
        server.quit()
        print ("Our email has been sent!")
        
# Open up last_ip.txt, and extract the contents
with open ('/home/pi/Desktop/Projet3/sshServer/email_IP_address/last_ip.txt', 'rt') as last_ip:
        last_ip = last_ip.read() # Read the text file

# Check if our IP address has changed
if last_ip == ourIP:
        print ("Our IP address have not changed.")
else:
        print ("We have a new IP address.")
        with open ('/home/pi/Desktop/Projet3/sshServer/email_IP_address/last_ip.txt', 'wt') as last_ip:
                last_ip.write(ourIP)
        print ("We have written our new IP address.")
        send_email(ourIP)
