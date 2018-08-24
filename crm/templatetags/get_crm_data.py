from django.template import Library
from django.utils.safestring import mark_safe
import datetime

register = Library()

@register.simple_tag
def get_approved_url(enrollment_obj):
    return "/crm/stu_enrollment/approved/%s"%enrollment_obj.id
