import pandas as pd

#cargar dataset
df = pd.read_csv('Dataset/4. Estudiantes.csv')

print(df.head)

#nombre de columnas
print(df.columns)

#cuantos estudiantes hay por pais
conteo = df.groupby("Country").size()

print(conteo)

#paises con mas de 15 estudiantes
resumen_paises = conteo[conteo >= 30].index

print(resumen_paises)

#filtramos el dataset para que solo sean de esos paises
df_2 = df[df["Country"].isin(resumen_paises)]

print(df_2)

#eliminar columnas que no necesitamos
df_filtrado = df_2.drop(["Student_ID", "Age", "Relationship_Status", "Gender", "Conflicts_Over_Social_Media"], axis=1)

print(df_filtrado)

#los paises que quedaron
paises_finales = df_filtrado["Country"].unique()

print(paises_finales)

print(df_filtrado.columns)

#renombrar columnas
df_filtrado.columns = [
    'Nivel_Academico',
    'Pais',
    'Promedio_Horas_Uso_Diario',
    'Plataforma_Mas_Usada',
    'Afecta_Rendimiento_Academico',
    'Horas_Sueño_Por_Noche',
    'Puntaje_Salud_Mental',
    'Puntaje_Adiccion'
]

print(df_filtrado.columns)

print(df_filtrado.head)

print(paises_finales)

df_filtrado.to_csv("Estudiantes_final.csv", index=False)