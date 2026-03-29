import streamlit as st
import plotly.express as px
import pandas as pd

#Titulo
st.title("Analisis de adiccion a las redes sociales y el bienestar estudiantil")

#carga de datos
df = pd.read_csv("Estudiantes_final.csv", sep=";", encoding="latin1")

#objetivo especifico 1
st.header("Impacto en el rendimiento y salud mental")

tab1, tab2 = st.tabs(["Rendimiento Academico", "Salud Mental y Sueño"])

with tab1:
    st.subheader("Impacto en el Rendimiento")
    # Usamos Box plot porque 'Afecta_Rendimiento_Academico' es texto (categoría)
    fig_rendimiento = px.box(df,
        x="Afecta_Rendimiento_Academico", 
        y="Puntaje_Adiccion",
        color="Afecta_Rendimiento_Academico",
        title="Distribución de Adicción según Impacto Académico")
    st.plotly_chart(fig_rendimiento)

with tab2:
    st.subheader("Relación Lineal: Adicción vs Sueño")
    #grafico de relacion lineal
    fig_sleep = px.scatter(df, 
        x="Puntaje_Adiccion", 
        y="Horas_de_Sueño_Por_Noche",
    trendline="ols", # Esto dibuja la línea de regresión
    trendline_color_override="red",
    title="¿A mayor adicción, menos horas de sueño?",
    labels={"Puntaje_Adiccion": "Nivel de Adicción", 
    "Horas_de_Sueño_Por_Noche": "Horas de Sueño"})
    
    st.plotly_chart(fig_sleep)



