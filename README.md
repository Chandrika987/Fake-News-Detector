

# Fake-News-Detector

This project uses **Machine Learning** to detect whether a news article is **real or fake** using text classification.

## 🧾 Project Overview

Fake news has become a major problem in the digital age.  
This project demonstrates how Natural Language Processing (NLP) and Machine Learning can be used to automatically detect fake news articles based on their content.  
It helps readers identify misinformation and promotes media literacy.

---

## 🚀 Features

- Detects fake and real news based on the article content  
- Uses **TF-IDF Vectorization** + **Logistic Regression**  
- Achieves high accuracy on benchmark datasets  
- Web interface built using **Streamlit** 
---

## 🧰 Technologies Used

- Python 
- Scikit-learn   
- Pandas & NumPy  
- Streamlit  
- Jupyter Notebook  

## 📂 Files

| File | Description |
|------|--------------|
| `logistic_model.ipynb` | Jupyter Notebook – data loading, training, and model building |
| `true.csv`, `fake.csv` | Datasets used for training |
| `model.pkl`, `vectorizer.pkl` | Saved model and vectorizer |
| `app.py` | Streamlit web app (used in Phase 2) |
| `README.md` | Project documentation |

---
## 🔁 Project Workflow

1. Data Collection → `true.csv`, `fake.csv`  
2. Data Preprocessing and Cleaning  
3. Feature Extraction using TF-IDF  
4. Model Training with Logistic Regression  
5. Saving Model (`model.pkl`) and Vectorizer (`vectorizer.pkl`)  
6. Deploying using Streamlit Web App


##  Model Details

- **Algorithm:** Logistic Regression  
- **Vectorization:** TF-IDF  
- **Accuracy:** ~98% (on test data)  

---

## Future Improvements

- **Add more advanced NLP models (e.g., BERT)
- **Deploy on Streamlit Cloud or Hugging Face Spaces
- **Create a browser extension for real-time fake news checking
- **Improve dataset quality with live web scraping


