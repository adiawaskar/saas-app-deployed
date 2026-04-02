import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json

# ---------------------------
# Firebase Initialization
# ---------------------------
if not firebase_admin._apps:
    if "firebase" in st.secrets:
        cred = credentials.Certificate(dict(st.secrets["firebase"]))
    else:
        cred = credentials.Certificate("firebase_key.json")
    
    firebase_admin.initialize_app(cred)

db = firestore.client()

# ---------------------------
# UI
# ---------------------------
st.set_page_config(page_title="SaaS App", layout="centered")

st.title("🚀 Mini SaaS App")

menu = st.sidebar.selectbox("Menu", ["Submit Form", "View Data"])

# ---------------------------
# FORM PAGE
# ---------------------------
if menu == "Submit Form":
    st.subheader("Enter Details")

    name = st.text_input("Name")
    email = st.text_input("Email")
    feedback = st.text_area("Feedback")

    if st.button("Submit"):
        if name and email:
            db.collection("users").add({
                "name": name,
                "email": email,
                "feedback": feedback
            })
            st.success("✅ Data stored successfully!")
        else:
            st.error("⚠️ Please fill required fields")

# ---------------------------
# DASHBOARD PAGE
# ---------------------------
elif menu == "View Data":
    st.subheader("📊 Stored Entries")

    docs = db.collection("users").stream()

    data = []
    for doc in docs:
        data.append(doc.to_dict())

    if data:
        st.dataframe(data)
    else:
        st.info("No data yet")