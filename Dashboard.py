import streamlit as st
import plotly.express as px
import pandas as pd

#Titulo
st.title("Analisis de Adiccion a las Redes Sociales y el Bienestar Estudiantil")

#carga de datos
df_final = pd.read_csv("Estudiantes_final.csv", encoding="latin1")

df = df_final.rename(columns={col: "Horas_Sueno" for col in df_final.columns if "Sue" in col})

df.columns = df.columns.str.strip()

st.sidebar.title("Panel de Control")
st.sidebar.markdown("Usa estos filtros para actualizar los gráficos:")

#filtro por País
paises = ["Todos"] + list(df['Pais'].unique())
pais_seleccionado = st.sidebar.selectbox("🌍 Selecciona un País:", paises)

#filtro por Nivel Académico 
niveles = ["Todos"] + list(df['Nivel_Academico'].unique())
nivel_seleccionado = st.sidebar.multiselect("🎓 Nivel Académico:", niveles, default="Todos")

df_filtrado = df.copy()

if pais_seleccionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado['Pais'] == pais_seleccionado]

if "Todos" not in nivel_seleccionado and len(nivel_seleccionado) > 0:
    df_filtrado = df_filtrado[df_filtrado['Nivel_Academico'].isin(nivel_seleccionado)]

#empieza la fiesta
tab1, tab2, tab3, tab4 = st.tabs(["Rendimiento Academico", "Bienestar Estudiantil", "Plataformas Mas Usada", "Nivel de Adiccion"])

with tab1:
    st.subheader("Impacto en el Rendimiento")
    
    #gráfico (Box Plot)
    fig_rendimiento = px.box(df_filtrado,
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

    #agrupar y calcular el promedio
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

    st.divider()

    df_conteo = df_filtrado['Afecta_Rendimiento_Academico'].value_counts().reset_index()
    df_conteo.columns = ['Afecta_Rendimiento_Academico', 'total']

    # 3. Crear el gráfico de torta
    fig = px.pie(
        df_conteo, 
        values='total', 
        names='Afecta_Rendimiento_Academico',
        hole=0.5, # Estilo donut
        color='Afecta_Rendimiento_Academico',
        color_discrete_map={'Yes': '#ADD8E6', 'No': '#00008B'},
        title="Porcentaje de Estudiantes que les Afecta el uso de redes sociales"
    )

    fig.update_layout(showlegend=False)

    fig.update_traces(textposition='inside', textinfo='percent+label')

    fig.update_layout(template="plotly_dark")

    st.plotly_chart(fig, use_container_width=True)

    total_alumnos = df_conteo['total'].sum()
    st.write(f"Total de estudiantes analizados: **{total_alumnos}**")

st.markdown("---") # Línea divisoria

# Creamos la "ventana" desplegable
with st.expander("📂 Haz clic aquí para ver la Base de Datos completa"):
    st.write("A continuación se muestran los datos originales filtrados:")
    
    # Mostramos el dataframe interactivo
    st.dataframe(
        df_filtrado, 
        use_container_width=True, # Para que ocupe todo el ancho
        column_config={
            "Puntaje_Adiccion": st.column_config.NumberColumn("Nivel Adicción", format="%d ⭐"),
            "Promedio_Horas_Uso_Diario": st.column_config.NumberColumn("Horas Uso", format="%.1f h")
        }
    )

with tab2:
    st.subheader("Adicción vs Sueño")
    
    # creacion del histograma
    fig_hist = px.histogram(
    df_filtrado, 
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
    df_burbujas = df_filtrado.groupby(['Puntaje_Adiccion', 'Puntaje_Salud_Mental']).size().reset_index(name='Cantidad_Estudiantes')

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

    df_linea = df_filtrado.groupby('Puntaje_Adiccion')['Promedio_Horas_Uso_Diario'].mean().reset_index()

    df_linea = df_linea.sort_values(by='Puntaje_Adiccion')

    st.subheader("Tendencia de Uso Diario por Nivel de Adicción")

    fig_tendencia = px.line(
        df_linea, 
        x='Puntaje_Adiccion', 
        y='Promedio_Horas_Uso_Diario',
        markers=True,
        title="Evolución del tiempo de uso según la adicción",
        color_discrete_sequence=['#ADD8E6'] 
    )

    fig_tendencia.update_layout(
        template="plotly_dark",
        xaxis=dict(dtick=1), # Muestra todos los números del 1 al 10 en el eje X
        xaxis_title="Nivel de Adicción (Puntaje)",
        yaxis_title="Horas de Uso (Promedio)",
        showlegend=False
    )

    st.plotly_chart(fig_tendencia, use_container_width=True)

    st.markdown("### 📝 Análisis de Resultados: Uso Diario vs. Adicción")

    col_a, col_b = st.columns([1, 1])

    with col_a:
        st.write("""
    **Observación de la Tendencia:**
    Se identifica una **correlación positiva directa** entre las horas de uso y el nivel de adicción. 
    A medida que el usuario se desplaza del nivel 3 al nivel 9, el promedio de horas de uso se triplica.
    """)

    with col_b:
        st.write("""
    **Punto Crítico:**
    El salto más significativo ocurre a partir del **nivel 7**, donde el uso diario supera las 5 horas promedio, 
    estabilizándose en niveles críticos (7 horas) para los puntajes de adicción más altos (8 y 9).
    """)

    #conclusión general
    st.write(f"""
**💡 Conclusión:** Los datos sugieren que el tiempo de exposición a las pantallas es un factor determinante en la percepción de adicción. 
Un uso superior a las **6 horas diarias** coincide sistemáticamente con los niveles de adicción más elevados en la muestra.
""")


with tab3:
    st.subheader("Análisis de las Plataformas más Utilizadas")

    #cuantas veces sale
    conteo_plataformas = df_filtrado['Plataforma_Mas_Usada'].value_counts().reset_index()
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

with tab4:
    df_promedio_adiccion = df_filtrado.groupby('Pais')['Puntaje_Adiccion'].mean().reset_index()

    #ordenar de mayor a menor 
    df_promedio_adiccion = df_promedio_adiccion.sort_values(by='Puntaje_Adiccion', ascending=True)

    st.subheader("Ranking de Adicción Promedio por País")

    #crear el gráfico de barras horizontales 
    fig_ranking = px.bar(
        df_promedio_adiccion,
        x='Puntaje_Adiccion',
        y='Pais',
        orientation='h', 
        title="Nivel de Adicción Promedio (USA, India, Canadá)",
        text_auto='.2f', 
        color='Puntaje_Adiccion', 
        color_continuous_scale='Blues' 
)

    fig_ranking.update_layout(
        template="plotly_dark",
        xaxis_title="Promedio del Puntaje",
        yaxis_title="",
        coloraxis_showscale=False # Oculta la barra de colores lateral
    )

    st.plotly_chart(fig_ranking, use_container_width=True)
    


