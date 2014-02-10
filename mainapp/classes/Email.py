import smtplib
import json

class Email():
    def __init__ (self):
        pass

    def send_mail(self, to, subject, message):
        sender = 'ed@foodtrade.com'
        passwd = 'NwotnhPk1Nprc6OX0Wq6vA'

        server = smtplib.SMTP('smtp.mandrillapp.com', 587)
        server.ehlo()
        server.starttls()
        server.login(sender, passwd)

        template_content = {"template_content": [
        {
            "name": "title",
            "content": "<h2>Your Order is Complete</h2>"
        },
        {
            "name": "main",
            "content": "We appreciate your business. Your order information is below."
        }
    ]}
    

        body = '\r\n'.join([
                            'To: %s' % to,
                            # 'From: %s' % sender,
                            'X-MC-Template: %s' % "foodtrade-master|main",
                            # 'X-MC-Metadata: %s' % json.dumps(template_content),
                            'Subject: %s' % subject,
                            '', message
                            ])

        try:
            server.sendmail(sender, [to], body)
            server.quit()
            return True
        except:
            server.quit()
            return False


m = Email()
m.send_mail("sujitmhj@gmail.com","test","test")
