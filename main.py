import streamlit as st
import os

st.set_page_config(
    page_title="Immigration Court Manager",
    page_icon="⚖️",
    layout="wide"
)

if os.path.exists("static/logo.png"):
    st.sidebar.image("static/logo.png", use_container_width=True)
else:
    st.sidebar.title("Immigration Court Manager")

st.sidebar.markdown("---")

users = {
    "admin": "admin123",
    "client": "client123"
}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None

if not st.session_state.logged_in:
    st.title("🔐 Login no Sistema")

    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    login_button = st.button("Entrar")

    if login_button:
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.session_state.user = username
            st.success(f"✅ Bem-vindo, {username}!")
        else:
            st.error("❌ Usuário ou senha inválidos.")

else:
    st.sidebar.subheader(f"👤 Usuário: {st.session_state.user}")
    logout = st.sidebar.button("Sair")

    if logout:
        st.session_state.logged_in = False
        st.session_state.user = None

    if st.session_state.user == "admin":
        st.title("⚖️ Painel de Administração")
        st.subheader("📄 Gerenciamento de Casos")
        st.info("Aqui você pode gerenciar os casos, criar Table of Contents, gerar Motions automáticas, etc.")
        st.subheader("🗂️ Upload e Organização de Documentos")
        st.info("Futuramente, integrar com email para ler arquivos de corte automaticamente.")
        st.subheader("✍️ Geração de Motions Automáticas")
        st.info("Use templates para criar documentos legais rapidamente.")
        st.subheader("🔐 Gerenciar Acesso de Clientes")
        st.info("Futuramente: gerar link seguro de upload para clientes.")
    else:
        st.title("📤 Área de Upload de Documentos")
        st.info("Envie seus documentos diretamente para seu advogado.")

        upload_folder = "uploads"
        os.makedirs(upload_folder, exist_ok=True)

        uploaded_files = st.file_uploader("Selecione os arquivos para upload", accept_multiple_files=True)

        if uploaded_files:
            for file in uploaded_files:
                file_path = os.path.join(upload_folder, file.name)
                with open(file_path, "wb") as f:
                    f.write(file.getbuffer())
                st.success(f"✅ Arquivo '{file.name}' enviado com sucesso!")

