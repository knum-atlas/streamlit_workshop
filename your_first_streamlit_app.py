import streamlit as st

st.title("Moja Aplikacja Streamlit")

st.write("To jest bardzo ogólny szablon aplikacji stworzony w Streamlit.")
st.markdown("to jest przykładowy tekst napisany w markdownie *ten sie chwieje*, a ten jest **pogrubiony**")

st.sidebar.header("Menu")
option = st.sidebar.selectbox("Wybierz opcję:", ["Opcja 1", "Opcja 2", "Opcja 3"])

if option == "Opcja 1":
    st.subheader("Widok dla Opcji 1")
    st.write("Tutaj możesz dodać kod lub elementy dla pierwszej opcji.")
elif option == "Opcja 2":
    st.subheader("Widok dla Opcji 2")
    st.write("Tutaj możesz dodać kod lub elementy dla drugiej opcji.")
elif option == "Opcja 3":
    st.subheader("Widok dla Opcji 3")
    st.write("Tutaj możesz dodać kod lub elementy dla trzeciej opcji.")


with st.form("my_form"):
    name = st.text_input("Wpisz swoje imię:")
    submitted = st.form_submit_button("Wyślij")
    if submitted:
        st.success(f"Cześć, {name}!")

st.write("---")
st.write("Aplikacja w Streamlit - szablon startowy")