import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Carpeta actual (donde se encuentra el programa .py)
carpeta = os.getcwd()

# Definir el rango de fechas de interés como objetos datetime
fecha_inicio = datetime(2011, 1, 1)
fecha_fin = datetime(2011, 12, 31)

# Inicializa un diccionario para contar las filas únicas por semana
filas_por_semana = {}

# Recorre todos los archivos CSV en la carpeta
for archivo in os.listdir(carpeta):
    if archivo.endswith('.csv'):
        # Extrae la fecha del nombre del archivo
        fecha_str = archivo.split('.')[0]
        fecha = datetime.strptime(fecha_str, '%Y%m%d').date()

        # Convierte la fecha a un objeto datetime completo
        fecha = datetime(fecha.year, fecha.month, fecha.day)

        # Verifica si la fecha está dentro del rango de interés
        if fecha_inicio <= fecha <= fecha_fin:
            # Carga el archivo CSV en un DataFrame de pandas
            df = pd.read_csv(os.path.join(carpeta, archivo))

            # Cuenta las filas únicas basadas en la columna "Number"
            filas_unicas = df['Number'].nunique()

            # Agrupa las filas únicas por semana
            semana = fecha.strftime('%Y-%U')
            filas_por_semana[semana] = filas_por_semana.get(semana, 0) + filas_unicas

# Convierte el diccionario en un DataFrame para crear el histograma
df_histograma = pd.DataFrame(list(filas_por_semana.items()), columns=['Semana', 'Filas_unicas'])

# Ordena las filas en función de la columna "Semana"
df_histograma.sort_values(by='Semana', inplace=True)

# Crea un DataFrame con todas las semanas dentro del rango de fechas
semanas_en_rango = []
fecha_actual = fecha_inicio
while fecha_actual <= fecha_fin:
    semana = fecha_actual.strftime('%Y-%U')
    semanas_en_rango.append(semana)
    fecha_actual += timedelta(weeks=1)

# Crea un DataFrame con todas las semanas y fusiona con el histograma
df_todas_semanas = pd.DataFrame({'Semana': semanas_en_rango})
df_histograma = df_todas_semanas.merge(df_histograma, on='Semana', how='left')

# Rellena los valores NaN con 0 (semanas sin datos)
df_histograma['Filas_unicas'].fillna(0, inplace=True)

# Crea un histograma de las filas únicas por semana
plt.bar(df_histograma['Semana'], df_histograma['Filas_unicas'])
plt.xlabel('Week')
plt.ylabel('New AR')
plt.xticks(rotation=45)
plt.title('New AR at East Limb by week')
plt.tight_layout()
plt.savefig('newARatEastLimb_histogram.png')
plt.show()
print(df_histograma)
df_histograma.to_csv('histogramtable.csv', index=False)