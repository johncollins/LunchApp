from email.mime.text import MIMEText
import smtplib

host = '10.7.7.6'
port = 25
me = 'lunchappadmin@archimedesmodel.com'

def send_signup_success_email(person, month):
	content = "Congratualtions %s\n\nYou have successfully been signed up for randomized group lunches for the month of %s\n\nThe lunch app team" % (person, month)
	
	message = MIMEText(content)
	message['subject'] = "Lunches signup for %s" % month
	message['from'] = me
	message['to'] = person.email

	server = smtplib.SMTP(host, port)
	server.sendmail(message['from'], [message['to']], message.as_string())
	server.quit()
		
	return
	
def send_removal_success_email(person, month):
	content = "Congratualtions %s\n\nYou have successfully been removed from participation in randomized group lunches for the month of %s\n\nThe lunch app team" % (person, month)
	
	message = MIMEText(content)
	message['subject'] = "Lunches non-participation for %s" % month
	message['from'] = me
	message['to'] = person.email

	server = smtplib.SMTP(host, port)
	server.sendmail(message['from'], [message['to']], message.as_string())
	server.quit()
		
	return