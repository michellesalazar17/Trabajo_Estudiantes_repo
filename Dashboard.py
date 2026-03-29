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
    
    # El código de tu gráfico (Box Plot)
    fig_rendimiento = px.box(df,
        x="Afecta_Rendimiento_Academico", 
        y="Puntaje_Adiccion",
        color="Afecta_Rendimiento_Academico",
        title="Distribución de Adicción según Impacto Académico")
    st.plotly_chart(fig_rendimiento)

    #Analisis estadistico
    st.divider()
    st.markdown("### 📊 Análisis de Resultados")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Diferencia de Medianas:**")
        st.write("""
        * **Grupo 'No'**: Los estudiantes muestran una mediana de adicción de **6 puntos**.
        * **Grupo 'Yes'**: La mediana sube a **8 puntos**, indicando una relación directa entre adicción y afectación académica.
        """)

    with col2:
        st.write("**Dispersión y Riesgo:**")
        st.write("""
        * El rango intercuartil del grupo afectado se concentra entre **6.5 y 9 puntos**.
        * Esto confirma que puntajes superiores a 7 representan un **umbral crítico** para el rendimiento.
        """)

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

    st.markdown("""
### 📝 Interpretación de la Tendencia
La línea roja de regresión confirma una **reducción lineal de las horas de sueño** conforme aumenta el puntaje de adicción. 
Los estudiantes en niveles críticos de dependencia (8-9) reportan hasta **4 horas menos** de descanso nocturno en comparación con aquellos con niveles bajos.
""")
    
    st.divider() # Línea divisoria visual

    # 2. GRÁFICO DE SALUD MENTAL (Box Plot)
    fig_mental = px.box(df, 
                        x="Puntaje_Adiccion", 
                        y="Puntaje_Salud_Mental",
                        color="Puntaje_Adiccion",
                        title="Distribución de Salud Mental según Nivel de Adicción")
    st.plotly_chart(fig_mental)

    st.markdown("""
    ## 🧠 Interpretación de Salud Mental
    Se observa que el incremento de la dependencia digital se asocia 
    con una mayor inestabilidad emocional. Los estudiantes con puntajes de adicción más altos suelen 
    reportar los niveles más bajos de bienestar mental.
    """)
    






