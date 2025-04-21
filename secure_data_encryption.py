import streamlit as st
import sqlite3
import hashlib
import os
from cryptography.fernet import Fernet

# ========== Encryption Key Setup ==========
KEY_FILE = "simple_secret.key"

def load_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as file:
            file.write(key)
    else:
        with open(KEY_FILE, "rb") as file:
            key = file.read()
    return key

cipher = Fernet(load_key())

# ========== Database Initialization ==========
def init_db():
    conn = sqlite3.connect("simple_data.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vault (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            LABEL TEXT NOT NULL UNIQUE,
            encrypted_text TEXT NOT NULL,
            passkey TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Call the DB init function once
init_db()

# ========== Helper Functions ==========
def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

def encrypt_data(text):
    return cipher.encrypt(text.encode()).decode()

def decrypt(encrypted_text):
    return cipher.decrypt(encrypted_text.encode()).decode()

# ========== Streamlit App ==========
st.title("🔐 Secure Data Encryption")
st.write("Store and encrypt your sensitive data securely.")
st.write("All data is encrypted using a symmetric key encryption algorithm.")

menu = ["Store Secret", "Retrieve Secret"]
choice = st.sidebar.selectbox("Select an option", menu)

if choice == "Store Secret":
    st.header("Store a new Secret")
    
    label = st.text_input("Label (Unique ID): ")
    secret = st.text_area("Secret Data: ")
    passkey = st.text_input("Passkey (to protect it): ", type="password")
    
    if st.button("Encrypt and Save"):
        if label and secret and passkey:
            conn = sqlite3.connect("simple_data.db")
            cursor = conn.cursor()
            encrypted_data = encrypt_data(secret)
            hashed_passkey = hash_passkey(passkey)
            try:
                cursor.execute("INSERT INTO vault (LABEL, encrypted_text, passkey) VALUES (?, ?, ?)", 
                               (label, encrypted_data, hashed_passkey))
                conn.commit()
                st.success("✅ Secret stored successfully!")
            except sqlite3.IntegrityError:
                st.error("❌ Label already exists. Please use a different label.")
            finally:
                conn.close()
        else:
            st.error("⚠️ Please fill in all fields.")

elif choice == "Retrieve Secret":
    st.header("Retrieve a Secret")
    
    label = st.text_input("Enter the Label: ")
    passkey = st.text_input("Enter the Passkey: ", type="password")
    
    if st.button("Decrypt"):
        if label and passkey:
            conn = sqlite3.connect("simple_data.db")
            cursor = conn.cursor()
            cursor.execute("SELECT encrypted_text, passkey FROM vault WHERE LABEL=?", (label,))
            result = cursor.fetchone()
            
            if result:
                encrypted_data, stored_passkey = result
                if hash_passkey(passkey) == stored_passkey:
                    decrypted_data = decrypt(encrypted_data)
                    st.success(f"✅ Decrypted Data: {decrypted_data}")
                else:
                    st.error("❌ Incorrect passkey.")
            else:
                st.error("❌ Label not found.")
            conn.close()
        else:
            st.error("⚠️ Please fill in all fields.")