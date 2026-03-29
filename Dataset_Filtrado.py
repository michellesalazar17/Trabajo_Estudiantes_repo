import pandas as pd

#cargar dataset
df = pd.read_csv('Dataset/4. Estudiantes.csv')

print(df.head)

#nombre de columnas
print(df.columns)

#filtrar nivel academico
df_2 = df[df["Academic_Level"] == "Graduate"]

#cuantos estudiantes hay por pais
conteo = df_2.groupby("Country").size()

print(conteo)

#paises con mas de 15 estudiantes
resumen_paises = conteo[conteo > 15].index

print(resumen_paises)

#filtramos el dataset para que solo sean de esos paises
df_3 = df_2[df_2["Country"].isin(resumen_paises)]

print(df_3)

#eliminar columnas que no necesitamos
df_filtrado = df_3.drop(["Student_ID", "Age", "Relationship_Status", "Gender"], axis=1)

print(df_filtrado)

#los paises que quedaron
paises_finales = df_filtrado["Country"].unique()

print(paises_finales)





