import streamlit as st
import os

# === Configuração da página ===
st.set_page_config(
    page_title="Immigration Court Manager",
    page_icon="⚖️",
    layout="wide"
)

# === Sidebar com logo ===
logo_path = "static/logo.png"
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, use_container_width=True)
else:
    st.sidebar.title("Immigration Court Manager")

st.sidebar.markdown("---")

# === Usuários e senhas (em produção, use banco e hash) ===
users = {
    "admin": "admin123",
    "client": "client123"
}

# === Inicializar variáveis de sessão ===
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None
if "login_message" not in st.session_state:
    st.session_state.login_message = ""

# === Função para fazer logout ===
def logout():
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.login_message = ""

# === Tela de login ===
if not st.session_state.logged_in:
    st.title("🔐 Login no Sistema")

    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    login_btn = st.button("Entrar")

    if login_btn:
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.session_state.user = username
            st.session_state.login_message = f"✅ Bem-vindo, {username}!"
            # Não usar st.experimental_rerun nem set_query_params
        else:
            st.error("❌ Usuário ou senha inválidos.")

    if st.session_state.login_message:
        st.success(st.session_state.login_message)

# === Tela principal (após login) ===
else:
    st.sidebar.subheader(f"👤 Usuário: {st.session_state.user}")
    if st.sidebar.button("Sair"):
        logout()
        st.experimental_rerun()

    # === Área ADMIN ===
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

    # === Área CLIENTE (upload somente) ===
    else:
        st.title("📤 Área de Upload de Documentos")
        st.info("Envie seus documentos diretamente para seu advogado.")

        upload_folder = "uploads"
        os.makedirs(upload_folder, exist_ok=True)

        uploaded_files = st.file_uploader(
            "Selecione os arquivos para upload",
            accept_multiple_files=True
        )

        if uploaded_files:
            for file in uploaded_files:
                file_path = os.path.join(upload_folder, file.name)
                with open(file_path, "wb") as f:
                    f.write(file.getbuffer())
                st.success(f"✅ Arquivo '{file.name}' enviado com sucesso!")
