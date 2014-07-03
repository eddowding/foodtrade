from django import template
from mainapp.classes.Email import Email
register = template.Library()

@register.filter
def error(value, args):
    email = Email()
    to = ['hello@foodtrade.com', 'sujit@phunka.com']
    subject = args + ' Error in Foodtrade'
    msg = 'Foodtrade just encountered a ' + args + ' ' + 'error at ' + value +'. Please fix this as soon as you can.'
    # print to, subject, msg
    for each_receipent in to:
	    email.send_mail(each_receipent, subject , msg)
    return ''