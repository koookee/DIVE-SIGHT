import smtplib
from email.message import EmailMessage
def email_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to  
  
    user = "brainerdesther@gmail.com"
    msg['from'] = user
    password = "christopher*2000"
    
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user,password)
    server.send_message(msg)
    
    server.quit()

email_alert("hey", "Hello world","brainerdesther@gmail.com")

