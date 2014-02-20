import mandrill 

class Email():
    def __init__ (self):
        pass

    def send_mail(self, subject, template_content=[{}], to = [{}]):
        # sender = 'ed@foodtrade.com'
        # passwd = 'NwotnhPk1Nprc6OX0Wq6vA'
        #md = mandrill.Mandrill('DS3yEW4HdOzqHGXOiXGPkg')
        md = mandrill.Mandrill('NwotnhPk1Nprc6OX0Wq6vA')
        mes = mandrill.Messages(md)

        message ={
            'auto_html': False,
            'auto_text': False,
            'to':to,
            'from_email':'no-reply@foodtrade.com', 
            'from_name':'FoodTrade', 
            'important':'true',
            'track_click':'true',
            'subject':subject,
        }

        template_content = template_content
        mes.send_template('foodtrade-master', template_content, message)

