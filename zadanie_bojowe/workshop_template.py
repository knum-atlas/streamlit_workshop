import streamlit as st

from utils import (
    load_data,
    prepare_data,
    train_model,
    round_p,
    produce_confusion,
)

st.set_page_config(page_title="Pracowania Alchemiczna", layout="wide")
st.title("Magiczne Mikstury: Lekarstwo na chorobę")

# --- Ładowanie i przygotowanie danych ---
df, y = load_data()  # df - zawiera zmienne x, y - zmienna docelowa
X_train, X_test, y_train, y_test = prepare_data(df, y)

# --- Przygotowanie stanu sesji ---
if "model" not in st.session_state:
    st.session_state.model = None

if "scores" not in st.session_state:
    st.session_state.scores = {}

# --- Zakładki ---
tab1, tab2, tab3 = st.tabs(["🧪 Przygotuj recepturę", "🔮 Zajrzyj w nieznane", "📈 Twoja alchemiczna wizja"])

# --- Tab 1: Trenowanie modelu ---
with tab1:
    st.markdown("""
    ## Zadania
    Nadworny alchemiku! Twoim zadaniem jest przygotowanie magicznej receptury w oparciu o magiczne knieje (random forest).

    🎯 **Wymagane:**
    - Wyświetl dane na których będziesz działać
    - Dodaj opcję dostosowania hiperparametrów
    - Wyświetl metryki jakości modelu (train/test score, precision, recall, f1)
    - Dodaj wizualizację macierzy pomyłek

    🧠 **Dodatkowe wyzwania:**
    - Pokoloruj metryki (np. używając `delta` lub kolorów)
    - Zmierz czas trenowania modelu i pokaż użytkownikowi
    """)

    with st.expander("🔍 Podgląd danych"):
        pass
        # TODO: dodaj podgląd danych

    with st.sidebar.form(key="hyperparameters_form"):
        st.header("⚙️ Ustawienia modelu Random Forest")

        st.markdown("""
        **Opis parametrów:**
        - `n_estimators` – liczba drzew w lesie (np. 50–200)
        - `max_depth` – maksymalna głębokość drzewa (np. 5–30)
        - `min_samples_split` – minimalna liczba próbek potrzebnych do podziału węzła (np. 2–10)
        - `min_samples_leaf` – minimalna liczba próbek w liściu (np. 1–5)
        - `criterion` – sposób mierzenia jakości podziału (`gini`, `entropy`, `log_loss`)
        - `bootstrap` – czy losować próbki z powtórzeniami

        Możesz eksperymentować z ustawieniami!
        """)

        # TODO: dodaj widgety do ustawienia parametrów modelu
        # random_state = st.slider(...)
        # criterion = st.selectbox(...)
        # n_estim = st.slider(...)
        # ...

        submit_button = st.form_submit_button("Trenuj Model", type="primary")

    if submit_button:
        # TODO: zbierz hiperparametry w słowniku hyperparams
        hyperparams = {
            # "random_state": random_state,
            # ...
        }

        # Wywołanie funkcji trenującej
        (
            train_score,
            test_score,
            precision,
            recall,
            f1,
            confusion,
            seconds_run,
            _, _, _,
            model,
        ) = train_model(hyperparams, X_train, X_test, y_train, y_test)

        # Zapisz model i metryki w session_state
        st.session_state.model = model
        st.session_state.scores = {
            "train_score": train_score,
            "test_score": test_score,
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "confusion": confusion,
        }

        # TODO: Wyświetl metryki i wizualizacje
        # st.metric(...)
        # st.altair_chart(...)

# --- Tab 2: Predykcja ---
with tab2:
    st.markdown("""
    ## Zadania
    Pragniemy sprawdzić działanie nowej magicznej receptury. Od niej zależeć będzie życie mieszkańców królestwa!

    🎯 **Wymagane:**
    - Dodaj formularz do wprowadzania wartości składników
    - Dodaj przycisk uruchamiający predykcję
    - Wyświetl wynik: czy mikstura uzdrowi pacjenta

    🧠 **Dodatkowe wyzwania:**
    - Pokoloruj wynik predykcji (zielony/czerwony)
    - Dodaj wyświetlanie prawdopodobieństwa
    - Dodaj możliwość ponownego przeliczenia bez utraty modelu
    """)

    with st.form("prediction_form"):
        inputs = []
        for col in df.columns:
            val = st.number_input(f"{col}", min_value=0.0, value=1.0)
            inputs.append(val)
        pred_button = st.form_submit_button("🔮 Wykonaj predykcję")

    if pred_button:
        if st.session_state.model is None:
            st.warning("🔧 Najpierw wytrenuj model w zakładce 'Przygotuj recepturę'.")
        else:
            import numpy as np

            X_input = np.array(inputs).reshape(1, -1)
            prediction = st.session_state.model.predict(X_input)[0]
            prob = st.session_state.model.predict_proba(X_input)[0][1]

            if prediction:
                st.success(f"✅ Mikstura **UZDROWI** pacjenta! (Prawdopodobieństwo: {round_p(prob)})")
            else:
                st.error(f"❌ Mikstura **NIE ZADZIAŁA**! (Prawdopodobieństwo: {round_p(prob)})")

            with st.expander("📊 Wyniki ostatniego modelu"):
                for name, value in st.session_state.scores.items():
                    if name != "confusion":
                        st.write(f"**{name.replace('_', ' ').capitalize()}**: {round_p(value)}")

# --- Tab 3: Zadanie dodatkowe: własna wizualizacja ---
with tab3:
    st.markdown("""
    ## 🧠 Dodatkowe wyzwanie: Twoja alchemiczna wizja

    Spróbuj stworzyć własną wizualizację danych lub wyników działania modelu!

    ✨ **Pomysły:**
    - Histogram jednej ze zmiennych (np. długość pazura smoka)
    - Porównanie średnich wartości między klasami (Cured vs Not Cured)
    - Wykres punktowy (scatterplot) dwóch cech
    
    W tym miejscu masz pełną swobodę działania! 🎨
    """)

    st.info("Użyj np. `st.bar_chart(df)` lub `st.altair_chart(...)`")
