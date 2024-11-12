from email.message import EmailMessage
import smtplib
def email_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to

    user = "rasppi39@gmail.com"
    msg['from'] = user
    password = "ezyittzjooqgwptb"


    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)

    server.quit()

if __name__ == '__main__':
    email_alert("Home Security System Alert", "Your home has been invaded!", "sakari.heinio@gmail.com")

