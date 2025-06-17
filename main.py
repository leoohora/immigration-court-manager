import streamlit as st
import os
import json
import datetime
from pathlib import Path

# ============ CONFIGURAÇÕES DA PÁGINA ============
st.set_page_config(
    page_title="Immigration Court Manager",
    page_icon="⚖️",
    layout="wide"
)

# ============ CONFIGURAÇÃO DE USUÁRIOS ============
# Em produção, ideal usar um banco de dados e senhas criptografadas
USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "client1": {"password": "client123", "role": "client"},
}

# ============ CARREGAR DADOS DE CLIENTES ============
DATA_FILE = "clients_data.json"

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

with open(DATA_FILE, "r") as f:
    clients_data = json.load(f)

# ============ FUNÇÕES AUXILIARES ============

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(clients_data, f, indent=4)


def create_client_folder(client_name):
    base_path = Path("uploads") / client_name
    base_path.mkdir(parents=True, exist_ok=True)
    return base_path


def list_uploaded_files(client_name):
    folder = Path("uploads") / client_name
    if not folder.exists():
        return []
    return [f.name for f in folder.iterdir() if f.is_file()]


def generate_table_of_contents(file_list):
    toc = "TABLE OF CONTENTS\n\n"
    for idx, filename in enumerate(file_list, start=1):
        toc += f"{idx}. {filename}\n"
    return toc


def generate_motion(client_name, motion_type):
    template_path = Path("templates") / f"{motion_type}.txt"
    if not template_path.exists():
        return "❌ Template não encontrado."

    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    motion = template.replace("[CLIENT_NAME]", client_name)
    motion = motion.replace("[TODAY_DATE]", datetime.date.today().strftime("%B %d, %Y"))

    return motion


# ============ INTERFACE ============

# Sidebar com logo
if os.path.exists("static/logo.png"):
    st.sidebar.image("static/logo.png", use_container_width=True)
else:
    st.sidebar.title("Immigration Court Manager")

st.sidebar.markdown("---")

# Sessão
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.role = None

# ============ LOGIN ============
if not st.session_state.logged_in:
    st.title("🔐 Login no Sistema")

    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    login_button = st.button("Entrar")

    if login_button:
        user = USERS.get(username)
        if user and user["password"] == password:
            st.session_state.logged_in = True
            st.session_state.user = username
            st.session_state.role = user["role"]
            st.success(f"✅ Bem-vindo, {username}!")
        else:
            st.error("❌ Usuário ou senha inválidos.")

# ============ LOGOUT ============
else:
    st.sidebar.subheader(f"👤 Usuário: {st.session_state.user.capitalize()}")
    if st.sidebar.button("🚪 Sair"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.role = None
        st.experimental_rerun()

    # ============ DASHBOARD ADMIN ============
    if st.session_state.role == "admin":
        st.title("⚖️ Painel de Administração")

        st.subheader("📋 Lista de Clientes")
        client_list = list(clients_data.keys())

        if client_list:
            client_selected = st.selectbox("Selecione um cliente", client_list)

            if client_selected:
                st.subheader(f"📂 Gerenciando Cliente: {client_selected}")

                # Upload de documentos
                st.markdown("### 🔺 Upload de Documentos")
                uploaded_files = st.file_uploader(
                    "Selecione arquivos",
                    accept_multiple_files=True
                )
                if uploaded_files:
                    folder = create_client_folder(client_selected)
                    for file in uploaded_files:
                        file_path = folder / file.name
                        with open(file_path, "wb") as f:
                            f.write(file.getbuffer())
                        st.success(f"✅ '{file.name}' enviado com sucesso.")

                # Listar arquivos
                files = list_uploaded_files(client_selected)
                st.markdown("### 📑 Arquivos do Cliente")
                if files:
                    for file in files:
                        st.markdown(f"- {file}")
                else:
                    st.info("Nenhum arquivo enviado ainda.")

                # Geração de TOC
                st.markdown("### 🗂️ Gerar Table of Contents")
                if st.button("Gerar TOC"):
                    toc = generate_table_of_contents(files)
                    st.text_area("📄 Table of Contents", toc, height=200)

                # Geração de Motions
                st.markdown("### ✍️ Gerar Motion")
                motion_type = st.selectbox("Selecione o tipo de motion", ["motion_to_continue", "motion_to_change_venue"])
                if st.button("Gerar Motion"):
                    motion = generate_motion(client_selected, motion_type)
                    st.text_area("📄 Motion", motion, height=300)

        st.markdown("---")
        st.subheader("➕ Adicionar Novo Cliente")
        new_client = st.text_input("Nome do Cliente")
        if st.button("Adicionar Cliente"):
            if new_client and new_client not in clients_data:
                clients_data[new_client] = {"created": str(datetime.date.today())}
                save_data()
                st.success(f"✅ Cliente '{new_client}' adicionado.")
            else:
                st.error("⚠️ Nome inválido ou cliente já existe.")

    # ============ DASHBOARD CLIENTE ============
    else:
        st.title("📤 Área de Upload de Documentos")
        st.info("Envie seus documentos diretamente para seu advogado.")

        client_name = st.session_state.user
        folder = create_client_folder(client_name)

        uploaded_files = st.file_uploader(
            "Selecione arquivos para upload",
            accept_multiple_files=True
        )
        if uploaded_files:
            for file in uploaded_files:
                file_path = folder / file.name
                with open(file_path, "wb") as f:
                    f.write(file.getbuffer())
                st.success(f"✅ '{file.name}' enviado com sucesso.")

        # Mostrar arquivos enviados
        files = list_uploaded_files(client_name)
        st.subheader("📑 Seus arquivos enviados")
        if files:
            for file in files:
                st.markdown(f"- {file}")
        else:
            st.info("Nenhum arquivo enviado ainda.")
