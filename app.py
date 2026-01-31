import streamlit as st
import random
import string
import pandas as pd
import os

# 1. Page Config
st.set_page_config(page_title="Fortress Vault", page_icon="🛡️")

# 2. Simple Authentication Logic
def check_password():
    """Returns True if the user had the correct password."""
    def password_entered():
        # Change 'mysecret123' to whatever you want your master password to be
        if st.session_state["password"] == st.secrets["MASTER_PASSWORD"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password
        st.title("🔐 Vault Access")
        st.text_input("Enter Master Password", type="password", on_change=password_entered, key="password")
        st.info("Identity is the first perimeter. Please authenticate to view your keys.")
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error
        st.title("🔐 Vault Access")
        st.text_input("Enter Master Password", type="password", on_change=password_entered, key="password")
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct
        return True

# 3. Only run the app if authenticated
if check_password():
    
    # --- VAULT APP CODE STARTS HERE ---
    st.title("🛡️ Fortress Vault")
    
    # Setup Storage
    VAULT_FILE = "vault.csv"

    def save_to_vault(site, password):
        new_data = pd.DataFrame([[site, password]], columns=["Website", "Password"])
        if os.path.isfile(VAULT_FILE):
            new_data.to_csv(VAULT_FILE, mode='a', index=False, header=False)
        else:
            new_data.to_csv(VAULT_FILE, index=False)

    # --- GENERATOR SECTION ---
    st.header("🔑 New Entry")
    site_name = st.text_input("Website Name:")
    if st.button("Generate & Store"):
        if site_name:
            chars = string.ascii_letters + string.digits + "!@#$%^&*"
            pwd = ''.join(random.choice(chars) for _ in range(16))
            save_to_vault(site_name, pwd)
            st.success(f"Key saved for {site_name}!")
        else:
            st.warning("Enter a site name.")

    # --- MANAGER SECTION ---
    st.divider()
    st.header("🗄️ Your Stored Keys")
    if os.path.isfile(VAULT_FILE):
        df = pd.read_csv(VAULT_FILE)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Vault is empty.")

    if st.button("Logout"):
        st.session_state["password_correct"] = False
        st.rerun()