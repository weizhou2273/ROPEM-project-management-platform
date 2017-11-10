import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
 
def send_email(to_email,url):
	fromaddr = 'ropdemreset@gmail.com'
	toaddr = to_email
	# msg = MIMEMultipart()
	# msg['From'] = fromaddr
	# msg['To'] = toaddr
	# msg['Subject'] = 'ROPDEM project management form password reset'
	 
	body = 'Please click the url to reset your password. {}'.format(url)
	
	# msg.attach(MIMEText(body, 'plain'))
	
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, "nyulmcropdem")
	# text = msg.as_string()
	server.sendmail(fromaddr, toaddr, body)
	server.quit()