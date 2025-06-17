
import streamlit as st
import os
import json
from datetime import datetime
from fpdf import FPDF

for folder in ["uploads", "templates", "static"]:
    os.makedirs(folder, exist_ok=True)

DB_FILE = "clients_data.json"
if os.path.exists(DB_FILE):
    with open(DB_FILE, "r") as f:
        clients = json.load(f)
else:
    clients = {}

def save_db():
    with open(DB_FILE, "w") as f:
        json.dump(clients, f, indent=4)

def create_client_folder(client_id):
    folder = os.path.join("uploads", client_id)
    os.makedirs(folder, exist_ok=True)
    return folder

def generate_toc(client_id):
    folder = os.path.join("uploads", client_id)
    toc = ["TABLE OF CONTENTS\n"]
    counter = 1

    for category in sorted(os.listdir(folder)):
        cat_path = os.path.join(folder, category)
        if os.path.isdir(cat_path):
            toc.append(f"{counter}. {category}\n")
            sub_counter = 1
            for file in sorted(os.listdir(cat_path)):
                toc.append(f"    {counter}.{sub_counter} {file}\n")
                sub_counter += 1
            counter += 1
    return "".join(toc)

st.set_page_config(page_title="Immigration Court Manager", layout="centered")
st.title("🗂️ Immigration Court Case Manager")

st.sidebar.image("static/logo.png", use_container_width=True)

menu = ["Login"]
choice = st.sidebar.selectbox("Menu", menu)

username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")
login_button = st.sidebar.button("Login")

USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "client1": {"password": "client123", "role": "client"}
}

if login_button:
    if username in USERS and USERS[username]['password'] == password:
        role = USERS[username]['role']
        st.session_state["role"] = role
        st.session_state["username"] = username
        st.experimental_rerun()
    else:
        st.error("❌ Invalid username or password")

if st.session_state.get("role") == "admin":
    st.success(f"Logged in as Admin: {st.session_state['username']}")
    tabs = st.tabs(["Manage Clients", "Documents", "Generate TOC"])

    with tabs[0]:
        st.subheader("➕ Add New Client")
        client_name = st.text_input("Full Name")
        client_a_number = st.text_input("A-Number")
        if st.button("Add Client"):
            client_id = client_a_number.strip().replace(" ", "_")
            clients[client_id] = {"name": client_name, "a_number": client_a_number}
            create_client_folder(client_id)
            save_db()
            st.success("Client added!")

        st.subheader("📋 Clients List")
        for cid, data in clients.items():
            st.write(f"**{data['name']}** | A#: {data['a_number']} | ID: {cid}")

    with tabs[1]:
        st.subheader("⬆️ Upload Documents")
        selected_client = st.selectbox("Select Client", list(clients.keys()))
        category = st.text_input("Document Category", placeholder="e.g., Notices, Identity, Hardship")
        files = st.file_uploader("Upload Files", accept_multiple_files=True)
        if st.button("Upload"):
            folder = os.path.join("uploads", selected_client, category)
            os.makedirs(folder, exist_ok=True)
            for file in files:
                with open(os.path.join(folder, file.name), "wb") as f:
                    f.write(file.read())
            st.success("Files uploaded!")

    with tabs[2]:
        st.subheader("📑 Generate Table of Contents")
        selected_client = st.selectbox("Select Client for TOC", list(clients.keys()), key="toc")
        toc = generate_toc(selected_client)
        st.text(toc)
        if st.button("Download TOC as PDF"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            for line in toc.split("\n"):
                pdf.multi_cell(0, 10, line)
            toc_path = f"uploads/{selected_client}/TOC.pdf"
            pdf.output(toc_path)
            with open(toc_path, "rb") as f:
                st.download_button("📥 Download TOC", data=f, file_name="TOC.pdf")

elif st.session_state.get("role") == "client":
    st.success(f"Logged in as Client: {st.session_state['username']}")
    st.subheader("⬆️ Upload Your Documents")
    client_id = st.session_state['username']
    category = st.text_input("Document Category", placeholder="e.g., Notices, Identity, Hardship")
    files = st.file_uploader("Upload Files", accept_multiple_files=True)
    if st.button("Upload"):
        folder = os.path.join("uploads", client_id, category)
        os.makedirs(folder, exist_ok=True)
        for file in files:
            with open(os.path.join(folder, file.name), "wb") as f:
                f.write(file.read())
        st.success("Files uploaded!")

if st.sidebar.button("Logout"):
    st.session_state.clear()
    st.experimental_rerun()
