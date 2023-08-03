import os

def leer_datos_archivo(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo:
        datos = set(int(linea.strip()) for linea in archivo)
    return datos

def encontrar_datos_nuevos():
    archivos_txt = [archivo for archivo in os.listdir() if archivo.endswith('.txt')]

    datos_totales = set()
    for archivo in archivos_txt:
        datos_archivo = leer_datos_archivo(archivo)
        datos_nuevos = datos_archivo - datos_totales
        datos_totales.update(datos_archivo)

        if datos_nuevos:
            print(f"Archivo: {archivo}")
            print("Datos nuevos:", ", ".join(str(dato) for dato in datos_nuevos)
            print()

encontrar_datos_nuevos()
