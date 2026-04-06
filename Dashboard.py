import streamlit as st
import plotly.express as px
import pandas as pd

#Titulo
st.title("Analisis de adiccion a las redes sociales y el bienestar estudiantil")

#carga de datos
df_final = pd.read_csv("Estudiantes_final.csv", encoding="latin1")

df = df_final.rename(columns={col: "Horas_Sueno" for col in df_final.columns if "Sue" in col})

df.columns = df.columns.str.strip()

#empieza la fiesta
tab1, tab2, tab3, tab4 = st.tabs(["Rendimiento Academico", "Adiccion, Salud Mental y Sueño", "Plataformas Mas Usada", "lo otro"])

with tab1:
    st.subheader("Impacto en el Rendimiento")
    
    #gráfico (Box Plot)
    fig_rendimiento = px.box(df,
        x="Afecta_Rendimiento_Academico", 
        y="Puntaje_Adiccion",
        color="Afecta_Rendimiento_Academico",
        title="Distribución de Adicción según Impacto Académico")
    st.plotly_chart(fig_rendimiento)

    #analisis
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

    st.divider()

    st.header("Nivel educativo con mas horas de uso")

    #Agrupar y calcular el promedio
    df_nivel_educativo = df.groupby('Nivel_Academico')['Promedio_Horas_Uso_Diario'].mean().reset_index()
    df_nivel_educativo = df_nivel_educativo.sort_values(by='Promedio_Horas_Uso_Diario', ascending=False)

    st.header("Uso de Redes Sociales por Nivel Educativo")

    #grafico de barra
    fig2 = px.bar(
        df_nivel_educativo,
        x='Nivel_Academico',
        y='Promedio_Horas_Uso_Diario',
        title='Promedio de Horas Diarias por Nivel Académico',
    labels={
        'Nivel_Academico': 'Nivel Academico', 
        'Promedio_Horas_Uso_Diaria': 'Promedio de Horas Diario'
    },
    color='Promedio_Horas_Uso_Diario',
    color_continuous_scale='Viridis'
)

    st.plotly_chart(fig2, use_container_width=True)

    #conclusion
    nivel_max = df_nivel_educativo.iloc[0]['Nivel_Academico']
    horas_max = df_nivel_educativo.iloc[0]['Promedio_Horas_Uso_Diario']

    st.subheader("Conclusión:")
    st.info(f"El nivel educativo que más tiempo pasa en redes sociales es **{nivel_max}**, con un promedio de **{horas_max:.2f} horas** diarias.")


with tab2:
    st.subheader("Adicción vs Sueño")
    #grafico de relacion lineal
    fig_sleep = px.scatter(df, 
        x="Puntaje_Adiccion", 
        y="Horas_Sueno",
        trendline="ols", 
    trendline_color_override="red",
        title="¿A mayor adicción, menos horas de sueño?",
        labels={"Puntaje_Adiccion": "nivel de adiccion", 
    "Horas_Sueno": "Horas de Sueño"})
    
    st.plotly_chart(fig_sleep)

    #analisis
    st.markdown("""
### 📝 Interpretación de la Tendencia
La línea roja de regresión confirma una **reducción lineal de las horas de sueño** conforme aumenta el puntaje de adicción. 
Los estudiantes en niveles críticos de dependencia (8-9) reportan hasta **4 horas menos** de descanso nocturno en comparación con aquellos con niveles bajos.
""")
    
    st.divider() 

    st.header("Distribución de Salud Mental según Nivel de Adicción")

    #Grafico de salud mental (box plot)
    fig_mental = px.box(df, 
                        x="Puntaje_Adiccion", 
                        y="Puntaje_Salud_Mental",
                        color="Puntaje_Adiccion",
                        )
    st.plotly_chart(fig_mental)

    #analisis
    st.markdown("""
### 🧠 Interpretación de Salud Mental
Se observa que el incremento de la dependencia digital se asocia 
con una mayor inestabilidad emocional. Los estudiantes con puntajes de adicción más altos suelen 
reportar los niveles más bajos de bienestar mental.
""")

    st.divider()

    st.header("Existe relacion entre el uso diario y la adiccion?")

    #gráfico de dispersión
    fig = px.scatter(
        df, 
        x='Promedio_Horas_Uso_Diario', 
        y='Puntaje_Adiccion',
        trendline="ols", 
        trendline_color_override="red",
        labels={
        'Avg_Daily_Usage_Hours': 'Horas de Uso Diario',
        'Addicted_Score': 'Puntaje de Adicción'
    },
        title="Horas de Uso vs. Adicción",
        template="plotly_white"
)

#analisis
    st.plotly_chart(fig, use_container_width=True)

    correlacion = df['Promedio_Horas_Uso_Diario'].corr(df['Puntaje_Adiccion'])

    st.subheader("Conclusión:")

    st.write(f"Coeficiente de correlación: **{correlacion:.2f}**")

    if correlacion >= 0.6:
        st.success("Existe una **fuerte relación positiva**. El tiempo de uso es un factor determinante en el puntaje de adicción.")
    elif 0.3 <= correlacion < 0.6:
        st.info("Existe una **relación moderada**. Se observa una tendencia clara al aumento de la adicción con el uso prolongado.")
    else:
        st.warning("La relación es **débil**. Aunque hay una tendencia, otros factores podrían estar influyendo en la adicción.")

with tab3:
    st.subheader("Análisis de las Plataformas más Utilizadas")

    #cuantas veces sale
    conteo_plataformas = df['Plataforma_Mas_Usada'].value_counts().reset_index()
    conteo_plataformas.columns = ['Plataforma', 'Cantidad']

    #grafico de barras
    fig_plataformas = px.bar(
        conteo_plataformas, 
        x='Plataforma', 
        y='Cantidad',
        title="Ranking de Popularidad por Red Social",
        labels={'Cantidad': 'Número de Estudiantes', 'Plataforma': 'Red Social'},
        color='Plataforma',
        text_auto=True 
    )
    
    st.plotly_chart(fig_plataformas)

    #analisis
    st.markdown(f"""
    **Análisis rápido:** En este gráfico se observa la distribución de los **{len(df)}** estudiantes según su plataforma principal. 
    Esto nos permite identificar qué redes sociales tienen mayor impacto en su rutina diaria.
    """)

