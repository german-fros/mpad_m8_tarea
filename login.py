import streamlit as st

# Usuarios permitidos (clave = usuario, valor = contraseña)
USUARIOS = {
    "admin": "sportsdatacampus",
    "invitado": "MPAD_M8"
}

def login():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.title("🔐 Iniciar Sesión")

        with st.form("login_form"):
            usuario = st.text_input("Usuario")
            contraseña = st.text_input("Contraseña", type="password")
            submit = st.form_submit_button("Entrar")

            if submit:
                if usuario in USUARIOS and USUARIOS[usuario] == contraseña:
                    st.session_state.logged_in = True
                    st.session_state.usuario = usuario
                    st.rerun()
                    st.success("Inicio de sesión exitoso. Recargá la página si no continúa.")
                else:
                    st.error("Credenciales inválidas")
        st.stop()  # Detiene la ejecución de la app hasta que haya login
