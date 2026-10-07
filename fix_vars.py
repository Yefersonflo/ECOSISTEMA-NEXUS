import os

path = "trd/templates/trd/editar_trd.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

consts = {
    "INPUT": "w-full px-4 py-3 bg-white border-2 border-slate-300 rounded-xl text-sm font-bold text-slate-800 placeholder-slate-400 placeholder:font-normal hover:border-slate-400 focus:border-comfaBlue focus:ring-4 focus:ring-blue-100 outline-none transition-all",
    "INPUT_COD": "w-full px-4 py-3 bg-white border-2 border-slate-300 rounded-xl text-sm font-black text-comfaBlue placeholder-slate-400 placeholder:font-normal hover:border-slate-400 focus:border-comfaBlue focus:ring-4 focus:ring-blue-100 outline-none transition-all",
    "INPUT_NUM": "w-full px-4 py-3 bg-white border-2 border-slate-300 rounded-xl text-lg font-black text-slate-800 text-center hover:border-slate-400 focus:border-comfaBlue focus:ring-4 focus:ring-blue-100 outline-none transition-all",
    "AREA": "w-full px-4 py-3 bg-white border-2 border-slate-300 rounded-xl text-sm font-medium text-slate-800 placeholder-slate-400 placeholder:font-normal hover:border-slate-400 focus:border-comfaBlue focus:ring-4 focus:ring-blue-100 outline-none transition-all",
    "LABEL": "text-xs font-black text-slate-700 uppercase tracking-wider mb-2 flex items-center gap-1.5",
    "LEGEND": "px-3 mx-2 bg-white border-2 rounded-lg text-[10px] font-black uppercase tracking-widest"
}

import re
# Remove the {% set ... %} lines
content = re.sub(r"\{%\s*set\s+.*?\s*%\}", "", content)

# Replace {{ INPUT }} with actual class strings
for key, val in consts.items():
    content = content.replace("{{ " + key + " }}", val)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Replaced variables in editar_trd.html")
