# 🔐 Secure Data Encryption App

This is a simple yet secure web application built using **Streamlit** and **SQLite**, allowing users to **store and retrieve sensitive data** securely. All data is **encrypted using symmetric encryption (Fernet)** and protected with a user-defined passkey.

---

## 🚀 Features

- 🔐 **Encrypt and store sensitive data** like passwords, notes, or credentials.
- 🗝️ **Passkey-protected access** to stored secrets.
- 📁 Uses **SQLite** as the backend database.
- 🔒 All secrets are **encrypted using Fernet symmetric encryption**.
- 🔑 Stores hashed passkeys using **SHA-256** for extra security.

---

## 🧰 Tech Stack

- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [SQLite](https://www.sqlite.org/)
- [Cryptography (Fernet)](https://cryptography.io/en/latest/)
- [Hashlib (SHA-256)](https://docs.python.org/3/library/hashlib.html)

---

## 📦 Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/secure-data-encryption-app.git
    cd secure-data-encryption-app
    ```

2. **Create a virtual environment** (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the app**:
    ```bash
    streamlit run app.py
    ```

---

## 📝 How It Works

1. **Store Secret**:
   - Enter a unique label (ID).
   - Type in the secret data.
   - Set a passkey to protect the secret.
   - Your secret is encrypted and stored in the local database.

2. **Retrieve Secret**:
   - Enter the correct label and passkey.
   - If the passkey is correct, the decrypted secret is shown.

---

## 🛡️ Security Notes

- The encryption key (`simple_secret.key`) is generated once and reused for all encryption/decryption. Keep this file safe.
- The passkey is **not stored in plain text**. It is hashed using SHA-256.
- If the key file is lost or deleted, **all stored data will become unrecoverable**.

---