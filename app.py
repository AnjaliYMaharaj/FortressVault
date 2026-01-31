import streamlit as st
import random
import string
import pandas as pd
import os

# 1. Page Configuration
st.set_page_config(page_title="Fortress Vault", page_icon="🛡️", layout="centered")

# 2. Authentication Logic
def check_password():
    """Returns True if the user has the correct password."""
    if "password_correct" not in st.session_state:
        st.title("🔐 Vault Access")
        st.markdown("Please authenticate to manage your secure keys.")
        pwd = st.text_input("Master Password", type="password")
        if st.button("Unlock Vault"):
            if pwd == st.secrets["MASTER_PASSWORD"]:
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("🚫 Incorrect Password. Access Denied.")
        return False
    return True

# 3. Main Application
if check_password():
    st.title("🛡️ Fortress Vault")
    st.caption("Secure Password Generation & Management")
    
    VAULT_FILE = "vault.csv"

    # --- SIDEBAR: LOGOUT & UTILS ---
    with st.sidebar:
        st.header("Settings")
        if st.button("Logout"):
            st.session_state.clear()
            st.rerun()
        st.divider()
        st.info("Fortress Vault uses local CSV storage for your credentials.")

    # --- SECTION 1: GENERATOR & STRENGTH METER ---
    st.header("🔑 Generator")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        site_name = st.text_input("Service Name:", placeholder="e.g. Amazon")
        length = st.slider("Password Length", 8, 32, 16)
    
    with col2:
        st.write("Complexity Options")
        use_digits = st.checkbox("Include Numbers", value=True)
        use_special = st.checkbox("Include Symbols", value=True)

    # Strength Logic Calculations
    strength_score = 0
    if length >= 12: strength_score += 1
    if length >= 16: strength_score += 1
    if use_digits: strength_score += 1
    if use_special: strength_score += 1

    # Visual Strength Meter
    st.write("**Real-time Strength Check:**")
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
            
            # Save Logic
            new_entry = pd.DataFrame([[site_name, pwd]], columns=["Website", "Password"])
            if os.path.isfile(VAULT_FILE):
                new_entry.to_csv(VAULT_FILE, mode='a', index=False, header=False)
            else:
                new_entry.to_csv(VAULT_FILE, index=False)
            
            st.success(f"Successfully saved for **{site_name}**!")
            st.code(pwd, language="text")
        else:
            st.warning("⚠️ Please enter a service name before generating.")

    # --- SECTION 2: MANAGED VAULT ---
    st.divider()
    st.header("🗄️ Managed Vault")
    
    if os.path.isfile(VAULT_FILE):
        df = pd.read_csv(VAULT_FILE)
        
        # Edit/Delete Interface
        st.write("Double-click any cell to edit. Use the trash icon to delete rows.")
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

        # --- THE "NUKE" OPTION ---
        with delete_col:
            if st.button("🗑️ Clear All Data", type="primary"):
                # Confirmation step to prevent accidental clicks
                st.session_state["confirm_delete"] = True
        
        if st.session_state.get("confirm_delete"):
            st.warning("⚠️ Are you absolutely sure? This will delete ALL saved passwords.")
            if st.button("Confirm Total Deletion"):
                os.remove(VAULT_FILE)
                st.session_state["confirm_delete"] = False
                st.success("Vault wiped clean.")
                st.rerun()
            if st.button("Cancel"):
                st.session_state["confirm_delete"] = False
                st.rerun()
    else:
        st.info("Your vault is empty. Generate your first password above.")

    st.divider()
    st.caption("Build with focus on Digital Safety and Human-Centered Security.")

