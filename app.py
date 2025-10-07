
import streamlit as st
import pickle

# -------------------------------
# Load model and vectorizer
# -------------------------------
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# -------------------------------
# Page configuration
# -------------------------------
st.set_page_config(
    page_title="Fake News Detector",
    page_icon="📰",
    layout="centered",
    initial_sidebar_state="expanded"
)

# -------------------------------
# App header
# -------------------------------
st.markdown("""
    <h1 style='text-align: center; color: #FF4B4B;'>📰 Fake News Detector</h1>
    <p style='text-align: center; color: #666;'>Enter news text below to check if it is Real or Fake.</p>
""", unsafe_allow_html=True)

# -------------------------------
# Sidebar instructions
# -------------------------------
st.sidebar.header("Instructions")
st.sidebar.write("""
1. Paste or type news text in the box.  
2. Click **Predict**.  
3. The app will classify the news as **Real** or **Fake**.  
4. It also shows the confidence/probability of the prediction.
""")

# -------------------------------
# Text input area
# -------------------------------
user_input = st.text_area("Enter news text here:", height=200)

# -------------------------------
# Prediction button
# -------------------------------
if st.button("Predict"):
    if user_input.strip() == "":
        st.warning("⚠️ Please enter some text!")
    else:
        # Transform input
        input_vect = vectorizer.transform([user_input])
        
        # Predict class
        prediction = model.predict(input_vect)[0]
        
        # Get prediction probabilities
        prob = model.predict_proba(input_vect)[0]
        fake_prob = prob[0] * 100
        real_prob = prob[1] * 100
        
        # Display result with colors
        if prediction == 0:
            st.markdown(f"<h3 style='color: red;'>❌ This news is Fake!</h3>", unsafe_allow_html=True)
        else:
            st.markdown(f"<h3 style='color: green;'>✅ This news is Real!</h3>", unsafe_allow_html=True)
        
        # Show probabilities
        st.info(f"Confidence:\n- Fake: {fake_prob:.2f}%\n- Real: {real_prob:.2f}%")

# -------------------------------
# Footer
# -------------------------------
st.markdown("""
    <hr>
    <p style='text-align: center; color: #999;'>Fake News Detector Project • Built by a student • Powered by Python, Streamlit & ML</p>
""", unsafe_allow_html=True)
