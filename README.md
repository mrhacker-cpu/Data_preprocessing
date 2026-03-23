# 🚀 CSV Intelligence Studio

A powerful **GUI-based Data Preprocessing and Analytics Tool** built using Python and CustomTkinter.
This application enables users to perform end-to-end data preprocessing operations with an interactive dashboard.

---

## 📌 Features

### 🧹 Data Cleaning

* Remove null values
* Fill missing values (numeric + categorical)
* Drop duplicates (with preview & column selection)

### 🔄 Data Transformation

* Min-Max Scaling
* Standard Scaling
* Categorical Encoding (One-Hot Encoding)

### 🔗 Data Integration

* Merge multiple CSV/Excel files
* Join datasets based on selected column

### 📉 Data Reduction

* Sampling (reduce dataset size)
* PCA (Dimensionality Reduction)

---

### 📊 Visualization & Insights

* Multi-column histogram visualization
* Real-time graph updates
* Dataset summary (rows, columns, missing values)
* Smart insights:

  * Missing value detection
  * Duplicate detection
  * Skewness analysis

---

### 🎯 Advanced Features

* 🔍 Search and filter data
* 🎚️ Interactive slider-based filtering
* 📋 Responsive table (auto-adjusting layout)
* 🔄 Undo functionality
* 💾 Save & load session
* 📁 Export processed dataset
* 🌙 Dark / Light mode toggle
* 📂 Supports CSV & Excel (.xlsx)

---

## 🖥️ Tech Stack

* Python 🐍
* CustomTkinter (Modern GUI)
* Pandas (Data Processing)
* NumPy
* Matplotlib & Seaborn (Visualization)
* Scikit-learn (Scaling & PCA)

---

## 📁 Project Structure

```
csv_preprocessor/
│
├── app.py
├── requirements.txt
├── .gitignore
│
└── modules/
    ├── file_handler.py
    ├── preprocessing.py
    └── visualization.py
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone <your-repo-link>
cd csv_preprocessor
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

### 3️⃣ Activate Environment

```bash
venv\Scripts\activate
```

### 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 5️⃣ Run the Application

```bash
python app.py
```

---

## 📸 Screenshots

> Add screenshots of your UI here for better presentation

---

## 🧠 How It Works

1. Upload a dataset (CSV or Excel)
2. Preview and explore data
3. Apply preprocessing techniques
4. Visualize results dynamically
5. Export cleaned dataset

---

## 🎓 Academic Coverage

This project implements all major stages of **Data Preprocessing**:

* Data Cleaning ✔️
* Data Transformation ✔️
* Data Integration ✔️
* Data Reduction ✔️

---

## 💬 Viva / Interview Explanation

> “This project is a GUI-based data preprocessing system that integrates cleaning, transformation, integration, and reduction techniques with real-time visualization and user interaction.”

---

## 🚀 Future Enhancements

* Excel sheet selection UI
* Column-wise filtering panel
* Machine Learning model integration
* Web deployment (Streamlit version)

---

## ⭐ Acknowledgment

Developed as part of academic coursework to demonstrate practical implementation of data preprocessing concepts.

---
