import os
import re

def is_numero(cadena):
    try:
        int(cadena)
        return True
    except ValueError:
        return False

def obtener_fecha_desde_nombre(nombre_archivo):
    # Buscar el patrón de fecha en el nombre del archivo
    patron_fecha = re.search(r'(\d{4})(\d{2})(\d{2})', nombre_archivo)
    if patron_fecha:
        anio, mes, dia = patron_fecha.groups()
        return f"{anio}-{mes}-{dia}"
    else:
        return "Fecha no encontrada"

def leer_datos_archivo(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo:
        datos = set(int(linea.split()[0]) for linea in archivo if is_numero(linea.strip().split()[0]))
    return datos

def encontrar_datos_nuevos():
    archivos_txt = [archivo for archivo in os.listdir() if archivo.endswith('.txt')]
    archivos_txt.sort()  # Ordena los nombres de archivos alfabéticamente

    datos_archivos = []
    for archivo in archivos_txt:
        #print(f"Leyendo archivo: {archivo}")
        fecha = obtener_fecha_desde_nombre(archivo)
        datos_archivo = leer_datos_archivo(archivo)
        datos_archivos.append((fecha, datos_archivo))

    datos_primer_vez = set()
    for fecha, datos_archivo in datos_archivos:
        datos_nuevos = datos_archivo - datos_primer_vez
        datos_primer_vez.update(datos_archivo)

        if datos_nuevos:
            print(f"{fecha}")
            print(", ".join(str(dato) for dato in datos_nuevos))
            print()
        else:
            print(f"{fecha}")
            print()

encontrar_datos_nuevos()


