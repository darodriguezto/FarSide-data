'''
    Este programa busca las AR nuevas por fecha y muestra la información que NOAA proporciona
'''
import os
import re

def is_numero(cadena):
    try:
        int(cadena)
        return True
    except ValueError:
        return False

def obtener_fecha_desde_nombre(nombre_archivo):
    patron_fecha = re.search(r'(\d{4})(\d{2})(\d{2})', nombre_archivo)
    if patron_fecha:
        anio, mes, dia = patron_fecha.groups()
        return f"{anio}-{mes}-{dia}"
    else:
        return "Fecha no encontrada"

def leer_datos_archivo(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo:
        lineas = archivo.readlines()
        datos = set(linea.strip().split()[0] for linea in lineas if is_numero(linea.strip().split()[0]))
    return datos, lineas

def obtener_semana(fecha):
    fecha_obj = datetime.strptime(fecha, '%Y-%m-%d')
    semana = fecha_obj - timedelta(days=fecha_obj.weekday())
    return semana.strftime('%Y-%m-%d')

def encontrar_datos_nuevos():
    archivos_txt = [archivo for archivo in os.listdir() if archivo.endswith('.txt')]
    archivos_txt.sort()  # Ordena los nombres de archivos alfabéticamente

    datos_archivos = []
    for archivo in archivos_txt:
        fecha = obtener_fecha_desde_nombre(archivo)
        datos_archivo, lineas_archivo = leer_datos_archivo(archivo)
        datos_archivos.append((fecha, datos_archivo, lineas_archivo))

    datos_primer_vez = set()
    for fecha, datos_archivo, lineas_archivo in datos_archivos:
        datos_nuevos = datos_archivo - datos_primer_vez
        datos_primer_vez.update(datos_archivo)

        if datos_nuevos:
            print(f"Fecha: {fecha}")
            for linea in lineas_archivo:
                if linea.strip().split()[0] in datos_nuevos:
                    print(linea.strip())
            print()

encontrar_datos_nuevos()



