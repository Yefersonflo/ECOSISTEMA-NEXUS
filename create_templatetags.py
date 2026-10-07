import os

os.makedirs("trd/templatetags", exist_ok=True)
with open("trd/templatetags/__init__.py", "w") as f:
    pass

with open("trd/templatetags/trd_extras.py", "w", encoding="utf-8") as f:
    f.write("""from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    if dictionary is None:
        return None
    return dictionary.get(key)
""")
