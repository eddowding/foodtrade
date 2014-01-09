

import smtplib


class Email():
    def __init__ (self):
        pass

    def send_mail(self, to, subject, message):
    

        # mandrill Sign In
        sender = 'ed@foodtrade.com'
        passwd = 'NwotnhPk1Nprc6OX0Wq6vA'

        server = smtplib.SMTP('smtp.mandrillapp.com', 587)
        server.ehlo()
        server.starttls()
        server.login(sender, passwd)

        body = '\r\n'.join(['To: %s' % to,
                            'From: %s' % sender,
                            'Subject: %s' % subject,
                            '', message])

        try:
            server.sendmail(sender, [to], body)
            server.quit()
            return True
        except:
            server.quit()
            return False

            