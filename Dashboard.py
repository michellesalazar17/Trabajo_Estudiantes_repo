import streamlit as st
import plotly.express as px
import pandas as pd

#Titulo
st.title("Analisis de Adiccion a las Redes Sociales y el Bienestar Estudiantil")

#carga de datos
df_final = pd.read_csv("Estudiantes_final.csv", encoding="latin1")

df = df_final.rename(columns={col: "Horas_Sueno" for col in df_final.columns if "Sue" in col})

df.columns = df.columns.str.strip()

#anadiendo filtro
st.sidebar.title("Panel de Control")
st.sidebar.markdown("Usa estos filtros para actualizar los gráficos:")

#filtro por País
paises = ["Todos"] + list(df['Pais'].unique())
pais_seleccionado = st.sidebar.selectbox("🌍 Selecciona un País:", paises)

#filtro por Nivel Académico 
niveles = ["Todos"] + list(df['Nivel_Academico'].unique())
nivel_seleccionado = st.sidebar.multiselect("🎓 Nivel Academico:", niveles, default="Todos")

df_filtrado = df.copy()

if pais_seleccionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado['Pais'] == pais_seleccionado]

if "Todos" not in nivel_seleccionado and len(nivel_seleccionado) > 0:
    df_filtrado = df_filtrado[df_filtrado['Nivel_Academico'].isin(nivel_seleccionado)]

#empieza la fiesta
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊Valores claves", "📝Rendimiento Academico", "🧠Bienestar Estudiantil", "📱Plataformas Mas Usada", "📉Nivel de Adiccion"])

with tab1:
    
    st.caption("Nota: los datos presentados provienen del dataset Estudiantes_final.csv, que refleja el bienestar de los estudiantes enfente del uso de las redes sociales ")

    #calculamos los valores clave
    media_uso = df_filtrado['Promedio_Horas_Uso_Diario'].mean()
    mediana_adiccion = df_filtrado['Puntaje_Adiccion'].median()
    total_estudiantes = len(df_filtrado)
    uso_maximo = df_filtrado['Promedio_Horas_Uso_Diario'].max()
    uso_minimo = df_filtrado['Promedio_Horas_Uso_Diario'].min()
    maximo_adiccion = df_filtrado['Puntaje_Adiccion'].max()
    minimo_adiccion = df_filtrado['Puntaje_Adiccion'].min()
    conteo = df_filtrado['Afecta_Rendimiento_Academico'].value_counts()
    #extraer los numeros
    si_afecta = conteo.get('Yes', 0)
    no_afecta = conteo.get('No', 0)

    #creo columnas
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Promedio Uso Diario", f"{media_uso:.1f} horas")
        st.caption("Media aritmética del tiempo en pantalla.")

        st.divider()

        st.metric("", f"{uso_maximo} horas/día")
        st.caption("hora de uso maxima")

        st.divider()
        
        st.metric("", f"{uso_minimo} horas/día")
        st.caption("hora de uso minima")

    with col2:
        st.metric("Mediana de Adicción", f"{mediana_adiccion:.0f} pts")
        st.caption("Punto medio de la escala de adicción.")

        st.divider()

        st.metric("", f"{maximo_adiccion} pts")
        st.caption("nivel maximo de adiccion")

        st.divider()

        st.metric("", f"{minimo_adiccion} pts")
        st.caption("nivel minimo de adiccion")

    with col3:
        st.metric("Total Estudiantes", total_estudiantes)
        st.caption("Muestra total analizada.")

        st.divider()

        st.metric("", value=f"{si_afecta} personas")
        st.caption("Si les afecto su rendimiento academico")

        st.divider()

        st.metric("", value=f"{no_afecta} personas")
        st.caption("No les afecto su rendimiento academico")

with tab2:
    
    st.caption("Nota: los datos presentados provienen del dataset Estudiantes_final.csv, que refleja el bienestar de los estudiantes enfente del uso de las redes sociales ")

    st.subheader("Impacto en el Rendimiento")
    
    #grafico de caja
    fig_rendimiento = px.box(df_filtrado,
        x="Afecta_Rendimiento_Academico", 
        y="Puntaje_Adiccion",
        color="Afecta_Rendimiento_Academico",
        title="Distribución de Adicción según Impacto Académico")
    st.plotly_chart(fig_rendimiento)

    #analisis
    st.markdown("### 📊 Analisis de Resultados")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Diferencia de Medianas:**")
        st.write("""
        * **Grupo 'No'**: Los estudiantes muestran una mediana de adicción de **6 puntos**.
        * **Grupo 'Yes'**: La mediana sube a **8 puntos**, indicando una relación directa entre adicción y afectación académica.
        """)

    with col2:
        st.write("**Dispersion y Riesgo:**")
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
    st.write(f"El nivel educativo que mas tiempo pasa en redes sociales es **{nivel_max}**, con un promedio de **{horas_max:.2f} horas** diarias.")

    st.divider()

    df_conteo = df_filtrado['Afecta_Rendimiento_Academico'].value_counts().reset_index()
    df_conteo.columns = ['Afecta_Rendimiento_Academico', 'total']

    #crear el grafico de torta
    fig = px.pie(
        df_conteo, 
        values='total', 
        names='Afecta_Rendimiento_Academico',
        hole=0.5, # estilo dona
        color='Afecta_Rendimiento_Academico',
        color_discrete_map={'Yes': '#ADD8E6', 'No': '#00008B'},
        title="Porcentaje de Estudiantes que les Afecta el uso de redes sociales"
    )

    fig.update_layout(showlegend=False)

    fig.update_traces(textposition='inside', textinfo='percent+label')

    fig.update_layout(template="plotly_dark")

    st.plotly_chart(fig, use_container_width=True)

st.markdown("---") 

#ventana desplegable
with st.expander("📂 Haz clic aquí para ver la Base de Datos completa"):
    st.write("A continuación se muestran los datos originales filtrados:")
    
    st.dataframe(
        df_filtrado, 
        use_container_width=True, 
        column_config={
            "Puntaje_Adiccion": st.column_config.NumberColumn("Nivel Adicción", format="%d ⭐"),
            "Promedio_Horas_Uso_Diario": st.column_config.NumberColumn("Horas Uso", format="%.1f h")
        }
    )

with tab3:
    
    st.caption("Nota: los datos presentados provienen del dataset Estudiantes_final.csv, que refleja el bienestar de los estudiantes enfente del uso de las redes sociales ")

    st.markdown("### 📉 Tendencia: Horas de Sueño por Nivel de Adiccion")

    #agrupar para obtener el promedio de horas de sueño por cada nivel de adiccion
    df_sueno_tendencia = df_filtrado.groupby('Puntaje_Adiccion')['Horas_Sueno'].mean().reset_index()

    #crear el grafico de lineas con puntos
    fig_linea_sueno = px.line(
        df_sueno_tendencia,
        x='Puntaje_Adiccion',
        y='Horas_Sueno',
        title="Relación entre Nivel de Adicción y Promedio de Horas de Sueño",
        markers=True, 
        labels={
            'Puntaje_Adiccion': 'Nivel de Adicción (1-10)',
            'Horas_Sueno': 'Promedio Horas de Sueño'
        }
    )

    fig_linea_sueno.update_traces(
        line_color='#ADD8E6', 
        marker=dict(size=10, symbol='circle', line=dict(width=2, color='DarkSlateGrey'))
    )

    st.plotly_chart(fig_linea_sueno, use_container_width=True)

    st.subheader("Interpretacion")
    
    st.write("""1. **Punto de Quiebre:** Se observa que hasta el nivel 6 de adicción, el promedio de sueño se mantiene estable (cerca de las 7.5 - 8 horas).
2. **Correlación Negativa:** A partir del nivel 6, existe una caída drástica. Los estudiantes con nivel 9 de adicción apenas alcanzan las **5.3 horas** de sueño promedio.
3. **Impacto Crítico:** Existe una diferencia de casi **2.5 horas de sueño** entre un estudiante con adicción baja y uno con adicción alta.
""")

    st.divider() 

    st.header("Distribución de Salud Mental según Nivel de Adicción")

    st.subheader("Relación: Salud Mental vs Adicción")

    #agrupo los datos par ver la frecuencia y cuantas personas hay en cada cruce del puntaje
    df_burbujas = df_filtrado.groupby(['Puntaje_Adiccion', 'Puntaje_Salud_Mental']).size().reset_index(name='Cantidad_Estudiantes')

    #creacion grafico de burbujas
    fig_burbujas = px.scatter(
        df_burbujas,
        x="Puntaje_Adiccion",
        y="Puntaje_Salud_Mental",
        size="Cantidad_Estudiantes", 
        color="Puntaje_Salud_Mental", 
        hover_name="Cantidad_Estudiantes", 
        title="Gráfico de Burbujas: Frecuencia de Salud Mental por Adicción",
        labels={
            "Puntaje_Adiccion": "Nivel de Adicción",
            "Puntaje_Salud_Mental": "Nivel de Salud Mental",
            "Cantidad_Estudiantes": "Nro. de Estudiantes"
        },
        size_max=40
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
        title="Evolución del tiempo de uso segun la adicción",
        color_discrete_sequence=['#ADD8E6'] 
    )

    fig_tendencia.update_layout(
        template="plotly_dark",
        xaxis=dict(dtick=1), 
        xaxis_title="Nivel de Adiccion (Puntaje)",
        yaxis_title="Horas de Uso (Promedio)",
        showlegend=False
    )

    st.plotly_chart(fig_tendencia, use_container_width=True)

    st.markdown("### 📝 Analisis de Resultados: Uso Diario vs. Adiccion")

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

    #conclusion
    st.write(f"""
**💡 Conclusión:** Los datos sugieren que el tiempo de exposición a las pantallas es un factor determinante en la percepción de adicción. 
Un uso superior a las **6 horas diarias** coincide sistemáticamente con los niveles de adicción más elevados en la muestra.
""")


with tab4:
    
    st.caption("Nota: los datos presentados provienen del dataset Estudiantes_final.csv, que refleja el bienestar de los estudiantes enfente del uso de las redes sociales ")

    st.subheader("Análisis de las Plataformas más Utilizadas")

    #colores a la app 
    colores_app = {
        "Instagram" : "#E1306C",
        "TikTok" : "#000000",
        "WhatsApp" : "#25D366",
        "Facebook" : "#1877F2",
        'Twitter' : "#1DA1F2"
    }

    #cuantas veces sale
    conteo_plataformas = df_filtrado['Plataforma_Mas_Usada'].value_counts().reset_index()
    conteo_plataformas.columns = ['Plataforma', 'Cantidad']

    #grafico de barras
    fig_plataformas = px.bar(
        conteo_plataformas, 
        x='Plataforma', 
        y='Cantidad',
        title="Ranking de Popularidad por Red Social",
        labels={'Cantidad': 'Numero de Estudiantes', 'Plataforma': 'Red Social'},
        color='Plataforma',
        color_discrete_map= colores_app,
        text_auto=True 
    )
    
    st.plotly_chart(fig_plataformas)

    #analisis
    st.markdown(f"""
    **Análisis:** En este gráfico se observa la distribución de los **{len(df)}** estudiantes según su plataforma principal. 
    Esto nos permite identificar qué redes sociales tienen mayor impacto en su rutina diaria.
    """)

with tab5:
    
    st.caption("Nota: los datos presentados provienen del dataset Estudiantes_final.csv, que refleja el bienestar de los estudiantes enfente del uso de las redes sociales ")
 
    df_promedio_adiccion = df_filtrado.groupby('Pais')['Puntaje_Adiccion'].mean().reset_index()

    #ordenar de mayor a menor 
    df_promedio_adiccion = df_promedio_adiccion.sort_values(by='Puntaje_Adiccion', ascending=True)

    st.subheader("Ranking de Adiccion Promedio por Pais")

    #crear el gráfico de barras horizontales 
    fig_ranking = px.bar(
        df_promedio_adiccion,
        x='Puntaje_Adiccion',
        y='Pais',
        orientation='h', 
        title="Nivel de Adiccion Promedio (USA, India, Canadá)",
        text_auto='.2f', 
        color='Puntaje_Adiccion', 
        color_continuous_scale='Blues' 
)

    fig_ranking.update_layout(
        template="plotly_dark",
        xaxis_title="Promedio del Puntaje",
        yaxis_title="",
        coloraxis_showscale=False #oculta la barra de colores lateral
    )

    st.plotly_chart(fig_ranking, use_container_width=True)

    st.divider()

    st.markdown("### 📊 Impacto en el Rendimiento por Plataforma")

    #agrupamos los datos para contar estudiantes por Red Social y si les afecta
    df_impacto_plataforma = df_filtrado.groupby(['Plataforma_Mas_Usada', 'Afecta_Rendimiento_Academico']).size().reset_index(name='Cantidad_Estudiantes')

    #crear el gráfico de barras agrupadas
    fig_impacto = px.bar(
        df_impacto_plataforma, 
        x='Plataforma_Mas_Usada', 
        y='Cantidad_Estudiantes', 
        color='Afecta_Rendimiento_Academico',
        barmode='group', 
        title="Distribucion de Impacto Academico según Red Social",
        labels={
            'Plataforma_Mas_Usada': 'Plataforma', 
            'Cantidad_Estudiantes': 'Numero de Estudiantes',
            'Afecta_Rendimiento_Academico': '¿Afecta?'
        },
        color_discrete_map={'Yes': '#EF553B', 'No': '#636EFA'}, 
        text_auto=True 
    )

    #mostrar el grafico
    st.plotly_chart(fig_impacto, use_container_width=True)
    


