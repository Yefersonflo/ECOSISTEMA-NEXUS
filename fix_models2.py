import os

with open("trd/models.py", "r", encoding="utf-8") as f:
    content = f.read()

# remove from EncabezadoTRD
content = content.replace("""
    def to_json(self):
        import json
        return json.dumps({
            "id": self.id,
            "codigo": self.codigo,
            "nivel": self.nivel,
            "nombre": self.nombre,
            "soporte_papel": self.soporte_papel,
            "soporte_electronico": self.soporte_electronico,
            "extensiones": self.extensiones,
            "retencion_gestion": self.retencion_gestion,
            "retencion_central": self.retencion_central,
            "disposicion_final": self.disposicion_final,
            "reproduccion_tecnica": self.reproduccion_tecnica,
            "procedimiento": self.procedimiento,
            "orden": self.orden
        })
""", "")

# add to ItemTRD
content = content.replace("""    def __str__(self):
        return f"{self.codigo} - {self.nombre}""","""    def to_json(self):
        import json
        return json.dumps({
            "id": self.id,
            "codigo": self.codigo,
            "nivel": self.nivel,
            "nombre": self.nombre,
            "soporte_papel": self.soporte_papel,
            "soporte_electronico": self.soporte_electronico,
            "extensiones": self.extensiones,
            "retencion_gestion": self.retencion_gestion,
            "retencion_central": self.retencion_central,
            "disposicion_final": self.disposicion_final,
            "reproduccion_tecnica": self.reproduccion_tecnica,
            "procedimiento": self.procedimiento,
            "orden": self.orden
        })

    def __str__(self):
        return f"{self.codigo} - {self.nombre}""")

with open("trd/models.py", "w", encoding="utf-8") as f:
    f.write(content)
