# 📧 AI-Powered Phishing Email Detection System

An AI/ML-based phishing email detection system built using **Python**, **Scikit-learn**, and **Random Forest Classifier**.  
This project analyzes email content, extracts security-related features, and classifies emails as **Phishing** or **Safe**.

---

## 🚀 Features

- 🔍 Detects phishing emails using Machine Learning
- 🧠 Feature extraction from:
  - URLs
  - Keywords
  - Email structure
- 📊 Random Forest classification model
- 📈 Confusion matrix visualization
- 📉 Feature importance analysis
- 🧪 Test predictions on custom emails
- 📚 Synthetic dataset generation for training/testing

---

## 🛠️ Tech Stack

- Python
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Seaborn

---

## 📂 Project Structure

```bash
.
├── main.py              # Main project file
├── README.md            # Project documentation
```

---

## ⚙️ Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/phishing-email-detector.git
cd phishing-email-detector
```

### 2️⃣ Install Dependencies

```bash
pip install pandas numpy scikit-learn matplotlib seaborn
```

---

## ▶️ Run the Project

```bash
python main.py
```

---

## 🧠 How It Works

The system performs the following steps:

### 1. Dataset Generation
Creates synthetic phishing and legitimate emails.

### 2. Feature Extraction
Extracts:
- URL-based features
- Keyword-based indicators
- Structural email patterns

### 3. Model Training
Uses a **Random Forest Classifier** for phishing detection.

### 4. Evaluation
Displays:
- Accuracy score
- Classification report
- Confusion matrix
- Feature importance

### 5. Prediction
Tests the model on sample real-world style emails.

---

## 🔍 Extracted Features

### 🌐 URL Features
- Number of URLs
- HTTP usage
- URL shorteners
- Suspicious TLDs
- Average URL length

### 🧠 Keyword Features
- Urgent language
- Verification requests
- Threat-based wording
- Suspicious phishing keywords

### 📑 Structural Features
- Email length
- Exclamation marks
- Uppercase word count
- Deadline phrases

---

## 📊 Model Performance

The model evaluates:
- Accuracy
- Precision
- Recall
- Confusion Matrix

Example output:

```bash
✓ Accuracy: 95%
✓ Precision: 94%
✓ Recall: 96%
```

---

## 🖼️ Visualizations

The project generates:
- 📉 Confusion Matrix Heatmap
- 📊 Feature Importance Graph

---

## 🧪 Sample Predictions

Example:

```bash
Prediction: ⚠️ PHISHING
Confidence: 97%
```

```bash
Prediction: ✅ SAFE
Confidence: 95%
```

---
