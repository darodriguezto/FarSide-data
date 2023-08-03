import os

def is_numero(cadena):
    try:
        int(cadena)
        return True
    except ValueError:
        return False

def leer_datos_archivo(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo:
        datos = set(int(linea.split()[0]) for linea in archivo if is_numero(linea.strip().split()[0]))
    return datos

def encontrar_datos_nuevos():
    archivos_txt = [archivo for archivo in os.listdir() if archivo.endswith('.txt')]
    archivos_txt.sort()  # Ordena los nombres de archivos alfabéticamente

    datos_archivos = []
    for archivo in archivos_txt:
        print(f"Leyendo archivo: {archivo}")
        datos_archivo = leer_datos_archivo(archivo)
        datos_archivos.append(datos_archivo)

    datos_primer_vez = set()
    for datos_archivo in datos_archivos:
        datos_nuevos = datos_archivo - datos_primer_vez
        datos_primer_vez.update(datos_archivo)

        if datos_nuevos:
            print(f"{archivos_txt[datos_archivos.index(datos_archivo)]}")
            print(", ".join(str(dato) for dato in datos_nuevos))
            print()
        else:
            print(f"{archivos_txt[datos_archivos.index(datos_archivo)]}")
            print()

encontrar_datos_nuevos()


