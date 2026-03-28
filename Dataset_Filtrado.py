import pandas as pd

#cargar dataset
df = pd.read_csv('Dataset/4. Estudiantes.csv')

print(df.head)

#nombre de columnas
print(df.columns)

#filtrar nivel academico
df_2 = df[df["Academic_Level"] == "Graduate"]

print(df_2)

#seleccionar los paises que vamos a usar
paises = ["India", "USA", "UK", "Australia", "Bangladesh"]

df_3 = df_2[df_2["Country"].isin(paises)]

print(df_3)

#eliminar columnas que no necesitamos
df_filtrado = df_3.drop(["Student_ID", "Age", "Relationship_Status", "Gender"], axis=1)

print(df_filtrado)



