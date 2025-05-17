import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time
import datetime

# Konfiguracja strony
st.set_page_config(
    page_title="ATLAS STREAMLIT PLAYGROUND",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Niestandardowe style CSS
st.markdown("""
<style>
:root {
    --primary-color: #31817A;
    --background-color: #0F172A;
}

.stApp {
    background-color: var(--background-color);
    color: #F8FAFC;
}

.dashboard-section {
    background-color: #1E293B;
    border-radius: 15px;
    padding: 25px;
    margin: 15px 0;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}

.code-container {
    background-color: #1E293B;
    border-radius: 8px;
    padding: 15px;
    margin: 15px 0;
    font-family: 'Fira Code', monospace;
}

.chart-header {
    border-left: 4px solid #31817A;
    padding-left: 15px;
    margin: 20px 0;
}

.metric-card {
    background: #1E293B;
    border-radius: 10px;
    padding: 20px;
    margin: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# Funkcje pomocnicze
def show_full_code(code):
    st.code(code)

def generate_sample_data(rows=100, noise=0.5):
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', periods=rows)
    sales = np.cumsum(np.random.randn(rows)) * (1 + noise)
    costs = sales * 0.6 + np.random.normal(0, noise, rows)
    return pd.DataFrame({
        'Data': dates,
        'Sprzedaż': sales,
        'Koszty': costs,
        'Zysk': sales - costs
    })

# Inicjalizacja stanu
if "dashboard_data" not in st.session_state:
    st.session_state.dashboard_data = generate_sample_data()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Panel boczny
with st.sidebar:
    st.title("Menu główne")
    menu_option = st.selectbox(
        "Wybierz sekcję:",
        ["Interakcja", "Wizualizacje", "Dane", "Czat", "Playground", "Dashboard"]
    )

    st.markdown("---")
    with st.expander("Konfiguracja danych"):
        data_points = st.slider("Liczba dni", 30, 365, 100)
        noise_level = st.slider("Zmienność danych", 0.0, 1.0, 0.3)
        
        if st.button("Aktualizuj dane"):
            st.session_state.dashboard_data = generate_sample_data(data_points, noise_level)

# Główne sekcje
if menu_option == "Interakcja":
    st.header("🎮 Elementy Interaktywne")
    
    with st.expander("Podstawowe Kontrolki", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            slider_val = st.slider("Wybierz wartość", 0, 100, 50)
            show_full_code("""
            slider_val = st.slider(
                "Wybierz wartość", 
                0, 100, 50,
                help="Przykładowy suwak z wartościami 0-100"
            )
            """)
            
        with col2:
            color_val = st.color_picker("Wybierz kolor", "#31817A")
            show_full_code("""
            color_val = st.color_picker(
                "Wybierz kolor główny", 
                "#31817A",
                help="Wybierz kolor z palety"
            )
            """)

elif menu_option == "Wizualizacje":
    st.header("📊 Wizualizacje Danych")
    
    with st.expander("Dynamiczne Wykresy", expanded=True):
        chart_type = st.selectbox("Typ wizualizacji:", ["Linowy", "Słupkowy", "Mapa cieplna"])
        data = st.session_state.dashboard_data
        
        if chart_type == "Linowy":
            fig = px.line(data, x='Data', y=['Sprzedaż', 'Koszty', 'Zysk'])
            st.plotly_chart(fig, use_container_width=True)
            show_full_code("""
            fig = px.line(data, x='Data', y=['Sprzedaż', 'Koszty', 'Zysk'])
            st.plotly_chart(fig)
            """)
            
        elif chart_type == "Słupkowy":
            fig = px.bar(data.melt(id_vars='Data'), 
                        x='Data', y='value', color='variable', barmode='group')
            st.plotly_chart(fig, use_container_width=True)
            show_full_code("""
            fig = px.bar(data.melt(id_vars='Data'), 
                        x='Data', y='value', color='variable')
            """)
            
        else:
            fig = px.density_heatmap(data, x='Data', y='Zysk', marginal_x="histogram")
            st.plotly_chart(fig, use_container_width=True)
            show_full_code("""
            fig = px.density_heatmap(data, x='Data', y='Zysk')
            """)

elif menu_option == "Dane":
    st.header("📁 Zarządzanie Danymi")
    
    with st.expander("Edycja Danych", expanded=True):
        edited_df = st.data_editor(
            st.session_state.dashboard_data,
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "Data": st.column_config.DateColumn("Data"),
                "Sprzedaż": st.column_config.NumberColumn(format="%.2f zł"),
                "Koszty": st.column_config.NumberColumn(format="%.2f zł"),
                "Zysk": st.column_config.NumberColumn(format="%.2f zł")
            }
        )
        show_full_code("""
        edited_df = st.data_editor(
            data,
            column_config={
                "Data": st.column_config.DateColumn(),
                "Sprzedaż": st.column_config.NumberColumn(format="%.2f zł"),
                ...
            }
        )
        """)

elif menu_option == "Czat":
    st.header("💬 Komunikator")
    
    with st.container():
        for msg in st.session_state.chat_history:
            bg_color = "#31817A55" if msg['role'] == 'assistant' else "#2563EB"
            st.markdown(f"""
            <div style="
                background: {bg_color};
                border-radius: 10px;
                padding: 15px;
                margin: 10px 0;
                color: white;
            ">
                <small>{msg['time']}</small>
                <p><b>{msg['role'].title()}:</b> {msg['content']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        if prompt := st.chat_input("Zadaj pytanie..."):
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            st.session_state.chat_history.append({
                'role': 'user',
                'content': prompt,
                'time': timestamp
            })
            
            time.sleep(0.5)
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': "Atlas to najlepsze koło naukowe w Polsce! 🚀",
                'time': datetime.datetime.now().strftime("%H:%M:%S")
            })
            st.rerun()
        
        show_full_code("""
        if prompt := st.chat_input("Zadaj pytanie..."):
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            st.session_state.chat_history.append({
                'role': 'user',
                'content': prompt,
                'time': timestamp
            })
            
            time.sleep(0.5)
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': "Atlas to najlepsze koło naukowe w Polsce! 🚀",
                'time': datetime.datetime.now().strftime("%H:%M:%S")
            })
            st.rerun()
        """)

elif menu_option == "Playground":
    st.header("🚀 Sandbox Programistyczny")
    
    default_code = """import streamlit as st
import pandas as pd
import numpy as np

# Przykładowy dashboard
st.title("Mój Dashboard")
data = pd.DataFrame({
    'Data': pd.date_range(start='2023-01-01', periods=100),
    'Wartości': np.random.randn(100).cumsum()
})

st.line_chart(data, x='Data', y='Wartości')
"""
    
    user_code = st.text_area("Wprowadź własny kod:", value=default_code, height=400)
    
    if st.button("Wykonaj kod"):
        try:
            exec(user_code)
        except Exception as e:
            st.error(f"Błąd wykonania: {str(e)}")

elif menu_option == "Dashboard":
    st.header("📈 Interaktywny Dashboard Biznesowy")
    
    data = st.session_state.dashboard_data
    
    with st.container():
        st.markdown('<div class="dashboard-section">', unsafe_allow_html=True)
        
        # Sekcja metryk
        st.markdown("### Kluczowe Wskaźniki")
        cols = st.columns(3)
        metrics = {
            "Średnia sprzedaż": data['Sprzedaż'].mean(),
            "Całkowity zysk": data['Zysk'].sum(),
            "Maksymalny zysk": data['Zysk'].max()
        }
        
        for col, (name, value) in zip(cols, metrics.items()):
            with col:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>{name}</h4>
                    <h2>{value:,.2f} zł</h2>
                </div>
                """, unsafe_allow_html=True)
        
        show_full_code("""
        cols = st.columns(3)
        metrics = {'Średnia sprzedaż': data['Sprzedaż'].mean(), ...}
        for col, (name, value) in zip(cols, metrics.items()):
            with col:
                st.markdown(f'<div class="metric-card">...</div>')
        """)
        
        # Sekcja wykresów
        st.markdown('<div class="chart-header"><h3>Analiza Trendów</h3></div>', unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["Trendy miesięczne", "Analiza korelacji"])
        
        with tab1:
            fig = px.line(data, x='Data', y=['Sprzedaż', 'Koszty', 'Zysk'])
            st.plotly_chart(fig, use_container_width=True)
            show_full_code("""
            fig = px.line(data, x='Data', y=['Sprzedaż', 'Koszty', 'Zysk'])
            fig.update_layout(showlegend=True)
            """)
            
        with tab2:
            fig = px.scatter_matrix(data[['Sprzedaż', 'Koszty', 'Zysk']])
            st.plotly_chart(fig, use_container_width=True)
            show_full_code("""
            fig = px.scatter_matrix(data[['Sprzedaż', 'Koszty', 'Zysk']])
            """)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Stopka
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px;">
    <p>🧪 ATLAS STREAMLIT PLAYGROUND 🧪</p>
    <small>Mateusz Walo & Patryk Marek</small>
</div>
""", unsafe_allow_html=True)