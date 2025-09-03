import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.colors as mcolors
from scipy import stats

# Configuración de la página
st.set_page_config(
    page_title="Análisis de Riesgo Crediticio",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cargar datos
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('Bankloan.csv', sep=';', encoding='utf-8-sig')
        return df
    except FileNotFoundError:
        st.error("El archivo Bankloan.csv no se ha encontrado.")
        return None

# Preprocesamiento de datos
def preprocess_data(df):
    # Limpieza de la columna default
    df['default'] = df['default'].astype(str)
    mapeo_valores = {'0': 0, '1': 1, "'0'": 0, ":0": 0}
    df['default'] = df['default'].map(mapeo_valores)
    df['default'] = df['default'].astype(int)
    
    # Crear etiquetas para default
    df['default_label'] = df['default'].map({0: 'Aprobado', 1: 'No Aprobado'})
    
    return df

# Aplicar estilos CSS personalizados con efectos modernos
def apply_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    
    
    .main-header {
        font-family: 'Inter', sans-serif;
        font-size: 3.5rem;
        font-weight: 700;
        color: #ffffff;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 0 4px 15px rgba(0,0,0,0.2);
        background: linear-gradient(45deg, #fff5ff, #ff00f5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .section-header {
        font-family: 'Inter', sans-serif;
        font-size: 1.8rem;
        font-weight: 600;
        color: #ffffff;
        margin-top: 3rem;
        margin-bottom: 2rem;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: .2rem;
        margin: .5rem 0;
        border: 1px solid rgba(255, 255, 255, 0.18);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
    }
    
    .chart-container {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: .2rem;
        margin: .5rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .chart-container:hover {
        transform: translateY(-3px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
    }
    
    .stPlotlyChart {
        border-radius: 15px;
        overflow: hidden;
    }
    
    .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        border: 2px solid #00f5ff;
        color: #333;
    }
    
    .stSlider > div > div > div > div {
        background-color: #00f5ff;
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #00f5ff, #ff00f5);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
        box-shadow: 0 10px 25px rgba(0, 245, 255, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 30px rgba(0, 245, 255, 0.4);
    }
    
    .sidebar-filter {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .navigation-buttons {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .nav-button {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 25px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 500;
    }
    
    .nav-button:hover {
        background: rgba(255, 255, 255, 0.3);
        transform: translateY(-2px);
    }
    
    .nav-button.active {
        background: linear-gradient(45deg, #00f5ff, #ff00f5);
        box-shadow: 0 10px 25px rgba(0, 245, 255, 0.3);
    }
    
    .stMetric {
        background: transparent;
    }
    
    .stMetric > div {
        background: transparent;
    }
    
    .stMetric label {
        color: rgba(255, 255, 255, 0.8) !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
    }
    
    .stMetric div[data-testid="metric-value"] {
        color: #ffffff !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }
    
    .stMetric div[data-testid="metric-delta"] {
        color: #00f5ff !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Función principal
def main():
    apply_custom_css()
    
    st.markdown('<h1 class="main-header">ANÁLISIS DE RIESGO CREDITICIO</h1>', unsafe_allow_html=True)
    
    # Cargar datos
    df = load_data()
    if df is None:
        return
    
    # Preprocesar datos
    df = preprocess_data(df)
    
    # Inicializar estado de sesión para navegación
    if 'chart_section' not in st.session_state:
        st.session_state.chart_section = 'overview'
    
    # Sidebar con efectos glassmorphism
    st.sidebar.markdown('<div class="sidebar-filter">', unsafe_allow_html=True)
    st.sidebar.title("🔍 Filtros Inteligentes")
    
    # Filtros interactivos con colores personalizados
    default_filter = st.sidebar.selectbox(
        "🏦 Estado del Préstamo",
        options=["Todos", "Aprobado", "No Aprobado"]
    )
    
    # Modificado: rango de edad hasta 100 años
    age_range = st.sidebar.slider(
        "👤 Rango de Edad",
        min_value=18,
        max_value=65,
        value=(int(df['age'].min()), min(int(df['age'].max()), 65))
    )
    
    income_range = st.sidebar.slider(
        "💰 Rango de Ingresos",
        min_value=int(df['income'].min()),
        max_value=int(df['income'].max()),
        value=(int(df['income'].min()), int(df['income'].max()))
    )
    
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    # Aplicar filtros
    filtered_df = df.copy()
    
    if default_filter != "Todos":
        default_value = 0 if default_filter == "Aprobado" else 1
        filtered_df = filtered_df[filtered_df['default'] == default_value]
    
    filtered_df = filtered_df[
        (filtered_df['income'] >= income_range[0]) & 
        (filtered_df['income'] <= income_range[1]) &
        (filtered_df['age'] >= age_range[0]) & 
        (filtered_df['age'] <= age_range[1])
    ]
    
    # KPIs con efecto glassmorphism
    st.markdown('<h2 class="section-header">📈 Métricas Clave</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Préstamos", f"{len(filtered_df):,}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        tasa_default = filtered_df['default'].mean() * 100
        st.metric("Tasa de Default", f"{tasa_default:.2f}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        ingreso_promedio = filtered_df['income'].mean()
        st.metric("Ingreso Promedio", f"${ingreso_promedio:,.0f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        edad_promedio = filtered_df['age'].mean()
        st.metric("Edad Promedio", f"{edad_promedio:.1f} años")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Navegación por secciones con botones
    st.markdown("""
    <div class="navigation-buttons">
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("📊 Resumen General"):
            st.session_state.chart_section = 'overview'
    
    with col2:
        if st.button("📈 Análisis Numérico"):
            st.session_state.chart_section = 'numeric'
    
    with col3:
        if st.button("🔗 Correlaciones"):
            st.session_state.chart_section = 'correlation'
    
    with col4:
        if st.button("📋 Variables Categóricas"):
            st.session_state.chart_section = 'categorical'
    
    with col5:
        if st.button("🎯 Análisis Avanzado"):
            st.session_state.chart_section = 'advanced'
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Mostrar gráficos según la sección seleccionada
    if st.session_state.chart_section == 'overview':
        show_overview_charts(filtered_df)
    elif st.session_state.chart_section == 'numeric':
        show_numeric_charts(filtered_df)
    elif st.session_state.chart_section == 'correlation':
        show_correlation_charts(filtered_df)
    elif st.session_state.chart_section == 'categorical':
        show_categorical_charts(filtered_df)
    elif st.session_state.chart_section == 'advanced':
        show_advanced_charts(filtered_df, df)

def show_overview_charts(filtered_df):
    st.markdown('<h2 class="section-header">📊 Resumen General</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        # Distribución de defaults con colores personalizados
        default_distribution = filtered_df['default_label'].value_counts()
        fig_default = px.pie(
            values=default_distribution.values,
            names=default_distribution.index,
            title="Distribución de Préstamos",
            color=default_distribution.index,
            color_discrete_map={'Aprobado': '#00f5ff', 'No Aprobado': '#ff6b6b'}
        )
        fig_default.update_traces(textposition='inside', textinfo='percent+label', textfont_size=14)
        fig_default.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=12)
        )
        st.plotly_chart(fig_default, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        # Distribución de ingresos
        fig_income = px.histogram(
            filtered_df, 
            x='income', 
            nbins=30,
            title='Distribución de Ingresos',
            color_discrete_sequence=['#00f5ff']
        )
        fig_income.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=12),
            xaxis_title="Ingresos",
            yaxis_title="Frecuencia"
        )
        st.plotly_chart(fig_income, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

def show_numeric_charts(filtered_df):
    st.markdown('<h2 class="section-header">📈 Análisis de Variables Numéricas</h2>', unsafe_allow_html=True)
    
    numeric_vars = ['age', 'ed', 'employ', 'address', 'income', 'debtinc', 'creddebt', 'othdebt']
    selected_var = st.selectbox("Selecciona una variable:", numeric_vars, key="numeric_var")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        # Histograma por estado de préstamo
        fig_hist = px.histogram(
            filtered_df, 
            x=selected_var, 
            color='default_label',
            title=f'Distribución de {selected_var}',
            color_discrete_map={'Aprobado': '#00f5ff', 'No Aprobado': '#ff6b6b'},
            barmode='overlay',
            opacity=0.7
        )
        fig_hist.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=12)
        )
        st.plotly_chart(fig_hist, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        # Box plot
        fig_box = px.box(
            filtered_df, 
            x='default_label', 
            y=selected_var,
            title=f'Box Plot de {selected_var}',
            color='default_label',
            color_discrete_map={'Aprobado': '#00f5ff', 'No Aprobado': '#ff6b6b'}
        )
        fig_box.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=12)
        )
        st.plotly_chart(fig_box, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

def show_correlation_charts(filtered_df):
    st.markdown('<h2 class="section-header">🔗 Análisis de Correlación</h2>', unsafe_allow_html=True)
    
    numeric_vars = ['age', 'ed', 'employ', 'address', 'income', 'debtinc', 'creddebt', 'othdebt', 'default']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        # Matriz de correlación mejorada
        corr_matrix = filtered_df[numeric_vars].corr()
        
        # Redondear a 2 decimales
        corr_matrix_rounded = corr_matrix.round(2)
        
        fig_corr = px.imshow(
            corr_matrix_rounded,
            title="Matriz de Correlación",
            aspect="auto",
            color_continuous_scale=['#ff6b6b','white', '#00f5ff'],
            text_auto=True# Mostrar valores en las celdas
        )
        fig_corr.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=10)
        )
        fig_corr.update_traces(
            textfont=dict(color='black', size=10)
        )
        st.plotly_chart(fig_corr, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        # Correlación con default
        default_corr = corr_matrix['default'].drop('default').sort_values(key=abs, ascending=False)
        
        fig_default_corr = px.bar(
            x=default_corr.index,
            y=default_corr.values.round(2),
            title='Correlación con Default',
            color=default_corr.values,
            color_continuous_scale=['#ff6b6b','white', '#00f5ff'],
        )
        fig_default_corr.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=12),
            xaxis_title="Variables",
            yaxis_title="Correlación"
        )
        st.plotly_chart(fig_default_corr, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

def show_categorical_charts(filtered_df):
    st.markdown('<h2 class="section-header">📋 Variables Categóricas</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        # Distribución por educación
        if 'ed' in filtered_df.columns:
            ed_distribution = filtered_df['ed'].value_counts().sort_index()
            fig_ed = px.bar(
                x=ed_distribution.index.astype(str),
                y=ed_distribution.values,
                title='Distribución por Nivel Educativo',
                color=ed_distribution.values,
                color_continuous_scale=['#ff6b6b','white', '#00f5ff']
            )
            fig_ed.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', size=12)
            )
            st.plotly_chart(fig_ed, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        # Scatter plot ingresos vs deuda
        fig_scatter = px.scatter(
            filtered_df,
            x='income',
            y='debtinc',
            color='default_label',
            title='Ingresos vs Ratio de Deuda',
            color_discrete_map={'Aprobado': '#00f5ff', 'No Aprobado': '#ff6b6b'},
            opacity=0.7
        )
        fig_scatter.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=12)
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

def show_advanced_charts(filtered_df, df):
    st.markdown('<h2 class="section-header">🎯 Análisis Avanzado</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        # Gráfico 3D
        if all(col in filtered_df.columns for col in ['age', 'income', 'debtinc', 'default_label']):
            fig_3d = px.scatter_3d(
                filtered_df.sample(min(500, len(filtered_df))),  # Limitar puntos para performance
                x='age',
                y='income',
                z='debtinc',
                color='default_label',
                title='Análisis 3D: Edad, Ingresos, Deuda',
                color_discrete_map={'Aprobado': '#00f5ff', 'No Aprobado': '#ff6b6b'},
                opacity=0.7
            )
            fig_3d.update_layout(
                scene=dict(
                    bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(backgroundcolor='rgba(0,0,0,0)', gridcolor='white'),
                    yaxis=dict(backgroundcolor='rgba(0,0,0,0)', gridcolor='white'),
                    zaxis=dict(backgroundcolor='rgba(0,0,0,0)', gridcolor='white')
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', size=12)
            )
            st.plotly_chart(fig_3d, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        # Análisis de valores faltantes
        missing_values = df.isnull().sum()
        missing_percentage = (missing_values / len(df)) * 100
        missing_df = pd.DataFrame({
            'Valores_Faltantes': missing_values, 
            'Porcentaje': missing_percentage.round(2)
        }).sort_values('Porcentaje', ascending=False)
        missing_df = missing_df[missing_df['Valores_Faltantes'] > 0]
        
        if not missing_df.empty:
            fig_missing = px.bar(
                missing_df,
                x=missing_df.index,
                y='Porcentaje',
                title='Valores Faltantes (%)',
                color='Porcentaje',
                color_continuous_scale='Reds'
            )
            fig_missing.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', size=12)
            )
            st.plotly_chart(fig_missing, use_container_width=True)
        else:
            st.info("No hay valores faltantes en el dataset")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Información del dataset en un expander con estilo
    with st.expander("🔍 Ver información detallada del dataset"):
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("📊 Información del Dataset")
        st.write(f"**Dimensiones:** {df.shape[0]:,} filas x {df.shape[1]} columnas")
        
        st.subheader("📈 Estadísticas Descriptivas")
        st.dataframe(df.describe().round(2), use_container_width=True)
        
        st.subheader("👀 Muestra del Dataset")
        st.dataframe(df.head(10), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()