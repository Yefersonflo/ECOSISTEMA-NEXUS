with open('trd/templates/trd/diligenciar.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace trailing {% endblock %}\n\n{% endblock %} with a single {% endblock %}
content = content.replace('{% endblock %}\n\n{% endblock %}', '{% endblock %}')
content = content.replace('{% endblock %}\n{% endblock %}', '{% endblock %}')

with open('trd/templates/trd/diligenciar.html', 'w', encoding='utf-8') as f:
    f.write(content)
