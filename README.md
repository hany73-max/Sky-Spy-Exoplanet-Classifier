# 🌌✨ Exo Explorers – *A World Away* ✨🌌  

![Exoplanet Banner](https://www.nasa.gov/wp-content/uploads/2023/05/exoplanet_banner.jpg)  

<div align="center">

🛰️ *Exploring distant worlds with the power of AI* 🛰️  

[![Made with Python](https://img.shields.io/badge/Made%20with-Python-3776AB?logo=python&logoColor=white)](https://www.python.org/)  
[![XGBoost](https://img.shields.io/badge/Model-XGBoost-EB5E28?logo=python&logoColor=white)](https://xgboost.ai/)  
[![NASA Data](https://img.shields.io/badge/Data-NASA-blue?logo=nasa&logoColor=white)](https://exoplanetarchive.ipac.caltech.edu/)  
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)  

</div>

---

## 🚀 Project Overview  
We are **Exo Explorers**, tackling NASA’s **A World Away Challenge**.  
Our mission: use **Artificial Intelligence & Machine Learning** to detect **exoplanets** from NASA’s **Kepler** and **TESS** datasets.  

💡 Why? Because somewhere out there, another Earth could be waiting. 🌍✨  

---

## 🎯 Challenge Addressed  
> **Create an AI/ML model trained on NASA’s open-source exoplanet datasets that can analyze new data to identify exoplanets.**  

**Why it matters:**  
- 🌠 Exoplanet discovery helps us explore life beyond Earth  
- ⏱️ Manual classification = slow & error-prone  
- 🤖 AI scales the search & accelerates discovery  

---

## 🛠️ Approach  

### 1️⃣ Data Selection  
- Used **Kepler** + **TESS** datasets  
- Combined for more features + bigger sample size  

### 2️⃣ Data Preprocessing  
- 🧹 Cleaned noisy values  
- 🕳️ Fixed missing data  
- ⚖️ Balanced the classes  
- ✂️ Split into Train/Test  

### 3️⃣ Modeling  
- 🔬 Tested **13 ML models**  
- 📈 Accuracy range: *85–93%*  
- 🏆 Best: **XGBClassifier (~90%)**  

**Why XGB?**  
- ✔ Handles noisy & imbalanced data  
- ✔ Boosting reduces errors step-by-step  
- ✔ Outperformed other models in consistency  

### 4️⃣ Prediction  
- Trained on **Confirmed + False Positives**  
- Predicted on **Candidate exoplanets**  
- ✅ Detected possible new worlds! 🌍🪐  

---

## 📊 Results & Visualization  

| Metric        | Score  |
|---------------|--------|
| Accuracy      | ~90%   |
| Precision     | High   |
| Recall        | Strong |
| F1-Score      | Balanced |

🔭 Visualizations included:  
- Exoplanet class distributions  
- Confusion matrices  
- Model performance plots  
- Candidate prediction outcomes  

---

## 🌍 Impact & Future Work  
- ⚡ Automates exoplanet detection  
- 🧠 Reduces time for astronomers  
- 🌌 Future: connect with **real-time telescope data**  
- 🔮 Potential to classify other cosmic objects  

---

## 👨‍🚀 Team – Exo Explorers  

- 🪐 [Your Name 1] – Data Preprocessing & Cleaning  
- 🚀 [Your Name 2] – Modeling & AI Development  
- 🌠 [Your Name 3] – Visualization & Dashboards  
- 🌌 [Your Name 4] – Presentation & Storytelling  

---

## 📂 Repo Structure  

├── data/ # Cleaned & raw datasets
├── notebooks/ # Jupyter notebooks
├── models/ # Saved models (XGB, etc.)
├── visualization/ # Graphs & charts
├── presentation/ # Slides + Demo video
└── README.md # Documentation


---

## ⚙️ Tech Stack  

- 🐍 Python  
- 📊 Pandas, NumPy, Matplotlib, Seaborn  
- 🤖 Scikit-learn, XGBoost  
- 🌌 NASA Kepler & TESS datasets  
- 📓 Jupyter Notebooks  
- 📺 Streamlit for dashboard  

---

## 📜 License  
This project uses **NASA’s Open Data**  
Licensed under [MIT License](LICENSE).  

---

<div align="center">

🌠 *"We are explorers, turning data into discovery."* 🌠  

</div>