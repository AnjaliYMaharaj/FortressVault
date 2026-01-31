import streamlit as st
import random
import string
import pandas as pd
import os

# 1. Page Config
st.set_page_config(page_title="Fortress Vault", page_icon="🛡️")

# 2. Authentication Logic
def check_password():
    if "password_correct" not in st.session_state:
        st.title("🔐 Vault Access")
        pwd = st.text_input("Enter Master Password", type="password")
        if st.button("Unlock"):
            if pwd == st.secrets["MASTER_PASSWORD"]:
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("Incorrect Password")
        return False
    return True

if check_password():
    st.title("🛡️ Fortress Vault")
    VAULT_FILE = "vault.csv"

    # --- SECTION 1: GENERATOR WITH STRENGTH METER ---
    st.header("🔑 Password Generator")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        site_name = st.text_input("Website Name:", placeholder="e.g., GitHub")
        length = st.slider("Length", 8, 32, 16)
    
    with col2:
        use_digits = st.checkbox("Numbers", value=True)
        use_special = st.checkbox("Symbols", value=True)

    # Strength Logic
    strength_score = 0
    if length >= 12: strength_score += 1
    if length >= 16: strength_score += 1
    if use_digits: strength_score += 1
    if use_special: strength_score += 1

    # Visual Meter
    if strength_score <= 1:
        st.error("Strength: WEAK")
        st.progress(25)
    elif strength_score == 2:
        st.warning("Strength: FAIR")
        st.progress(50)
    elif strength_score == 3:
        st.info("Strength: STRONG")
        st.progress(75)
    else:
        st.success("Strength: EXTREME")
        st.progress(100)

    if st.button("Generate & Save"):
        if site_name:
            chars = string.ascii_letters
            if use_digits: chars += string.digits
            if use_special: chars += "!@#$%^&*"
            pwd = ''.join(random.choice(chars) for _ in range(length))
            
            # Save to CSV
            new_entry = pd.DataFrame([[site_name, pwd]], columns=["Website", "Password"])
            if os.path.isfile(VAULT_FILE):
                new_entry.to_csv(VAULT_FILE, mode='a', index=False, header=False)
            else:
                new_entry.to_csv(VAULT_FILE, index=False)
            st.success(f"Saved! Password: `{pwd}`")
        else:
            st.warning("Please enter a website name.")

    # --- SECTION 2: EDITABLE MANAGER & DOWNLOAD ---
    st.divider()
    st.header("🗄️ Managed Vault")
    
    if os.path.isfile(VAULT_FILE):
        df = pd.read_csv(VAULT_FILE)
        
        # Edit and Delete interface
        edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic")
        
        if st.button("💾 Save Changes"):
            edited_df.to_csv(VAULT_FILE, index=False)
            st.success("Vault Updated!")
            st.rerun()

        # Download Backup
        csv = edited_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Backup", data=csv, file_name="vault_backup.csv", mime="text/csv")
    else:
        st.info("No passwords saved yet.")

    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()
