import os

path = "trd/templatetags/trd_extras.py"
with open(path, "w", encoding="utf-8") as f:
    f.write("""from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    if not isinstance(dictionary, dict):
        return None
    return dictionary.get(key)
""")
