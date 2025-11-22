from django import template
from django.utils.safestring import mark_safe
import markdown

register = template.Library()

@register.filter(name='convert_markdown')
def convert_markdown(text):
    
    #converte o texto cru para HTML
    html = markdown.markdown(text)
    
    #O mark_safe diz ao Django 'confie neste HTML, não escape as tags'
    return mark_safe(html)