# 🌌 Sky Spy: AI for Exoplanet Discovery  

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)  
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-XGBoost-orange?logo=scikitlearn)  
![NASA Space Apps](https://img.shields.io/badge/NASA-Space%20Apps%20Challenge-black?logo=nasa)  
![Status](https://img.shields.io/badge/Status-Prototype-green)  

> *“When the sky is full of stars… which ones hide new worlds?”*  

Sky Spy is an AI-powered tool built by **Team Exo Explorers** for the **NASA Space Apps Challenge**.  
Our mission? To use **machine learning** and **open NASA data** to uncover the hidden planets orbiting distant stars — faster, smarter, and more transparently than ever before.  

---

## 📖 Table of Contents  
- [✨ Why Sky Spy?](#-why-sky-spy)  
- [🛰️ The Challenge We Tackled](#️-the-challenge-we-tackled)  
- [🧩 How It Works](#-how-it-works)  
- [🌍 Features](#-features)  
- [🚀 Future Directions](#-future-directions)  
- [👩‍🚀 Team Exo Explorers](#-team-exo-explorers)  
- [🖼️ Screenshots & Demo](#️-screenshots--demo)  
- [⚙️ How to Run](#️-how-to-run)  

---

## ✨ Why Sky Spy?  
- NASA missions like **Kepler** and **TESS** have given us **oceans of data**.  
- Thousands of exoplanets were discovered, but most detections were done **manually** — slow, noisy, and error-prone.  
- With AI, we can:  
  - Detect exoplanets **automatically**  
  - Handle **noisy, imbalanced datasets**  
  - Give **transparent visualizations** that even non-experts can understand  

---

## 🛰️ The Challenge We Tackled  
> **A World Away** — analyzing massive exoplanet datasets to identify new planets using AI/ML.  

Our goal was to train a model on open NASA datasets and make it:  
- Accurate  
- Transparent  
- Interactive  

---

## 🧩 How It Works  

### 1. **Datasets & Preprocessing**  
- Sources: **Kepler** + **TESS**  
- Cleaning: removed noise, filled missing values, dropped irrelevant columns  
- Split into **training/testing** sets  

### 2. **Modelling**  
- Tested **13+ models** (Random Forest, Gradient Boosting, etc.)  
- Winner: **XGBoost Classifier** 🚀  
- Why? It builds multiple decision trees, learns from mistakes, and thrives in **noisy NASA data**  

### 3. **Results**  
- Accuracy: **~90%**  
- Detected > **90% of confirmed exoplanets**  
- Confidence score: **97%**  

### 4. **Visualization**  
Because numbers alone are boring…  
- Scatter plots: planet radius vs star mass  
- Correlation heatmaps: which features matter most  
- Feature importance: why the AI makes decisions  

### 5. **Web Demo**  
- Users input planet data (mass, radius, distance)  
- Output: **Confirmed / Candidate / False Positive**  
- Instant visual explanation for transparency  

---

## 🌍 Features  
✔️ Handles messy real-world datasets  
✔️ Delivers predictions with **confidence + reasons**  
✔️ Transparent **visual storytelling** for users  
✔️ Interactive web demo anyone can try  

---

## 🚀 Future Directions  
- Link with **real-time NASA updates** for continuous learning  
- Add **3D visualizations** of planetary orbits in PowerPoint-style or WebGL  
- Expand classification to stars, moons, or even **rogue planets**  
- Turn Sky Spy into a full **public exploration tool** for space enthusiasts  

---

## 👩‍🚀 Team Exo Explorers  
We’re dreamers, coders, and space nerds who believe discovery should be:  
- Fast ⚡  
- Transparent 🔍  
- Accessible 🌍  

### 👩‍🚀 Team Members  
- **Hany** — Team Leader  
- **Rania** — Data Preprocessing & Modelling  
- **Tasneem** — Training & Evaluation  
- **Mriam** — Visualization & Web  
- **Mariam** — Presentation & Design  

---

## ⚙️ How to Run  

### 🔧 Requirements used in this project 
- Python==3.13
- pi==25.2
- numpy==1.24.4
- pandas==1.5.3
- scikit-learn==1.2.2
- xgboost==1.7.6
- matplotlib==3.7.1
- seaborn==0.12.2
- streamlit==1.27.2
- requests==2.31.0

### 📦 Installation  
Clone the repo and install dependencies:  

```bash
git clone https://github.com/yourusername/sky-spy.git
cd sky-spy
pip install -r requirements.txt
```

### ▶️ Run the Project  
For training and evaluation:  

```bash
python train_model.py
```

For visualization dashboard (Streamlit):  

```bash
streamlit run app.py
```

Then open: **http://localhost:8501/**  

---

🌌 *Sky Spy isn’t just a project. It’s our telescope into the unknown.*  
