import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(Subject: str, Body: str, destination_email: str):
    '''
    Functions that forms and sends a email
    Paramaters:
    Subject: Subject line of the email
    Body: Body of the email
    destination_email: email adress where email is to be sent 
    '''
    # Team email and password
    email = 'piguardian.l2g6@gmail.com'
    password = 'pllh vkut mexf kbdx'
    
    # This part creates the email message 
    email_message = MIMEMultipart()
    email_message['From'] = email
    email_message['To'] = destination_email
    email_message['Subject'] = Subject
    
    email_message.attach(MIMEText(Body))
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(email,password)
        server.send_message(email_message)
    
    

    