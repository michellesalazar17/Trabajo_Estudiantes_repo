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

    #Agrupar y calcular el promedio
    df_nivel_educativo = df.groupby('Nivel_Academico')['Promedio_Horas_Uso_Diario'].mean().reset_index()
    df_nivel_educativo = df_nivel_educativo.sort_values(by='Promedio_Horas_Uso_Diario', ascending=False)

    #grafico de barra
    fig2 = px.bar(
        df_nivel_educativo,
        x='Nivel_Academico',
        y='Promedio_Horas_Uso_Diario',
        title='Promedio de Horas Diarias por Nivel Académico',
    labels={
        'Nivel_Academico': 'Nivel Academico', 
        'Promedio_Horas_Uso_Diaria': 'promedio horas diaria'
    },
        color="Nivel_Academico",
        color_discrete_sequence=["#ADD8E6", "#00008B"]    
)

    st.plotly_chart(fig2, use_container_width=True)

    fig2.update_layout(coloraxis_showscale=False)

    #conclusion
    nivel_max = df_nivel_educativo.iloc[0]['Nivel_Academico']
    horas_max = df_nivel_educativo.iloc[0]['Promedio_Horas_Uso_Diario']

    st.subheader("Conclusión:")
    st.write(f"El nivel educativo que más tiempo pasa en redes sociales es **{nivel_max}**, con un promedio de **{horas_max:.2f} horas** diarias.")

with tab2:
    st.subheader("Adicción vs Sueño")
    
    # creacion del histograma
    fig_hist = px.histogram(
    df, 
    x="Horas_Sueno", 
    color="Puntaje_Adiccion",
    title="Distribución de Horas de Sueño por Nivel de Adicción",
    labels={"Horas_Sueno": "Horas de Sueño", "count": "Número de Estudiantes"},
    opacity=0.7,
    barmode="group" 
)
    #ajuste del diseno
    fig_hist.update_layout(
    bargap=0.1, 
    xaxis_title="Horas de Sueño",
    yaxis_title="Cantidad de Estudiantes"
)
    
    #paar que aparezca en la app
    st.plotly_chart(fig_hist, use_container_width=True)

    #analisis
    st.markdown("### 📝 Análisis del Histograma")

    st.write("""
Al observar la distribución de frecuencias, se identifican tres hallazgos clave:

1. **Desplazamiento de Masa:** Los niveles de adicción más altos (colores azules/celestes) muestran una clara **asimetría hacia la izquierda**, concentrando a la mayoría de los estudiantes en el rango de **4 a 6 horas** de sueño.
2. **Brecha de Descanso:** Existe una diferencia marcada entre los picos de frecuencia. Mientras que los niveles de adicción moderada alcanzan su máximo cerca de las **7-8 horas**, los niveles críticos rara vez superan las 6 horas.
3. **Zona de Riesgo:** El tramo de **menos de 5 horas** de sueño está poblado casi exclusivamente por estudiantes con puntajes de adicción elevados, lo que sugiere que la dependencia digital es un factor determinante en la privación del sueño.
""")
    
    st.divider() 

    st.header("Distribución de Salud Mental según Nivel de Adicción")

    st.subheader("Relación: Salud Mental vs Adicción")

    #agrupo los datos par ver la frecuencia
    # cuantas personas hay en cada cruce del puntaje
    df_burbujas = df.groupby(['Puntaje_Adiccion', 'Puntaje_Salud_Mental']).size().reset_index(name='Cantidad_Estudiantes')

    #creacion grafico de burbujas
    fig_burbujas = px.scatter(
        df_burbujas,
        x="Puntaje_Adiccion",
        y="Puntaje_Salud_Mental",
        size="Cantidad_Estudiantes", #depende de la cantidad de estudiantes
        color="Puntaje_Salud_Mental", 
        hover_name="Cantidad_Estudiantes", 
        title="Gráfico de Burbujas: Frecuencia de Salud Mental por Adicción",
        labels={
            "Puntaje_Adiccion": "Nivel de Adicción",
            "Puntaje_Salud_Mental": "Nivel de Salud Mental",
            "Cantidad_Estudiantes": "Nro. de Estudiantes"
        },
        size_max=40#tamano
    )

    #para que no solo se vean los numeros enteros
    fig_burbujas.update_layout(
        xaxis=dict(tickmode='linear', tick0=1, dtick=1),
        yaxis=dict(tickmode='linear', tick0=1, dtick=1)
    )

    #paar que aparezca en el dashboard
    st.plotly_chart(fig_burbujas, use_container_width=True)

    #analisis
    st.markdown("### 📝 Análisis de Salud Mental y Adicción")

    st.write("""
El gráfico de burbujas revela una tendencia estructural en los datos:

1. **Correlación Inversa:** Existe una trayectoria descendente clara. A medida que el **Nivel de Adicción** se desplaza hacia la derecha (valores 8 y 9), el **Nivel de Salud Mental** cae hacia los valores más bajos (4 y 5).
2. **Concentración de la Muestra:** Las burbujas de mayor tamaño se sitúan en los niveles de adicción 6 y 7 con una salud mental intermedia. Esto indica que el grueso de la población estudiantil ya presenta signos de afectación moderada.
3. **Puntos Críticos:** Es alarmante observar que en el nivel de **Adicción 9**, la mayor concentración de estudiantes se encuentra en los niveles de **Salud Mental 4 y 5**, desapareciendo casi por completo las burbujas en los niveles de salud óptimos (7 u 8).
""")
    
    st.divider()

    st.subheader("Análisis de Uso Diario por Nivel de Adicción")

    #boxplot de notched
    fig_uso = px.box(
        df, 
        x="Puntaje_Adiccion", 
        y="Promedio_Horas_Uso_Diario", # Nombre actualizado
        notched=True, # El toque estadístico para comparar medianas
        title="Distribución de Horas de Uso según Nivel de Adicción",
        color="Puntaje_Adiccion",
        points="all", # Para ver a cada estudiante como un punto
        labels={
            "Puntaje_Adiccion": "Nivel de Adicción",
            "Promedio_Horas_Uso_Diario": "Horas de Uso Diario"
        }
    )

    #quito la leyenda
    fig_uso.update_layout(showlegend=False)

    #mostrar en el dashboard
    st.plotly_chart(fig_uso, use_container_width=True)

    #analisis
    st.markdown("### 📝 Análisis de Intensidad de Uso vs Adicción")

    st.write("""
El diagrama de cajas y bigotes con muescas revela hallazgos estadísticos contundentes:

1. **Significancia Estadística:** Se observa que las **muescas no se solapan** entre la mayoría de los niveles (especialmente entre el nivel 6, 7, 8 y 9). Esto indica, con un **95% de confianza**, que las medianas de horas de uso diario son significativamente diferentes entre cada nivel de adicción.
2. **Relación Proporcional:** Existe una tendencia ascendente casi perfecta. A mayor puntaje de adicción, tanto la mediana como los cuartiles se desplazan hacia arriba, pasando de un uso de ~2 horas (Nivel 3) a más de **7 horas diarias** (Nivel 9).
3. **Dispersión de los Datos:** El nivel de adicción 7 muestra una caja más amplia y puntos más dispersos, lo que sugiere que es un "punto de quiebre" donde el comportamiento de los estudiantes varía más antes de estabilizarse en un uso intensivo crónico (niveles 8 y 9).
""")

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
    **Análisis:** En este gráfico se observa la distribución de los **{len(df)}** estudiantes según su plataforma principal. 
    Esto nos permite identificar qué redes sociales tienen mayor impacto en su rutina diaria.
    """)
