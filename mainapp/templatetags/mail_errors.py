from django import template
from mainapp.classes.Email import Email
register = template.Library()

@register.filter
def error(value, args):
    email = Email()
    to = 'santosh.ghimire33@gmail.com'
    subject = args + ' Error in Foodtrade'
    msg = 'Foodtrade just encountered a ' + args + ' ' + 'error at ' + value +'. Please fix this as soon as you can.'
    print to, subject, msg
    email.send_mail(to, subject , msg)
    return ''