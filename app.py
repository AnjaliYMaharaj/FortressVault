import streamlit as st
import random
import string
import pandas as pd
import os

# 1. Page Configuration
st.set_page_config(page_title="Fortress Vault", page_icon="🛡️", layout="centered")

# 2. Storage Setup
VAULT_FILE = "vault.csv"

# 3. Authentication Logic
def check_password():
    """Returns True if the user has the correct password."""
    if "password_correct" not in st.session_state:
        # --- THIS IS YOUR NEW HOME SCREEN FOR LOGGED-OUT USERS ---
        st.title("🛡️ Fortress Vault")
        st.subheader("Secure Password Management & Generation")
        
        st.info("🔐 This is a private security demonstration. Access is restricted.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Access the Vault")
            pwd = st.text_input("Enter Master Password", type="password")
            if st.button("Unlock Vault"):
                if pwd == st.secrets["MASTER_PASSWORD"]:
                    st.session_state["password_correct"] = True
                    st.rerun()
                else:
                    st.error("🚫 Incorrect Password.")
        
        with col2:
            st.markdown("### Request Entry")
            st.write("If you are a recruiter or collaborator, please use the link below to request the Master Password.")
            st.link_button("🤝 Request Key via Form", "https://forms.gle/Fou3KeXjTzYi5RBPA")
            st.caption("After requesting access, the confirmation window will provide further instructions.")
            
        return False
    return True

# 4. Main Application (Only runs if authenticated)
if check_password():
    # Sidebar for authenticated users
    with st.sidebar:
        st.title("🛡️ Vault Menu")
        st.success("Authenticated")
        if st.button("Logout"):
            st.session_state.clear()
            st.rerun()
        st.divider()
        st.write("**Project Milestone:** From Awareness to Action.")

    st.title("🛡️ Fortress Vault")
    st.caption("Logged in as Authorized User")

    # --- SECTION 1: GENERATOR & STRENGTH METER ---
    st.header("🔑 Generator")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        site_name = st.text_input("Service Name:", placeholder="e.g. GitHub")
        length = st.slider("Password Length", 8, 32, 16)
    
    with col2:
        st.write("Complexity Options")
        use_digits = st.checkbox("Include Numbers", value=True)
        use_special = st.checkbox("Include Symbols", value=True)

    # Strength Logic
    strength_score = 0
    if length >= 12: strength_score += 1
    if length >= 16: strength_score += 1
    if use_digits: strength_score += 1
    if use_special: strength_score += 1

    # Visual Strength Meter
    st.write("**Strength Feedback:**")
    if strength_score <= 1:
        st.error("Status: WEAK")
        st.progress(25)
    elif strength_score == 2:
        st.warning("Status: FAIR")
        st.progress(50)
    elif strength_score == 3:
        st.info("Status: STRONG")
        st.progress(75)
    else:
        st.success("Status: EXTREME")
        st.progress(100)

    if st.button("✨ Generate & Save to Vault"):
        if site_name:
            chars = string.ascii_letters
            if use_digits: chars += string.digits
            if use_special: chars += "!@#$%^&*"
            pwd = ''.join(random.choice(chars) for _ in range(length))
            
            new_entry = pd.DataFrame([[site_name, pwd]], columns=["Website", "Password"])
            if os.path.isfile(VAULT_FILE):
                new_entry.to_csv(VAULT_FILE, mode='a', index=False, header=False)
            else:
                new_entry.to_csv(VAULT_FILE, index=False)
            
            st.success(f"Saved! Password: `{pwd}`")
        else:
            st.warning("⚠️ Please enter a service name.")

    # --- SECTION 2: MANAGED VAULT ---
    st.divider()
    st.header("🗄️ Managed Vault")
    
    if os.path.isfile(VAULT_FILE):
        df = pd.read_csv(VAULT_FILE)
        
        st.write("Double-click cells to edit. Use the table trash icon to delete rows.")
        edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic")
        
        save_col, download_col, delete_col = st.columns([1, 1, 1])
        
        with save_col:
            if st.button("💾 Save Changes"):
                edited_df.to_csv(VAULT_FILE, index=False)
                st.success("Vault Updated!")
                st.rerun()

        with download_col:
            csv = edited_df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Backup", data=csv, file_name="vault_backup.csv", mime="text/csv")

        with delete_col:
            if st.button("🗑️ Clear All Data", type="primary"):
                st.session_state["confirm_delete"] = True
        
        if st.session_state.get("confirm_delete"):
            st.warning("⚠️ Delete ALL passwords?")
            if st.button("Yes, Confirm Total Deletion"):
                os.remove(VAULT_FILE)
                st.session_state["confirm_delete"] = False
                st.rerun()
            if st.button("Cancel"):
                st.session_state["confirm_delete"] = False
                st.rerun()
    else:
        st.info("Your vault is empty.")

    st.divider()
    st.caption("Build with focus on Digital Safety and Human-Centered Security.")

