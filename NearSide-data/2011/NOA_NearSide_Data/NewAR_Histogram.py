import os
import re
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pandas as pd

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
        datos = set(int(linea.split()[0]) for linea in archivo if is_numero(linea.strip().split()[0]))
    return datos

def obtener_semana(fecha):
    fecha_obj = datetime.strptime(fecha, '%Y-%m-%d')
    semana = fecha_obj - timedelta(days=fecha_obj.weekday())
    return semana.strftime('%Y-%m-%d')

def generar_histograma(datos_por_semana):
    semanas = list(datos_por_semana.keys())
    cantidades = list(datos_por_semana.values())

    plt.figure(figsize=(10, 6))
    plt.bar(semanas, cantidades, color='skyblue')
    plt.xlabel('Week')
    plt.ylabel('Number of new AR')
    plt.title('Histogram')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Guardar el gráfico como imagen
    plt.savefig('histogram.png')
    
    plt.show()

def encontrar_datos_nuevos():
    archivos_txt = [archivo for archivo in os.listdir() if archivo.endswith('.txt')]
    archivos_txt.sort()

    datos_archivos = []
    for archivo in archivos_txt:
        fecha = obtener_fecha_desde_nombre(archivo)
        datos_archivo = leer_datos_archivo(archivo)
        datos_archivos.append((fecha, datos_archivo))

    datos_primer_vez = set()
    datos_por_semana = {}
    for fecha, datos_archivo in datos_archivos:
        datos_nuevos = datos_archivo - datos_primer_vez
        datos_primer_vez.update(datos_archivo)

        semana = obtener_semana(fecha)
        if semana in datos_por_semana:
            datos_por_semana[semana] += len(datos_nuevos)
        else:
            datos_por_semana[semana] = len(datos_nuevos)

    generar_histograma(datos_por_semana)

    df = pd.DataFrame(list(datos_por_semana.items()), columns=['Week', 'New ARs'])
    df.to_csv('histogram.csv', index=False)
    print(df)

encontrar_datos_nuevos()


