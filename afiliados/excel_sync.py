import os
import re
import json
import pandas as pd

COLUMNS = [
    "Fecha",
    "Tipo Identificación",
    "Cédula",
    "Nombre",
    "Módulo",
    "Estante",
    "Bandeja",
    "Cubículo",
    "Número de Carpeta",
    "Estado",
    "Fecha Retiro"
]

def load_shared_folder_path():
    try:
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        config_path = os.path.join(desktop_path, "ECOSISTEMA NEXUS", "1. Gestor de Escritorio", "config.json")
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
                path = config.get("shared_folder_path", "")
                if path and os.path.isdir(path):
                    return path
    except Exception:
        pass
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    return os.path.join(desktop, "ECOSISTEMA NEXUS", "5. Base de Datos", "base_datos_prueba")

def sanitize_cedula(cedula):
    return re.sub(r"\D", "", str(cedula))

def get_excel_filename(cedula):
    cleaned = sanitize_cedula(cedula)
    if len(cleaned) < 2:
        cleaned = cleaned.zfill(2)
    suffix = cleaned[-2:]
    return f"{suffix}.xlsx"

def read_excel_file(folder_path, filename):
    filepath = os.path.join(folder_path, filename)
    if os.path.exists(filepath):
        try:
            df = pd.read_excel(filepath, dtype=str).fillna("")
            for col in COLUMNS:
                if col not in df.columns:
                    df[col] = ""
            return df[COLUMNS]
        except Exception:
            pass
    return pd.DataFrame(columns=COLUMNS)

def save_excel_file(folder_path, filename, df):
    filepath = os.path.join(folder_path, filename)
    df.to_excel(filepath, index=False)

def sync_to_excel(action, record_data, original_cedula=None):
    """
    Sincroniza los cambios realizados en la base de datos SQL desde la plataforma web
    hacia los archivos Excel particionados correspondientes.
    """
    folder_path = load_shared_folder_path()
    if not os.path.isdir(folder_path):
        print(f"[ERROR] Ruta de base de datos Excel no válida: {folder_path}")
        return
        
    try:
        if action == "SAVE":
            new_ced = sanitize_cedula(record_data.get("Cédula", ""))
            if not new_ced:
                return
                
            new_filename = get_excel_filename(new_ced)
            
            # Estandarizar la fila
            row = {col: str(record_data.get(col, "")).strip() for col in COLUMNS}
            row["Cédula"] = new_ced
            
            # Caso A: Modificación con cambio de cédula
            if original_cedula:
                orig_ced = sanitize_cedula(original_cedula)
                orig_filename = get_excel_filename(orig_ced)
                
                if orig_filename != new_filename:
                    # El registro cambió de partición. Eliminar de original y meter en destino
                    df_orig = read_excel_file(folder_path, orig_filename)
                    df_orig = df_orig[df_orig["Cédula"] != orig_ced]
                    save_excel_file(folder_path, orig_filename, df_orig)
                    
                    df_new = read_excel_file(folder_path, new_filename)
                    df_new = df_new[df_new["Cédula"] != new_ced]
                    df_new = pd.concat([df_new, pd.DataFrame([row])], ignore_index=True)
                    save_excel_file(folder_path, new_filename, df_new)
                    return
                else:
                    # Misma partición
                    df = read_excel_file(folder_path, new_filename)
                    df = df[df["Cédula"] != orig_ced]
                    df = df[df["Cédula"] != new_ced]
                    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
                    save_excel_file(folder_path, new_filename, df)
                    return
            
            # Caso B: Creación pura o actualización simple
            df = read_excel_file(folder_path, new_filename)
            df = df[df["Cédula"] != new_ced]
            df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
            save_excel_file(folder_path, new_filename, df)
            
        elif action == "DELETE":
            ced = sanitize_cedula(record_data.get("Cédula", ""))
            if not ced:
                return
            filename = get_excel_filename(ced)
            df = read_excel_file(folder_path, filename)
            df = df[df["Cédula"] != ced]
            save_excel_file(folder_path, filename, df)
            
    except Exception as e:
        print(f"Error sincronizando a Excel desde la web: {e}")
