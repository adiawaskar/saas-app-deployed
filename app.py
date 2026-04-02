import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# ---------------------------
# Firebase Initialization
# ---------------------------
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(dict(st.secrets["firebase"]))
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error("🔥 Firebase not initialized. Check your secrets.toml or Streamlit secrets.")
        st.stop()

db = firestore.client()

# ---------------------------
# UI CONFIG
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
            try:
                db.collection("users").add({
                    "name": name,
                    "email": email,
                    "feedback": feedback
                })
                st.success("✅ Data stored successfully!")
            except Exception as e:
                st.error(f"Error storing data: {e}")
        else:
            st.error("⚠️ Please fill required fields")

# ---------------------------
# DASHBOARD PAGE
# ---------------------------
elif menu == "View Data":
    st.subheader("📊 Stored Entries")

    try:
        docs = db.collection("users").stream()

        data = []
        for doc in docs:
            data.append(doc.to_dict())

        if data:
            st.dataframe(data)
        else:
            st.info("No data yet")

    except Exception as e:
        st.error(f"Error fetching data: {e}")