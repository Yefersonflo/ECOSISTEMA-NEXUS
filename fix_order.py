import os

path = "trd/templates/trd/editar_trd.html"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# find {% extends %} and {% load %}
extends_idx = -1
load_idx = -1
for i, line in enumerate(lines):
    if "{% extends" in line:
        extends_idx = i
    if "{% load trd_extras %}" in line:
        load_idx = i

if load_idx < extends_idx:
    # swap them
    temp = lines[extends_idx]
    lines[extends_idx] = lines[load_idx]
    lines[load_idx] = temp

with open(path, "w", encoding="utf-8") as f:
    f.writelines(lines)
