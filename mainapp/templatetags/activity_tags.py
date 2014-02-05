from django import template

register = template.Library()

@register.inclusion_tag('single_activity_template.html')
def single_activity(userinfo, result, result_type, position):
    return {'userinfo':userinfo, 'result': result, 'result_type':result_type, 'position':position}